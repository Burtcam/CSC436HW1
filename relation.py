from easygui import *
import csv
import tkinter as tk
from tkinter import filedialog
import copy


def getfiledir():
    root = tk.Tk()
    root.withdraw()

    fie_path = filedialog.askopenfilename()

    return fie_path

def relationread():
    ##GET DATA
    goodFile = False
    while goodFile == False:
        # calls to Dialog.py and opens a dialog box for the user to select a file.
        fname = getfiledir()
        # Begin exception handling
        try:
            # Try to open the file using the name given
            olympicsFile = open(fname, 'r')
            # If the name is valid, set Boolean to true to exit loop
            goodFile = True
        except:
            # If the name is not valid - IOError exception is raised
            print("Invalid filename, please try again ... ")

    reader = csv.reader(olympicsFile)
    relation = next(reader)
    funcdep = {}
    #get the functional dependencies
    reader = csv.DictReader(olympicsFile, fieldnames=("input", "output"))
    for row in reader:
        #thisdict["color"] = "red"
        funcdep[row['input']] = row['output']


    olympicsFile.close


    return relation, funcdep

def checkwhatcanbemade(key, funcDepend):
    #loop through key, call each on funcDepend, if found, add to key and call the value on funcDepend until an element in Key already is found
    for i in range(len(key)):
        key.append(funcDepend[key[i]])
        temp = funcDepend[key[i]]
        ##KEEP GOING UNTIL result of funcDepend[key[i] is not in funcDepend.values()
        while temp in funcDepend:
            temp = funcDepend[temp]
            key.append(temp)

    return key
#key = AECDBFDBB
def main():
    msgbox('Please choose the file which holds the relation and functional dependencies')
    #get the relation and functional dependencies
    relation, funcDepend = relationread()

    key = []
    #check which elements of relation are not on right side of dict O(n) put them in Key list (values) of dict
    for i in range(len(relation)):
        if relation[i] not in funcDepend.values():
            key.append(relation[i])

    #call each element of key list on dict. Add the result to found list O(n) for loop, O(1) for each dict call
    found = checkwhatcanbemade(copy.deepcopy(key), funcDepend)

    #check each element of relation in found list, if not, add to key.
    for i in range(len(relation)):
        if relation[i] not in found:
            key.append(relation[i])

    print ("The Candidate keys are: ", key)


main()