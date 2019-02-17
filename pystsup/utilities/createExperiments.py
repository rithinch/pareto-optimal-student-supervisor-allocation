"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: utilities
    File: createExperiments.py
    
    Purpose:  Contains Required functions to create and read experiment files, read and update GA config files
              create fitness cache and initial population, and convert string to an operator / function.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""



from .acmParser import getPath, parseFile
from .createRandomData import createRandomData
from pystsup.data import *
from pystsup.evolutionary import *
 

import os
import numpy as np
import glob
import gzip
import json
import random

def read_preference_tsv(path,student=True):
    topicNames,topicPaths,topicIDs,levels = parseFile("pystsup/test/acm.txt")
    f = open(path,"r")
    raw_data = []
    base = "student" if student else "supervisor"
    for line in f :
        fields = [ int(x) for x in line.split("\t") ]
        identifier = base + str(fields[0])
        kw = {}
        for i in range(1,6):
            kw[i] = getPath( topicIDs[ fields[i] + 1 ], topicNames, topicPaths, topicIDs )
        raw_data.append( (identifier, kw ) )
        print(identifier,kw)
    return raw_data

def createExperimentsFromRealData(maxStu,minStu,stepStu,maxSup,minSup,stepSup,scenarios,student_path,supervisor_path,folder="real_experiments",quotaMin=1,quotaMax=1.20,quotaStep=0.05,c=0.5,n=5):
    if not os.path.exists(folder):
        os.mkdir(folder)    
    filenames = []
    rankWeights = Solution.calcRankWeights(c=c,n=n)
    students_raw = read_preference_tsv(student_path)
    supervisors_raw = read_preference_tsv(supervisor_path,student=False)
    for num_students in range(minStu,maxStu+1,stepStu):
        for num_supervisors in range(minSup,maxSup+1,stepSup):
            for total_quota in [int(num_students*i) for i in np.arange(quotaMin,quotaMax+0.01,quotaStep)]: 
                maxQuota = 10
                minQuota = 4
                while num_supervisors*minQuota > total_quota:
                    minQuota -=1
                while num_supervisors*maxQuota < total_quota:
                    maxQuota += 1
                for num_scenarios in range(1,scenarios+1):
                    filename = str(num_students) + "_"+str(num_supervisors)+"_"+ str(total_quota)+"_"+str(num_scenarios)
                    destinationPath = folder+"/"+filename
                    students,supervisors = createRandomData(num_supervisors,num_students,total_quota,level=3,maxQuota=maxQuota,minQuota=minQuota)
                    random.shuffle(students_raw)
                    random.shuffle(supervisors_raw)
                    i = 0
                    for student in students :
                        students[student]._keywords = students_raw[i][1]
                        i = i + 1
                    i = 0
                    for supervisor in supervisors:
                        supervisors[supervisor]._keywords = supervisors_raw[i][1]
                        i = i + 1
                    fitnessCache = calcFitnessCache(students,supervisors,rankWeights)
                    filenames.append(destinationPath)
                    population = {}
                    for i in [128,256,512]: 
                        population[str(i)] = initializePopulation(i,students,supervisors,rankWeights,fitnessCache)
                    createFile(destinationPath,students,supervisors,minQuota,maxQuota,total_quota,num_scenarios,fitnessCache,population,rankWeights)
    return filenames

def createExperiments(maxStu,minStu,stepStu,maxSup,minSup,stepSup,scenarios,folder="experiments",quotaMin=1,quotaMax=1.20,quotaStep=0.05,acmLevel=3,c=0.5,n=5):
    """Function to create experiments""" 
    if not os.path.exists(folder):
        os.mkdir(folder)
    filenames = []
    rankWeights = Solution.calcRankWeights(c=c,n=n)
    for num_students in range(minStu,maxStu+1,stepStu):
        for num_supervisors in range(minSup,maxSup+1,stepSup):
            for total_quota in [int(num_students*i) for i in np.arange(quotaMin,quotaMax+0.01,quotaStep)]:
                maxQuota = 10
                minQuota = 4
                while num_supervisors*minQuota > total_quota:
                    minQuota -=1
                while num_supervisors*maxQuota < total_quota:
                    maxQuota += 1
                for num_scenarios in range(1,scenarios+1):
                    filename = str(num_students) + "_"+str(num_supervisors)+"_"+ str(total_quota)+"_"+str(num_scenarios)
                    
                    destinationPath = folder+"/"+filename
                    
                    students,supervisors = createRandomData(num_supervisors,num_students,total_quota,level=acmLevel,maxQuota=maxQuota,minQuota=minQuota)
                    
                    fitnessCache = calcFitnessCache(students,supervisors,rankWeights)
                    
                    filenames.append(destinationPath)
                    population = {}
                    
                    for i in [128,256,512]:
                        
                        population[str(i)] = initializePopulation(i,students,supervisors,rankWeights,fitnessCache)
                        

                    createFile(destinationPath,students,supervisors,minQuota,maxQuota,total_quota,num_scenarios,fitnessCache,population,rankWeights)
                    

        return filenames


