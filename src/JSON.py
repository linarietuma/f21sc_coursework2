# Code developed by Lina Rietuma and Ryan Farish 

import re
import json
import os.path
import numpy as np
import pandas as pd
from functools import cmp_to_key


class JSON:
    def __init__(self, path):
        # check if the url is valid
        current_path = os.getcwd() # current directory path
        config_path = os.path.join(current_path, path) # create absolute file path
        if os.path.exists(path): # relative path exists
            self.path = path
        elif os.path.exists(config_path): # absolute path exists
            self.path = config_path
        else: # path not found
            raise ValueError("Error: File not found, invlaid path: {}".format(config_path)) 

        try:
            data = self.read_data()
            self.data = data
        except:
            raise ValueError("Failed to load the data.")

        
    def read_data(self):
        """" Reads data from a JSON file and processes into a list of individual JSON objects line by line """
        
        try:
            # create a file object for the given file path
            with open(self.path) as f:
                # process the file line by line for efficiency 
                objects = [json.loads(line) for line in f]
        except:
            raise ValueError("Failed to load the JSON file.")
        # return a list of JSON objects
        return objects
    
    def filter_data(self, key, filter_by):
        """ Filters input data by the given key and filter_by value """
        try:
            # return an array of json objects where elements equal the filter_by value for the given key
            filtered = [obj for obj in self.data if obj[key] == filter_by]
        except:
            raise ValueError("Invalid key.")
        return filtered
    

    # returns a 2D array of unique elements and their corresponding counts
    # key is a json key, e.g. visitor_country, visitor_uuid etc
    # data is a list of json objects 
    def views_by(self, key, doc_uuid, process_browser=False):
        """ Find the frequency of unique elements for the given key and document UUID """
        
        # get elements for the given key from data filtered by event type (only interested in read events)
        elements = np.array([el[key] for el in self.filter_data('event_type', 'read') if el['env_doc_id'] == doc_uuid])           

        # if views by browser (processed version)
        if process_browser:
            # returns a list of shortened browsers names in the format 'main browser - subtype'
            elements = self.find_browser(elements)

        # find frequency of unique elements 
        (unique_els, counts) = np.unique(elements, return_counts=True)
        
        # combine unique elements and their counts into a 2D array
        # set dtype as object to maintain object types of unique_els and counts
        frequencies = np.array((unique_els, counts), dtype=object)
        
        # sort frequencies by counts 
        sorted_list = frequencies[:, frequencies[1].argsort()]
                   
        return sorted_list


    # useragents is a list of visitor_useragent strings (including the details of browser version, OS etc)
    def find_browser(self, useragents):
        """ For each value in the input list, finds main browser name and subtype from a browser string """

        # matches the begining of a string until the first '/' character
        main_rgx = r'[^/]+'
        # finds the first instance of the given browser names
        subtype_rgx = r'(\bChrome\b|\bSafari\b|\bFirefox\b|\bTrident\b|\bSilk\b|\bPresto\b)(?=\/)'
        
        for i, el in enumerate(useragents):
            # find the main browser name 
            x = re.match(main_rgx, el)
            # find the browser subtype
            y = re.search(subtype_rgx, el)

            if y is not None:
                y = y.group() # get the matched value
            else:
                # browser name not among the more popular types
                y = 'Other'    
            
            # assign the shortened browser name and type as element value
            useragents[i] = '{} - {}'.format(x.group(), y)
            
        return useragents
    
    
    def top_readers(self):
        """ Finds top 10 readers based on cumulative read time"""
        # retruns a list of arrays with visitor uuid and readtime
        pagereadtimes = [[el['visitor_uuid'], el['event_readtime']] for el in self.data if el['event_type'] == 'pagereadtime']
        
        # parse data as a dataframe 
        df = pd.DataFrame(data=pagereadtimes, columns = ['visitor_uuid', 'event_readtime'])
        
        # group rows by visitor_uuid, sum elements in event_readtime column and return top 10 instances
        top_readers = df.groupby(['visitor_uuid']).sum().nlargest(10,['event_readtime'])

        # convert pandas dataframe to a list of tuples
        counts = top_readers.to_records()
        
        # format the list of tuples as a string
        string_list = ['{} - {} hours'.format(el[0], round(el[1]/3600000, 2)) for el in counts]
        string = "\n".join(string_list)
        # returns s string in the format 'reader uuid - total reading time (in hours)'
        return string


    # by default returns all readers for a given document uuid
    def get_unique(self, uuid, data, input_uuid='', filter_by_doc=True):
        """  Returns unique readers (default)/ documents or for the given document/ reader uuid, excluding the input_uuid (for also likes function)"""
        
        # returns all readers for a given document uuid
        if filter_by_doc == True:
            key='visitor_uuid' 
            filter_by='env_doc_id'
        # returns all documents read for a given user_uuid
        else: 
            filter_by='visitor_uuid'
            key='env_doc_id'

        # retrieve values for the given key and filter value, excluding input_uuid (optional) 
        elements = np.array([obj[key] for obj in data if obj[filter_by] == uuid and obj[key] != input_uuid])
        # get unique values
        unique_elements = np.unique(elements)

        # return a list of unique elements
        return unique_elements

    
    def also_likes(self, doc_uuid, user_uuid=None):
        """ Finds a list of documents read by the readers (excluding user_uuid if provided) of the given doc_uuid """
        
        # filter out read events 
        data = self.filter_data('event_type', 'read')

         # find all readers of the document with the provided doc_uuid  
        if user_uuid is None:
            readers = self.get_unique(doc_uuid, data)
        else:
            # exclude user_uuid if provided 
            readers = self.get_unique(doc_uuid, data, input_uuid=user_uuid)
          
        readers_dict = {} # dictionary of user uuid (last 4 digits) as key for a list of read documents by the user
        for r in readers:
            # find other documents read by the readers of the provided document
            r_docs = self.get_unique(r, data, input_uuid=doc_uuid, filter_by_doc=False)
            if r_docs.size != 0: # reader has read other documents besides input doc
                # save last 4 digits as dictionary key, a list of unique documents as input
                readers_dict[r[-4:]] = r_docs 

        return readers_dict # return the dictionary

    # Reference: http://www.macs.hw.ac.uk/~hwloidl/Courses/F21SC/Samples/ho_sort.py
    def custom_cmp(x,y):
        """Custom comparison operator to return inverse of the default order."""
        # compares the first elements of the tuples
        return (-1)*(x[0]-y[0])

    # Reference: http://www.macs.hw.ac.uk/~hwloidl/Courses/F21SC/Samples/ho_sort.py 
    def count(x, dict):
        """ Count the number of occurrences of x in the dictionary """
        n = 0
        # iterate over the dictionary entries
        for k in dict.keys():
            if x in dict[k]:
                n += 1
        return n
    
    # Reference: http://www.macs.hw.ac.uk/~hwloidl/Courses/F21SC/Samples/ho_sort.py   
    def top_counts(self, dict, decorator=count, sort_cmp=custom_cmp):
        """Returns top 10 elements with the highest count using a decorator function argument."""
        list = np.array([])
        for val in dict.values():
            list = np.append(list, val)
        unique = np.unique(list)
        # decorate each unique element with element counts as the first arg in the tuple, element as the second
        xs_dec = [ (decorator(x, dict), x) for x in unique ]

        # sort the list by first component in the tuple (nr of counts)
        xs_dec.sort(key=cmp_to_key(sort_cmp))

        if len(xs_dec) > 10:
            top_docs = xs_dec[:10]  # return top 10 values
        else:
            top_docs = xs_dec

        # format the top documents as a string
        string_list = ['{} - {}'.format(el[1], el[0]) for el in top_docs]
        string = "\n".join(string_list)
         
        return string, top_docs

    

    
    





