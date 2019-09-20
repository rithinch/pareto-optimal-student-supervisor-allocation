"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: utilities
    File: acmParser.py
    
    Purpose:  Contains Required functions to parse the ACM Classfication file and get path of keywords.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""


def parseFile(filename):
    """
    Function to parse the ACM Classification Tree (txt file)

    Parameters:
        filename (string) - the text file which contains the ACM Classification.

    Returns:

        topicNames (dictionary) - the name of the topic as the key and the topic ID number as value.
        topicPaths (dictionary) - the topic ID as the key, and its parent as value.
        topicIDs (dictionary) - the topic ID as the key, and the topic name as the value.
        levels (dictionary) - the topic ID as the key, and the level of that topic in ACM Tree as value.
    """

    f = open(filename, "r")

    tid = 0
    prevTabCount = 0
    parents = []
    
    topicNames = {}
    topicPaths = {}
    topicIDs = {}
    levels = {}
    
    for line in f:
        if line != "\n":
            tid+=1
        
            name = line.strip("\t")
            name= name.strip("\n")
            if name[0] == " ":
                name = name[1:]
        
            tabCount = line.count("\t")

            if tabCount == 0:
                parent = 0
                parents.append(parent) #Add to stack
                
            elif tabCount > prevTabCount:
                parent = tid - 1
                parents.append(parent)
                
            elif tabCount < prevTabCount:
                for i in range(prevTabCount-tabCount):
                    parents.pop() #Remove from stack
                parent = parents[-1]
                
            else:
                parent = parents[-1]
                
            name = name.lower().strip()
            
            topicNames[name] = tid
            topicIDs[tid] = name
            topicPaths[tid] = parent
            levels[tid] = tabCount+1
            
            prevTabCount = tabCount

    f.close()

    return topicNames,topicPaths, topicIDs, levels


def getPath(keyword, topicNames, topicPaths, topicIDs):
    """
    Function to get the path of a particular keyword in ACM Tree.

    Parameters:
        keyword (string) - the keyword for which we want the path.
        topicNames (dictionary) - the name of the topic as the key and the topic ID number as value.
        topicPaths (dictionary) - the topic ID as the key, and its parent as value.
        topicIDs (dictionary) - the topic ID as the key, and the topic name as the value.

    Returns:
        path (list) - the path of that keyword (backwards)
    """
    
    topicId = topicNames[keyword]
    path = [keyword]
    topicParent = topicPaths[topicId]

    #Start from the keyword and backtrack until the first parent.
    while topicParent != 0:
        curr = topicIDs[topicParent]
        path.append(curr)
        topicParent = topicPaths[topicParent]

    return path



