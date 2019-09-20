"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: utilities
    File: createRandomData.py
    
    Purpose:  Contains Required functions to create random students and supervisor data.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""



import random
from .acmParser import getPath, parseFile
from .integerPartition import partition
from pystsup.data import Student
from pystsup.data import Supervisor
import numpy

def createRandomData(m,n,quotaSum,level=3,maxQuota=10,minQuota=4,no_topics=5):
    """
    Function to create random students and supervisors data.

    Parameters:
    
        m (int) - the number of supervisors.
        n (int) - the number of students.
        quotaSum (int) - the sum of all the supervisor quota's
        level (int) - the level of topics upto to be given to the students and supervisors.
        maxQuota (int) - the maximum quota possible for a supervisor.
        minQuota (int) - the minimum quota possible for a supervisor.
        no_topics (int) - the number of topics per student/supervisor.

    Returns:
    
        students (dictionary) - dictionary of all students with their details (id, preferences)
        supervisors (dictionary) - dictionary of all supervisors with their details (id,preferences,quota)
    """

    
    topicNames,topicPaths,topicIDs,levels = parseFile("pystsup/test/acm.txt")

    numberOfSupervisors = m
    numberOfStudents = n
    
    supervisors = {}
    students = {}

    supId = "supervisor"
    stuId = "student" 

    #Integer partition problem
    quotas = partition(quotaSum,m,minQuota,maxQuota)

    #Available Topics by Levels
    topicsAvailable = [i for i in levels if levels[i]<=level]
        
    while m > 0:
        m -= 1
        toAdd = []
        sup_List = {}
        rank = 0
        
        for i in random.sample(topicsAvailable,no_topics):
            kw = topicIDs[i]
            rank+=1
            sup_List[rank]=[kw,getPath(kw,topicNames, topicPaths, topicIDs)]

        sup = supId + str(numberOfSupervisors - m)
    
        quota = random.choice(quotas)
        quotas.remove(quota)

        SupervisorObject = Supervisor(sup,sup_List,quota)
        
        supervisors[sup] = SupervisorObject


    while n > 0:
        n-=1
        toAdd = []
        stu_List = {}
        rank = 0
        for i in random.sample(topicsAvailable,no_topics):
            kw = topicIDs[i]
            rank+=1
            stu_List[rank] = [kw,getPath(kw,topicNames, topicPaths, topicIDs)]

        stu = stuId + str(numberOfStudents-n)

        studentObject = Student(stu,stu_List)

        students[stu]=studentObject


    return students,supervisors



def createRandomDataExcel(m,n,quotaSum,level=3,maxQuota=10,minQuota=4,no_topics=5, keywordsFile="pystsup/test/acm.txt"):
    """
    Function to create random students and supervisors data.

    Parameters:
    
        m (int) - the number of supervisors.
        n (int) - the number of students.
        quotaSum (int) - the sum of all the supervisor quota's
        level (int) - the level of topics upto to be given to the students and supervisors.
        maxQuota (int) - the maximum quota possible for a supervisor.
        minQuota (int) - the minimum quota possible for a supervisor.
        no_topics (int) - the number of topics per student/supervisor.

    Returns:
    
        students (list) - list of tuples that represent each row in the students data file.
        supervisors (dictionary) - list of tuples that represent each row in the supervisors data file.
    """

    topicNames,topicPaths,topicIDs,levels = parseFile(keywordsFile)

    numberOfSupervisors = m
    numberOfStudents = n
    
    supervisors = []
    students = []

    suprealID = "aab"
    

    #Integer partition problem
    quotas = partition(quotaSum,m,minQuota,maxQuota)

    f = open('random_names.txt','r').read()
    names = f.split("\n")
    

    #Available Topics by Levels
    topicsAvailable = [i for i in levels if levels[i]<=level]
        
    while m > 0:
        m -= 1
        
        
        realID = suprealID + str(random.randint(2333,9999))
        name = random.choice(names)
        quota = random.choice(quotas)
        quotas.remove(quota)

        toAdd = [realID,name,quota]
        
        for i in random.sample(topicsAvailable,no_topics):
            kw = topicIDs[i]
            toAdd.append(kw.upper())

        supervisors.append(tuple(toAdd))
        

    while n > 0:
        n-=1
        

        realID = str(random.randint(1000000,9999999))
        name = random.choice(names)
        toAdd = [realID,name]
                     
        for i in random.sample(topicsAvailable,no_topics):
            kw = topicIDs[i]
            
            toAdd.append(kw.upper())

        students.append(tuple(toAdd))

        

    return students,supervisors



