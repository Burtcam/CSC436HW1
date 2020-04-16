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

#todo
'''
# don't touch... not sure if needed but we'll talk about it when the rest of the group looks at it?
def checkwhatcanbemade(key, funcDepend):
    #loop through key, call each on funcDepend, if found, add to key and call the value on funcDepend until an element in Key already is found
    for i in range(len(key)):
        #Todo bug fix here. This will throw an error in the event of a compound key being provided.
        #if compound key, check if both elements are in the key
        if len(key[i] >1):
            flag = 1
            for j in range(len(key[i])):
                if key[j] not in key:
                    flag = 0
                    break
        ##if all elements of compound key in keylist then we can find all of the values of the compound key
       # if flag == 1:

        key.append(funcDepend[key[i]])
        temp = funcDepend[key[i]]
        ##KEEP GOING UNTIL result of funcDepend[key[i] is not in funcDepend.values()
        while temp in funcDepend:
            temp = funcDepend[temp]
            key.append(temp)

    return key


#call each element of key list on dict. Add the result to found list O(n) for loop, O(1) for each dict call
# #found = checkwhatcanbemade(copy.deepcopy(key), funcDepend)
#TODO loop through funcDepend keys and check that using those keys, you can find ALL members of relation. If not, add what is needed to find that
def checkrevised(keylist, funcDepend):

    return 0
    ##loop through funcDepend values,
    
'''


#check which elements of relation are not on right side of dict O(n) put them in Key list (values) of dict
def onlyleftsidecrap(funcDepend, relation):
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

#takes neither + left side + a char to run against func Depends
def closuretest(totest,funcDepends, relation):
    #BC +A and BC +D
    totest = sorted(totest)
    totest = "".join(map(str, totest))

    for key in funcDepends.keys():
        if key in totest:
            totest = totest + funcDepends[key]

    #remove dupes
    totest = "".join(set(totest))
    if len(totest) == len(relation):
        return True
    else:
        return False

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
    print("final left = ",leftNoDupes)

    #findonly rightside
    rightNoDupes = onlyright(leftList,rightList)
    print("final right =", rightNoDupes)

    #find nither right nor left!
    neither =neitherRightOrLeft(relation,leftList,rightList)
    print (neither)


    #combine the elements of neither and leftnoDupes then find the closures using the relational dependencies
    exter = exteriors(neither+leftNoDupes,rightNoDupes, relation)
    print ("exteriors = " , exter)

    #test closures of combined + each element of exteriors TODO
    new = neither+leftNoDupes
    new.append("")
    print("test new = ", new)


    print(closuretest(new,funcDepend,relation))


main()