def createFile(filename,students,supervisors,minQuota,maxQuota,quotaSum,testCase,fitnessCache,population,rankWeights):
    """Function to create an exepriment file"""
    
    filename += ".json.gz"
    
    data = {}
    data['numberOfStudents']=len(students)
    data['numberOfSupervisors']=len(supervisors)
    data['testCase']=testCase
    data['quotaSum']=quotaSum
    data['minQuota']=minQuota
    data['maxQuota']=maxQuota
    data['students']=students #serialize
    data['supervisors']=supervisors #serialize
    data['rankWeights'] = rankWeights
    data['fitnessCache']=fitnessCache
    data['population'] = population #contains sub solutions
    
    with gzip.GzipFile(filename,'w') as f:
        json_str = json.dumps(data,default=lambda o: o.__dict__)
        json_bytes = json_str.encode('utf-8')
        f.write(json_bytes)


def saveExpResults(filename,data):
    filename += ".json.gz"

    with gzip.GzipFile(filename,'w') as f:
        json_str = json.dumps(data)
        json_bytes = json_str.encode('utf-8')
        f.write(json_bytes)


def readFile(filename):
    """Function to read an experiment file"""

    with gzip.GzipFile(filename,'r') as f:

        json_bytes = f.read()
        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)


    students = data['students']
    supervisors = data['supervisors']
    fitnessCache = data['fitnessCache']
    rankWeights = data['rankWeights']
    population = data['population']

    details = ['numberOfStudents','numberOfSupervisors','testCase','quotaSum','minQuota','maxQuota']
    expDetails = {k:data[k] for k in details}


    for stu in students:
        new = Student.__new__(Student)
        new.__dict__ = students[stu]
        students[stu] = new

    for sup in supervisors:
        new = Supervisor.__new__(Supervisor)
        new.__dict__ = supervisors[sup]
        supervisors[sup]=new


    for i in population:
        for j in range(int(i)):
            
            new = Solution.__new__(Solution)

            graph = BipartiteGraph.__new__(BipartiteGraph)
            graph.__dict__ = population[i][j]['_graph']
            population[i][j]['_graph']=graph
            
            new.__dict__ = population[i][j]
            
            population[i][j] = new


    return students,supervisors,population,fitnessCache,rankWeights,expDetails
            
            

def parseConfigFile(filename):
    """Function to parse GA config file and return the necessary values for GA Object"""

    f = open(filename,'r')
    data = json.load(f)
    f.close()
    gen = data['genLimit']
    popSize = data['populationSize']
    mutationProbability = data['mutationProbability']
    swapProbability = data['swapProbability']
    transferProbability = data['transferProbability']
    crossoverOp = strToOp(data['crossoverOp'],'crossover')
    mutationOp = strToOp(data['mutationOp'],'mutation')
    selectionOp = strToOp(data['selectionOp'],'selection')

    return gen,popSize,crossoverOp,mutationOp,selectionOp,mutationProbability,swapProbability,transferProbability



def updateConfigFile(filename,genLimit,popSize,muProb,swapProb,transProb):
    """Function to update the GA config file, used in GUI"""

    f = open(filename,'r')
    data = json.load(f)
    f.close()
    
    f = open(filename,'w')
    data['genLimit'] = genLimit
    data['populationSize']=popSize
    data['mutationProbability'] = muProb
    data['swapProbability']=swapProb
    data['transferProbability']=transProb

    json.dump(data,f,indent=4)
    f.close()

def strToOp(name,op):
    """Function to convert a string into a reference to a function and return it"""

    if op=='mutation':

        operator = mutate

    elif op=='crossover':

        if name=='kPoint':

            operator = kPoint
            
        elif name == 'crossover':
            
            operator = crossover

        elif name == 'uniform' :
            operator = uniform

        elif name == 'sp_crossover':
            operator = sp_crossover
        
        elif name == 'crossover6':
            operator = crossover6

    elif op=='selection':

        if name=='tournamentSelection':
            operator = tournamentSelection
        elif name=='rouletteWheel':
            operator = rouletteWheel


    return operator

        
    
def calcFitnessCache(students,supervisors,rankWeights):
    """Function to calculate the fitness cache for set of students and supervisors"""
    fitnessCache = {}
    dummySolution = Solution()
    
    for sup in supervisors:
        supervisorKeywords = supervisors[sup].getKeywords()
        for stu in students:
            studentKeywords = students[stu].getKeywords()
            f_stu, f_sup = dummySolution.kw_similarity(studentKeywords,supervisorKeywords, rankWeights)
            fitnessCache[str((stu,sup))] = (f_stu,f_sup)

    return fitnessCache




def initializePopulation(size,students,supervisors,rankWeights,fitnessCache):
    """Function to initialize Population of a given size"""
    
    population = []
    count = 0
    while count < size:
        new = Solution.generateRandomSolution(students,supervisors)
        new.calcFitness(students,supervisors,rankWeights,fitnessCache)
        population.append(new)
        count+=1

    return population

 

                
    





        
        



            
                            
                        
