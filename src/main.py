# Code developed by Lina Rietuma and Ryan Farish 

import argparse
import graph
import hist
import JSON
import os
import gui

def main():
    # create an argument parser object 
    parser = argparse.ArgumentParser(prog='cw2', description='Performs the tasks for F21SC coursework.')
    # add the required arguments
    parser.add_argument('-u', '-user_uuid', help='User_UUID', default=None)
    parser.add_argument('-d', '-doc_uuid',help='Document_UUID')
    parser.add_argument('-t', '-task_id',help='Task ID', choices=['2a', '2b', '3a', '3b', '4', '5d', '6', '7'], required=True)
    parser.add_argument('-f', '-file_name',help='JSON File')

    args = parser.parse_args() # get input arguments 
    
    if args.t == '7':
        task_7() # open GUI
    else:
        validate_file(args.f) # check file is valid
        json = JSON.JSON(args.f) # create a JSON file

        if args.t == '2a':
            validate_doc(args.d) 
            try:
                task_2a(json, args.d) # views by country historgam
            except:
                print("No instances found for the given document UUID in the JSON file provided.")
                exit()
        elif args.t == '2b':
            validate_doc(args.d)
            try:
                task_2b(json, args.d) # views by continent histogram 
            except:
                print("No instances found for the given document UUID in the JSON file provided.")
                exit()
        elif args.t == '3a':
            validate_doc(args.d)
            try:
                task_3a(json, args.d) # views by browser histogram (full browser names)
            except:
                print("No instances found for the given document UUID in the JSON file provided.")
                exit()
        elif args.t == '3b':
            validate_doc(args.d)
            try:
                task_3b(json, args.d) # views by browser histogram (shortened browser names)
            except:
                print("No instances found for the given document UUID in the JSON file provided.")
                exit()
        elif args.t == '4':
            task_4(args) # list of top 10 readers
        elif args.t == '5d':
            validate_doc(args.d)
            task_5d(args) # list of top 10 'also likes' documents
        elif args.t == '6':
            validate_doc(args.d)
            task_6(json, args.d, args.u) # 'also likes' graph
    

def validate_file(file):
    """ Validates the file provided exists and has .json extension """
    # Check if the file exists
    if not os.path.exists(file):
        print("Error: No such file in the current directory '{}'".format(file))
        exit()

    # Check if the file has .json extension 
    if not file.endswith('.json'):
        print("Error: Must provide a JSON file '{}'".format(file))
        exit()

def validate_doc(doc):
    """ Checks if the document UUID has been provided """
    if doc is None:
        print('Error: No document UUID provided.')
        exit()


def task_2a(json, doc_uuid):
    """ Returns a histogram of views for a given document grouped by country """
    by_country = json.views_by('visitor_country', doc_uuid)
    if len(by_country) == 0: # no readers found for the given document 
        raise Exception
    else:
        histogram = hist.histogram(by_country) 
        histogram.hist("Views by Country")

def task_2b(json, doc_uuid):
    """ Displays a histogram of document views by continent """
    by_continent = json.views_by('visitor_country', doc_uuid)
    if len(by_continent) == 0: # no readers found for the given document 
        raise Exception
    else:
        histogram = hist.histogram(by_continent) 
        histogram.hist("Views by Continent", continents=True)

def task_3a(json, doc_uuid):
    """ Displays a histogram of document views by browser (full) """
    by_agent = json.views_by('visitor_useragent', doc_uuid)
    if len(by_agent) == 0: # no readers found for the given document 
        raise Exception
    else:
        histogram = hist.histogram(by_agent) 
        histogram.hist("Views by Browser")

def task_3b(json, doc_uuid):
    """ Displays a histogram of document views by browser (shortened) """
    by_agent = json.views_by('visitor_useragent', doc_uuid, process_browser=True)
    if len(by_agent) == 0: # no readers found for the given document 
        raise Exception
    else:
        histogram = hist.histogram(by_agent) 
        histogram.hist("Views by Browser")


def task_4(args):
    """ Prints a list of top 10 readers based on total reading time. """
    json = JSON.JSON(args.f)
    top_readers = json.top_readers()
    print('\n' + 'Reader UUID - Total Read Time' + '\n')
    print(top_readers + '\n')

def task_5d(args):
    """ Prints a list of top 10 'also likes' documents """
    json = JSON.JSON(args.f)
    dict = json.also_likes(args.d, user_uuid=args.u)
    top_docs, list = json.top_counts(dict)
    print('\n' + 'Document UUID - Times Read By Readers Of {}'.format(args.d) + '\n')
    print(top_docs + '\n')   
    

def task_6(json, doc_uuid, user_uuid):
    """ Displays 'also likes' graph. """
    dict = json.also_likes(doc_uuid, user_uuid=user_uuid)
    string, top_docs = json.top_counts(dict)
    likes_graph = graph.graph(dict, top_docs, doc_uuid, user_uuid=user_uuid)
    likes_graph.also_likes()
    
def task_7():
    """ Initialises the GUI """
    guis = gui.GUI()
    # Function loop to check for inputs
    guis.mainloop()


if __name__ == "__main__":
    # call main() function
    main()
