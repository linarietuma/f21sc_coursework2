# Code developed by Lina Rietuma and Ryan Farish 

# Imports
import graph
import JSON
import tkinter as tk
from tkinter import *
import main
import os

class GUI(tk.Tk):
    def __init__(self):
        self.json = None
        self.doc_uuid = None
        self.user_uuid = None

         # Create the GUI object
        tk.Tk.__init__(self)
        self.title('JSON Data Reader') # GUI title
        
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = int(screen_width/2)
        height = int(screen_height/2)
        # set the minimum size of the GUI as half of the user screen dimensions
        self.minsize(width, height)
        
        self.main_frame = Frame(self)
        self.main_frame.pack(padx=15, pady=15)

        self.window = Canvas(self.main_frame, width=width, height=height)
        self.window.pack()

        # File search section of GUI
        # Created a grid structure for entities
        Label(self.window, text='File Path:').grid(row=0)
        self.entry = Entry(self.window, width=65) # file path text box
        self.entry.grid(row=0, column=1)
        self.select = Button(self.window, text='Select', width=10, fg='black', command=self.select_btn_click).grid(row=0, column=2)

        # Main text box for information display
        # Creates additional frame below the file search
        search_frame = Frame(self.main_frame)
        search_frame.pack(side=TOP, expand=True)
        # main text box for information display
        self.main_text = Text(search_frame, width=120, padx=15)
        self.main_text.configure(state='disabled') # disable the text box   
        self.main_text.pack()

        # Bottom half of GUI
        # ID search function and buttons
        idframe = Frame(self.main_frame)
        idframe.pack(side=TOP)

        # First row of buttons go here
        midframe = Frame(self.main_frame)
        midframe.pack(side=BOTTOM, pady=2)

        # Bottom row of buttons go here
        mainframe = Frame(self.main_frame)
        mainframe.pack(side=BOTTOM)

        # User and Document ID search input
        # boxes and labels
        Label(idframe, text='Doc UUID:').grid(row=0, column=2)
        self.entry_doc = Entry(idframe, width=30)
        self.entry_doc.grid(row=0, column=3)
        Label(idframe, text='User UUID:').grid(row=0, column=0)
        self.entry_user = Entry(idframe, width=30)
        self.entry_user.grid(row=0, column=1)
        self.confirm = Button(idframe, text='Confirm', width=10, fg='black', command=self.confirm_btn_click).grid(row=0, column=4)

        # Buttons for different functions of the code
        self.country_view = Button(midframe, text='Views by Country', width=25, command=self.views_by_country_btn_click)
        self.country_view.pack(side=LEFT)
        self.continent_view = Button(midframe, text='Views by Continent', width=25, command=self.views_by_continent_btn_click)
        self.continent_view.pack(side=LEFT)
        self.browser_view = Button(midframe, text='Views by Browser', width=25, command=self.views_by_browser_btn_click)
        self.browser_view.pack(side=LEFT)
        self.profile_view = Button(mainframe, text='Top 10 Readers', width=25, command=self.top_readers_btn_click)
        self.profile_view.pack(side=LEFT)
        self.likes_view = Button(mainframe, text='Top Also Likes Docs', width=25, command=self.top_also_likes_btn_click)
        self.likes_view.pack(side=LEFT)
        self.likes_graph_view = Button(mainframe, text='Also Likes Graph', width=25, command=self.also_likes_graph_btn_click)
        self.likes_graph_view.pack(side=LEFT)
       

    def select_btn_click(self):
        """ Event listener for the 'Select' button.
            Initialises a JSON class with the provided file path. """
        self.set_text('1.0', 'Reading data...', delete=True)
        try:
            self.json = JSON.JSON(self.entry.get().strip()) # remove whitespace
            self.set_text('end', 'Data load successful!')   
        except:
            app_path = os.getcwd() # get current path
            config_path = os.path.join(app_path, self.entry.get().strip()) # get the full path
            self.set_text('1.0', 'Read unsuccessful, make sure the file and path exist: {}'.format(config_path), delete=True)
    
    def confirm_btn_click(self):
        """ Event listener for the 'Confirm' button.
            Saves input user and document UUIDs as local variables. """
        # delete previous doc and user UUID
        self.doc_uuid = None
        self.user_uuid = None
        if len(self.entry_doc.get()) != 0:
            self.doc_uuid = self.entry_doc.get().strip()  # remove whitespace
            self.set_text('end', 'Document UUID set.')
        if len(self.entry_user.get()) != 0:
            self.user_uuid = self.entry_user.get().strip()  # remove whitespace
            self.set_text('end', 'User UUID set.')
    
    def views_by_country_btn_click(self):
        """ Event listener for 'Views By Country' button.
            Displays a histogram of views grouped by country for a given document """

        if self.json is None:  # no JSON file is provided
            self.set_text('1.0', 'No JSON data file provided!', delete=True)
        elif self.doc_uuid is None: # no document UUID is provided
            self.set_text('1.0', 'Please provide a document and user (optional) UUID!', delete=True)
        else:
            try:
                main.task_2a(self.json, self.doc_uuid)
            except: # no instances for the given document were found
                self.set_text('1.0', 'No instances found for the given document UUID in the JSON file provided.' + 
                                    '\n' 'Double check the document UUID is valid: {}'.format(self.doc_uuid), delete=True)
    
    def views_by_continent_btn_click(self):
        """ Event listener for 'Views By Continent' button.
            Displays a histogram of views grouped by continent for a given document """

        if self.json is None:  # no JSON file is provided
            self.set_text('1.0', 'No JSON data file provided!', delete=True)
        elif self.doc_uuid is None: # no document UUID is provided
            self.set_text('1.0', 'Please provide a document and user (optional) UUID!', delete=True)
        else:
            try:
                main.task_2b(self.json, self.doc_uuid)
            except: # no instances for the given document were found
                self.set_text('1.0', 'No instances found for the given document UUID in the JSON file provided.' + 
                                    '\n' 'Double check the document UUID is valid: {}'.format(self.doc_uuid), delete=True)
    
    def views_by_browser_btn_click(self):
        """ Event listener for 'Views By Browser' button.
            Displays a histogram of views grouped by browser for a given document """

        if self.json is None:  # no JSON file is provided
            self.set_text('1.0', 'No JSON data file provided!', delete=True)
        elif self.doc_uuid is None: # no document UUID is provided
            self.set_text('1.0', 'Please provide a document and user (optional) UUID!', delete=True)
        else:
            try:
                main.task_3b(self.json, self.doc_uuid)
            except: # no instances for the given document were found
                self.set_text('1.0', 'No instances found for the given document UUID in the JSON file provided.' + 
                                    '\n' 'Double check the document UUID is valid: {}'.format(self.doc_uuid), delete=True)
    
    def top_readers_btn_click(self):
        """ Event listener for the 'Top 10 Readers' button.
            Displays a list of 10 readers with the highest reading time """

        if self.json is None: # no JSON file provided
            self.set_text('1.0', 'No JSON data file provided!', delete=True)
        else:
            top_readers = self.json.top_readers() # get the list of top readers
            # set the header
            self.set_text('1.0', 'Reader UUID - Total Reading Time' + '\n', delete=True)
            self.set_text('end', top_readers) # display the list
    
    def set_text(self, index, text, delete=False):
        """ Sets text in the main text box """
        self.main_text['state'] = 'normal' # activate the text area
        if delete: # delete any previous text from the text box
            self.main_text.delete('1.0', 'end')
        self.main_text.insert(index, '\n' + text)
        self.main_text['state'] = 'disabled' # deactivate the text area
    
    def also_likes(self):
        """ Retruns a dictionary of readers (of the input document) as keys and unique list of documents they've read as the value """
        if self.json is None:  # no JSON file provided
            self.set_text('1.0', 'No JSON data file provided!', delete=True)  
        elif self.doc_uuid is None: # no document UUID is provided
            self.set_text('1.0', 'Please provide a document and user (optional) UUID!', delete=True)
        elif self.json is not None and self.doc_uuid is not None: # both JSON doc and doc UUID are are provided
            dict = self.json.also_likes(self.doc_uuid, user_uuid=self.user_uuid)
            if bool(dict) is False: # the dictionary of 'also likes' documents is empty 
                self.set_text('1.0', 'No "also likes" documents found, check the document UUID and try again!', delete=True)
            else:
                return dict

    def also_likes_graph_btn_click(self):
        """ Event listener for the 'Also Likes Graph' button.
            Return a pdf of 'Also Likes' graph in a separate window. """
        dict = self.also_likes()
        if dict is not None: # dictionary is not empty
            string, top_docs = self.json.top_counts(dict) # get top 10 most read 'also likes' documents 
            # instantiate the graph class
            likes_graph = graph.graph(dict, top_docs, self.doc_uuid, user_uuid=self.user_uuid) 
            likes_graph.also_likes() # get the 'also likes' graph 

    def top_also_likes_btn_click(self):
        """ Event listener for the 'Top Also Likes Docs' button.
            Displays a list of most read 'also likes' documents for the input doc UUID. """
        dict = self.also_likes()
        if dict is not None: # dictionary is not empty
            top_docs, list = self.json.top_counts(dict)
            self.set_text('1.0', 'Document UUID - Times Read By Readers Of {}'.format(self.doc_uuid) + '\n', delete=True)
            self.set_text('end', top_docs)
    



        
        

 



