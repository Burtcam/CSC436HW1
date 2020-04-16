from easygui import *
import csv
import tkinter as tk
from tkinter import filedialog
import copy
import collections


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



def leftside(funcDepend, relation):

    #for each input of funcDepend,
    leftside = []
    final = []
    #put the keys in a list
    for key in funcDepend.keys():
        leftside.append(key)
    #split the values of the keys up
    for i in range(len(leftside)):
        if len(leftside[i])>1:
            for j in range(len(leftside[i])):
                final.append(leftside[i][j])
        else:
            final.append(leftside[i])
    #remove duplicates
    final = list(dict.fromkeys(final))

    return final


def rightside(funcDepend, relation):

    #for each input of funcDepend,
    rightside = []
    final = []
    #put the keys in a list
    for key in funcDepend.values():
        rightside.append(key)
    #split the values of the keys up
    for i in range(len(rightside)):
        if len(rightside[i])>1:
            for j in range(len(rightside[i])):
                final.append(rightside[i][j])
        else:
            final.append(rightside[i])
    #remove duplicates
    final = list(dict.fromkeys(final))

    return final

def onlyleft(leftlist,rightlist):
    left = []
    for i in range(len(leftlist)):
        if leftlist[i] in rightlist:
            continue
        else:
            left.append(leftlist[i])
    return left

def onlyright(leftlist,rightlist):
    right = []
    for i in range(len(rightlist)):
        if rightlist[i] in leftlist:
            continue
        else:
            right.append(rightlist[i])
    return right


def neitherRightOrLeft(relation,leftNoDupes,rightNoDupes):
    blank = []

    for i in range(len(relation)):
        if (relation[i] not in leftNoDupes) and (relation[i] not in rightNoDupes):
            blank.append(relation[i])

    return blank

#find all elements NOT in combined and right side
def exteriors(combined, right, relation):

    ext =[]
    for i in range(len(relation)):
        if (relation[i] not in combined) and (relation[i] not in right):
            ext.append(relation[i])

    return ext

def closurehelper(funcDepends, totest):

    for key in funcDepends.keys():
        if len(key)>1:
            flag =1
            for i in range(len(key)):
                if key[i] in totest:
                    flag = 1
                else:
                    flag = 0
                    break
        else:
            flag = 1
        if flag ==1:
            totest = totest+funcDepends[key]
        else:
            continue

    return totest



#takes neither + left side + a char to run against func Depends
def closuretest(totest,funcDepends, relation):
    #BC +A and BC +D
    totest = sorted(totest)
    totest = "".join(map(str, totest))

    #todo develop a way to go back to top of func keys on the event a new one is found and added to the list?
    i =0
    while i < len(funcDepends):
        totest = closurehelper(funcDepends,totest)
        i +=1

    #remove dupes
    totest = "".join(set(totest))
    #print("totest at the end", totest)
    if len(totest) == len(relation):
        #print("True")
        return True
    else:
        #print("false")
        return False

    #TODO all elements of new must be in every permutation, however there can be anywhere between 1 and n elements of extern in every permutation.
# Add exterior values to complete keys
def combineExteriors(keyList, exter, funcDepend, relation):
    if (len(exter) != 0):
        finalKeys = []
        for i in exter:
            for j in keyList:
                if (closuretest(i+j, funcDepend, relation)):
                    finalKeys.append(i + j)
    else:
        finalKeys = keyList

    return finalKeys

def main():
    msgbox('Please choose the file which holds the relation and functional dependencies')
    #get the relation and functional dependencies
    relation, funcDepend = relationread()


    #isolate left side
    leftList = leftside(funcDepend, relation)

    #isolate right side
    rightList = rightside(funcDepend,relation)


    #find only leftside
    leftNoDupes = onlyleft(leftList,rightList)
    #print("final left = ",leftNoDupes)

    #findonly rightside
    rightNoDupes = onlyright(leftList,rightList)
    #print("final right =", rightNoDupes)

    #find nither right nor left!
    neither =neitherRightOrLeft(relation,leftList,rightList)
    #print ("neither =" ,neither)
    keyList = []

    new = leftNoDupes+neither
    new = (''.join(map(str, leftNoDupes + neither)))
    #test if combined is a closure if it is, print it and end it all right here!
    if ((closuretest(new, funcDepend, relation)) ==True):
        keyList.append(new)
        print("The candidate key is = ", keyList)
        exit(1)



    #combine the elements of neither and leftnoDupes then find the closures using the relational dependencies
    exter = exteriors(neither+leftNoDupes,rightNoDupes, relation)
    #print ("exteriors = " , exter)


    #TODO deal with the problem of how to create a list of every permutation of "new" + the externs list then test each of them against closuretest
    keyList = combineExteriors(keyList, exter, funcDepend, relation)

    print("The options for candidate keys are: ", keyList)
main()