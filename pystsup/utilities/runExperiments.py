"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: utilities
    File: runExperiments.py
    
    Purpose:  Contains Required functions to read experiments config file, run experiment files and save the results.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""


from .createExperiments import readFile,strToOp
from pystsup.data import *
from pystsup.evolutionary import *
import sys
import numpy as np
import os
import glob
import json


def parseExpConfig(filename):

    f = open(filename,'r')
    data = json.load(f)
    f.close()

    return data


def toString(identifier,testname,metricData):

    seq = [metricData['initial_maxFst'],metricData['initial_minFst'],metricData['initial_maxFsup'],metricData['initial_minFsup'],metricData['final_maxFst'],metricData['final_minFst'],
           metricData['final_maxFsup'],metricData['final_minFsup']]

    seq2 = [metricData['diversity'],metricData['numberOfGenerations'],metricData['total_time_generations'],metricData['avg_time_generation']]
    

    seq.extend(seq2)

    points = list(map(str,metricData['non_dominated_solutions']))

    point_evolution = str(metricData['evolution'])
    
    data = list(map(str,seq))

    result = identifier + testname + "\t" + "\t".join(data)

    result += "\t" + ",".join(points) + "\t" + point_evolution

    return result


def getExperimentFiles(foldername):
    path = foldername + "/"+"*.gz"
    filenames = glob.glob(path)
    return filenames


def saveResults(results,filename):

    filename += ".tsv"
    
    f = open(filename,'a')

    for line in results:
        f.write(line+"\n")

    f.close()


def writeResult(result,filename,mode='a'):

    filename += ".tsv"

    
    f = open(filename,mode)
    

    f.write(result+"\n")
    f.close()


def runExperiments(configFile,experimentsFolder,outputName):

    
    data = parseExpConfig(configFile)

    genLimit = data['genLimit']
    populationSizes = data['populationSizes']
    mutationProbabilities = list(np.arange(data['min_MutationProbability'],data['max_MutationProbability']+0.01,data['step_MutationProbability']))
    swapProbabilities = list(np.arange(data['min_SwapProbability'],data['max_SwapProbability']+0.01,data['step_SwapProbability']))

    muOp = strToOp(data['mutationOp'],'mutation')
    crossoverOperators = data['crossoverOp']
    selOp = strToOp(data['selectionOp'],'selection')

    k_values = data['k_values']


    #Getting the experiments files

    files = getExperimentFiles(experimentsFolder)


    #Running the experiments

    headings = ['numberOfStudents','numberOfSupervisors','quotaSum','testCase','popSize','mutProb','swapProb','crossoverOp','kValue','initial_maxFst','initial_minFst',
                'initial_maxFsup','initial_minFsup','final_maxFst','final_minFst','final_maxFsup','final_minFsup','diversity','numberOfGenerations','total_time_generations',
                'avg_time_generation',
                'non_dominated_solutions','evolution']

    writeResult("\t".join(headings),outputName,mode='w')

    

    for filename in files:

        print(filename)

        students,supervisors,populations,fitnessCache,rankWeights,expDetails = readFile(filename)

        identifier = str(expDetails['numberOfStudents']) + "\t" + str(expDetails['numberOfSupervisors']) + "\t" + str(expDetails['quotaSum']) + "\t" + str(expDetails['testCase']) + "\t"
    
        for popSize in populationSizes:

            population = populations[str(popSize)]
        
            for mutProb in mutationProbabilities:

                for swapProb in swapProbabilities:

                    transferProb = 1 - swapProb

                    for crossoverOp in crossoverOperators:

                        if crossoverOp == 'crossover' or crossoverOp == 'uniform' or crossoverOp == 'sp_crossover' or crossoverOp == 'none':

                            testname = str(popSize) + "\t" + str(mutProb) + "\t" + str(swapProb) + "\t" + crossoverOp + "\t" + str(-1)

                            crOp = strToOp(crossoverOp,'crossover') if crossoverOp != 'none' else None
                            crossover_flag = False if crossoverOp == 'none' else True

                            geneticAlgorithm = GeneticAlgorithm(students,supervisors,fitnessCache,rankWeights,muOp,crOp,selOp,crossover=crossover_flag)
                        
                            (metricData,solutions) = geneticAlgorithm.start(popSize,genLimit,mutProb,swapProb,transferProb,population)
                            
                            string = toString(identifier,testname,metricData)

                            writeResult(string,outputName)
                            
                       
                        
                        elif crossoverOp == 'kPoint':

                            crOp = strToOp(crossoverOp,'crossover')

                            for kVal in k_values:

                                testname = str(popSize) + "\t" + str(mutProb) + "\t" + str(swapProb) + "\t" + crossoverOp + "\t" + str(kVal)

                                geneticAlgorithm = GeneticAlgorithm(students,supervisors,fitnessCache,rankWeights,muOp,crOp,selOp)

                                (metricData,solutions) = geneticAlgorithm.start(popSize,genLimit,mutProb,swapProb,transferProb,population,kVal)

                                string = toString(identifier,testname,metricData)

                                writeResult(string,outputName)
                                


