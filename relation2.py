from easygui import *
import csv
import tkinter as tk
from tkinter import filedialog



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


#check which elements of relation are not on right side of dict O(n) put them in Key list (values) of dict
def getStartingKeyList(funcDepend, relation):
    listToExclude = set()

    for value in funcDepend.values():
        if len(value) > 1:
            for j in range(len(value)):
                listToExclude.add(value[j])
        else:
            listToExclude.add(value)

    keyList = []

    for i in range(len(relation)):
        if relation[i] not in listToExclude:
            keyList.append(relation[i])

    return keyList

def main():
    msgbox('Please choose the file which holds the relation and functional dependencies')
    #get the relation and functional dependencies
    relation, funcDepend = relationread()

    keyList = getStartingKeyList(funcDepend, relation)

    print(keyList)

main()