# User Guide 

## GUI
![](./design/gui.png)
### Input Data 
The data must be in JSON format (a single JSON object per line), sample data can be viewed [here](./src/data).

### Usage Guide
The interface includes every function of the program. The top bar holds the file path for the JSON file which can be specified by the user. The application uses relative paths therefore it is recommended the JSON file is located in the same directory as the program executable. Clicking ‘Select’ initialises the program to fetch and read the JSON file, with the output in the textbox below the top bar. If the program detects that the JSON file is invalid or cannot be read, this will be indicated within the textbox.
The user and document UUIDs can be specified by typing into the associated input boxes within the bottom bar, and then clicking confirm to source the requested data. To request a data analysis function, select one of the buttons at the bottom of the window to perform the analysis. Some instances will have an output in the main text box above, for example ‘Top 10 Readers’, while graphs will generate a new file and save it within the directory of the main program.

### Button to-task Guide
- Task 2a and 2b relate to ‘Views by Country’ and ‘Views by Continent’ buttons respectively.
- Task 3b relates to ‘Views by Browser’ button
- Task 4 relates to ‘Top 10 Readers’ button
- Task 5d relates to ‘Top Also Likes Docs’ button
- Task 6 relates to ‘Also likes graph’ button
- Task 7 opens the GUI

## Command Line Interface
The following command structure is used for the command line interface:
`cw2 -u user_uuid -d doc_uuid -t task_id -f file_name`
- `cw2` is the executable name or main.py file
- `-u` specifies user UUID, this argument is optional
- `-d` specifies document UUID, this argument is optional for tasks 4 and 7
- `-t` specifies task_id, this is a required argument and accepts the following values: {2a, 2b, 3a, 3b, 4, 5d, 6, 7}
- `-f` specifies a path to a JSON file, this argument is optional for task 7. The application uses relative paths with respect to the directory the executable is called from.