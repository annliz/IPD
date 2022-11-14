import gspread
import requests
from tqdm import tqdm
import types

from loguru import logger

from game_specs import *
from default_functions import *
from simulation import *
from output_locations import *


# retrieve latest list of submissions from google sheets
# link to the sheet: https://docs.google.com/spreadsheets/d/1YZZQFShRcYO4p3pCqBY5LPZf4pO9zfmt6b6BNItVb3g/edit?usp=sharing
# returns all data on the spreadsheet
def get_spreadsheet_data():
    print("Retrieving spreadsheet data...")
    service_account = gspread.service_account(filename="service_account.json")
    spreadsheet = service_account.open("IPD Player Strategies")
    worksheet = spreadsheet.worksheet("Form Responses 1")
    print("Retrieved spreadsheet data.")
    return worksheet.get_all_values()

import os

# returns an array of dictionary objects, each being a student
# student format: {name, link, function_names, code}
#                 where function_names is a list
def get_students_and_code(data):
    students = []
    
    print("Retrieving student code...")
    
    # # iterate through all submissions (every student)
    # for i in tqdm(range(1, len(data))):
    #     student = {}
    #     student["student_name"] = data[i][1]
        
    #     # accessing and parsing code from pastebin
    #     index = 2 # index of column for pastebin links in the spreadsheet. index of 2 is for the no noise data
    #     if NOISE:
    #         index = 3 # column index 3 (which is column D) contains links to submissions for tournament with noise
    #     link = data[i][index]
    #     if not "https://pastebin.com/" in link: # checks that valid pastebin link is submitted
    #         logger.error(f"Could not parse {data[i][1]}'s pastebin link")
    #         continue
    #     link = "https://pastebin.com/raw/" + link.split("pastebin.com/")[-1] # link to raw text on pastebin
    #     req = requests.get(link)
    #     print(req.status_code)
    #     code = req.text

    #     # try:
    #     #     code = open(f"./cache/{link.split('pastebin.com/')[-1]}.py").read() # retrieves the raw text from pastebin
    #     # except:
    #     #     code = ""
        
    #     student["link"] = link
    #     student["code"] = code
        
    #     # print("---", student["student_name"], "'s code retrieved.")
    #     students.append(student)

    for i in os.listdir("./cache_noise"):
        students.append({"code":  open(f"./cache_noise/{i}").read()})
        
    print("Retrieved all student code.")
    return students

# load all the functions that will actually be playing
def load_functions(students):    
    functions = []
    # bad_kids = []
    
    # iterate through all students (that are still valid)
    for i in tqdm(range(len(students))):
        # print("Loading student's functions:", students[i]["student_name"])
        try:
            exec(students[i]["code"]) # execute the student's code                
        except Exception as e:
            logger.error(f"Failed to execute code: {str(e)}")
            # add student to list of students whose functions did not compile
            # bad_kids.append(students[i]["student_name"])
            
    # get all the functions that have been loaded without issue
    loaded_functions = [f for f in locals().values() if type(f) == types.FunctionType]
    
    # filter for functions that pass basic input/output check
    good, bad = test_io_functions(loaded_functions)
    loaded_functions = good
    
    print("Removed", len(bad), "functions for bad IO.")
    print("Loaded", len(loaded_functions), " good functions.")
    return loaded_functions


# tests function input and outputs
# input must be three arguments: your past moves, opponent's past moves, and round number
def test_io_functions(functions):
    good_functions = []
    bad_functions = []
    
    # iterates through each function
    for function in functions:
        try:
            with suppress_stdout(): # ignore all printed statements from these functions
                output = function([True]*10,[False]*10,10) # run the function
                if output==None:
                    raise Exception("function returned None (make sure you are returning something)")
                if output:
                    pass # ensure output is boolean value (or int 0 or 1)
                good_functions.append(function)
        except Exception as e:
            logger.error(f"Testing I/O of {function.__name__} failed: {str(e)}")
            bad_functions.append(function)
        
    return good_functions, bad_functions
