# Code developed by Lina Rietuma and Ryan Farish 

import matplotlib.pyplot as plt
import pycountry_convert as pc
from textwrap import wrap
import pandas as pd
import numpy as np

class histogram:
    def __init__(self, array):
        self.els = array[0]
        self.counts = array[1]
    
    # country codes must be in a two-letter uppercase ISO3166 code format
    def find_continents(self):
        """ Given lists of country codes and their counts, finds the corresponding continent for each country
            and groups the countries by continent, summing the counts of each country """
        
        continents = [] # corresponding continents for each country go here
        # find the respective continent for each country in the elements list
        for country in self.els:
            try:
                continent  = pc.country_alpha2_to_continent_code(country)
                continents.append(continent)
            except:
                # if continent search unsuccessful
                continents.append('U')

        # convert data to pandas dataframe
        df = pd.DataFrame(data=continents, columns=['continents'])
        df['counts'] = self.counts
        # group countries by continent, summing the counts of the countries
        frequencies = df.groupby(['continents']).sum()

        # convert pandas dataframe to a list of tuples
        conts = frequencies.to_records()
        # convert the list of tuples to 2D Numpy array 
        array = np.array([list(item) for item in conts]).T

        # convert continent ISO codes to full names
        els = [self.to_full_name(el) for el in array[0]]
        # convert counts to integers
        freq = list(map(int, array[1]))

        freqs = np.array((els, freq), dtype=object)
        
        # sort frequencies by counts 
        sorted_list = freqs[:, freqs[1].argsort()]

        # return a sorted 2D array
        return sorted_list[0], sorted_list[1]

    
    def  to_full_name(self, continent):
        """ Converts continent ISO codes to their full names """

        if continent == "SA":
            return "South America"
        elif continent == "OC":
            return "Oceania"
        elif continent == "NA":
            return "North America"
        elif continent == "EU":
            return "Europe"
        elif continent == "AS":
            return "Asia"
        elif continent == "AF":
            return "Africa"
        elif continent == "AN":
            return "Antarctica"
        else:
            return "Unknown"


    def hist(self, title, continents=False):
        """ Returns a histogram for the input data """

        if continents:
            # group countries by continent
            els, counts = self.find_continents()
        else:
            els, counts = self.els, self.counts

        plt.rcParams.update({'font.size': 11}) # set the overall font size of the graph
        # determines the coordinates of each bar on the y axis
        y_coords = np.arange(len(els))
        # relative width of the bars
        width = 0.9

        # graph height is dependant on the number of elements provided
        if len(els) > 8: # if the nr of elements 8+, set a constant height
            height = 8.5
            plt.rcParams.update({'font.size': 8})
        else:
            height = len(els) +1

        fig, ax = plt.subplots(figsize = (12, height))
        hbars = ax.barh(y_coords, counts, height=width, align='center') # create a bar plot
        # set the location and labels of the y axis
        ax.set_yticks(y_coords)
        # wrap the labels if very long 
        if len(els[0]) > 30:
            els = [ '\n'.join(wrap(l, 20)) for l in els ]
        ax.set_yticklabels(els)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Frequency')
        ax.bar_label(hbars) # set bar labels
        ax.set_xlim(right=0.5 + 1 * counts[-1])  # adjust xlim to fit labels
        ax.set_title(title) # set figure title
        
        plt.tight_layout(pad=0.15)
        plt.show()

