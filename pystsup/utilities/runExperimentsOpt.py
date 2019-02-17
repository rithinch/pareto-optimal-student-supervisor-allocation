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
import math
from pyomo.environ import *
from pyomo.opt import SolverFactory

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

def createGAMSFileSup(filename,output,maxVersion=True):
 
    #Getting the experiments files


    students,supervisors,populations,fitnessCache,rankWeights,expDetails = readFile(filename)

    f = open(output, "w" )
    f.write("$offdigit\n")
    f.write( "Sets\n" )
    f.write( "\ti\tstudents\t/ ")
    l_students = ",".join( list(students.keys()) )
    f.write( l_students + "/\n")
    f.write( "\tj\tsupervisors\t/ ")
    l_supervisors = ",".join(list(supervisors.keys()))
    f.write( l_supervisors + "/;\n" )

    f.write("Parameters\n")
    f.write("c(j)\tcapacity of supervisor\n")
    f.write("\t/ ")
    for supervisor in supervisors:
        f.write( "\t" + str(supervisor) + "\t" + str(supervisors[supervisor].getQuota()) + "\n" )
    f.write(" / ;\n")

    f.write("Table v(i,j) valuation of being assigned i to j\n")
    f.write("$onDelim\n")
    f.write(",")
    l_supervisors = ",".join( list(supervisors.keys()) )
    f.write(l_supervisors + "\n")
    for student in students :
        f.write(str(student))
        for supervisor in supervisors:
            f.write("," + str( fitnessCache[str((student,supervisor))][1] ) )
        f.write("\n")
    f.write("$offDelim\n")
    f.write(";\n")

    f.write( "Scalar n_students number of students /" + str(len(students)) + "/;\n")
    f.write( "Scalar n_supervisors number of supervisors /" + str(len(supervisors)) + "/;\n")

    f.write("Variables\n")
    f.write("\tx(i,j) if student is assigned to supervisor \n")
    f.write("\tq(j) quality of allocation to supervisor j \n")
    f.write("\twl(j) workload of allocation for supervisor j\n")
    f.write("avg_wl average workload of allocation\n")
    f.write("\tz total quality of matching ;\n")
    f.write("Binary variables x ;\n")

    f.write("Equations\n")
    f.write("\tquality\tdefine objective function\n")
    f.write("\tworkload(j) workload of allocation for supervisor j\n")
    f.write("average_workload average workload of allocation\n")
    f.write("\tsup_quality(j)   quality of matching for supervisor j\n")
    f.write("\tmin_sup(j) minimum supervision quota for supervisor j\n")
    f.write("\tmax_sup(j) maximum supervision quota for supervisor j\n")
    f.write("\tstu_alloc(i) ensures that the student is allocated to someone ;\n")

    f.write("sup_quality(j) ..\t q(j) =e= sum(i, v(i,j)*x(i,j))/sum(i,x(i,j)) ;\n")
    f.write("workload(j) ..\t wl(j) =e= sum(i,x(i,j))/c(j) ;\n")
    f.write("average_workload ..\t avg_wl =e= (1/n_supervisors) * sum(j,wl(j)) ;\n")
    f.write("quality ..\t z =e= (1/ (1+sqrt((1/n_supervisors) * sum(j, power(avg_wl-wl(j),2) )))**2 ) *  (1/n_supervisors) * sum(j,q(j)) ;\n")
    f.write("min_sup(j) .. sum(i, x(i,j)) =G= 1 ;\n")
    f.write("max_sup(j) .. sum(i, x(i,j)) =L= c(j) ;\n")
    f.write("stu_alloc(i) .. sum(j,x(i,j)) =e= 1 ;\n")
    f.write("Model project_alloc /all/ ;\n")

    rsol = Solution.generateRandomSolution(students,supervisors)
    g = rsol.getGraph()

    for student in students :
        for supervisor in supervisors :
            if g.isEdge(supervisor,student) :
                f.write("x.L(\""+str(student)+"\",\"" + str(supervisor)+"\") = 1;\n");
            else :
                f.write("x.L(\""+str(student)+"\",\"" + str(supervisor)+"\") = 0;\n");


    f.write("Solve project_alloc using MINLP maximizing z ;")



    f.close()
    return students,supervisors,populations,fitnessCache,rankWeights,expDetails 

def runExperimentsOpt(filename,studentVersion=True,maxVersion=True):

    #Getting the experiments files


    students,supervisors,populations,fitnessCache,rankWeights,expDetails = readFile(filename)

    model = ConcreteModel()

    n_stu = len(students)
    n_sup = len(supervisors)

    model.students = Set( initialize=[student for student in students], doc="Student population" )
    model.supervisors = Set( initialize=[supervisor for supervisor in supervisors], doc="Supervisor population" )

    model.capacity = Param( model.supervisors, initialize= { s: supervisors[s].getQuota() for s in supervisors }, doc = "Supervisor quotas" )

    idx_valuation = 0 if studentVersion else 1
    valuations = {}

    for student in students :
        for supervisor in supervisors :
            valuations[ (student,supervisor) ] = fitnessCache[str((student,supervisor))][idx_valuation]

    model.valuations = Param( model.students, model.supervisors, initialize=valuations, doc="Values given to being assigned")

    model.n_students = Param(initialize=n_stu)
    model.n_supervisors = Param(initialize=n_sup)

    # Defining variables
    model.x = Var(model.students, model.supervisors, domain=Boolean, doc="Variables")

    def student_constraint(model, st):
        return sum( model.x[st,j] for j in model.supervisors ) == 1

    def minimum_quota(model,sup):
        return sum( model.x[i,sup] for i in model.students ) >= 1

    def maximum_quota(model,sup):
        return sum( model.x[i,sup] for i in model.students ) <= model.capacity[sup]
    
    # Defining constraints
    model.student_c = Constraint(model.students, rule=student_constraint, doc ="Student constraints, so that they are supervised by only one" )
    model.sup_min_c = Constraint(model.supervisors, rule=minimum_quota, doc = "Minimum quota constraint" )
    model.sup_max_c = Constraint(model.supervisors, rule=maximum_quota, doc = "Maximum quota constraint" )

    if studentVersion : 
        def objective_rule(model) :
            return sum( [ 1/model.n_students * model.valuations[i,j] * model.x[i,j] for i in model.students for j in model.supervisors ] )
    else :
        def objective_rule(model) :
            e = None
            for supervisor in model.supervisors :
                s = sum( [ 1/model.n_supervisors  * model.valuations[i,supervisor] * model.x[i,supervisor]  for i in model.students ] )/sum( model.x[i,supervisor] for i in model.students )
                if e is None :
                    e = s
                else :
                    e = e + s
            wl = None
            for supervisor in model.supervisors :
                w = sum( model.x[i,supervisor] for i in model.students  )/model.capacity[supervisor]
                if wl is None :
                    wl = w
                else :
                    wl = wl + w
            avg_wl = wl * 1/model.n_supervisors
            penalization = None
            for supervisor in model.supervisors :
                p = (sum(model.x[i,supervisor] for i in model.students)/model.capacity[supervisor] - avg_wl) * (sum(model.x[i,supervisor] for i in model.students)/model.capacity[supervisor] - avg_wl)
                penalization = p if penalization is None else penalization + p
            penalization = sqrt(penalization/model.n_supervisors)
            #return e * 1/(1 + penalization)**2
            return e/(1+penalization)**2
    model.objective = Objective(rule=objective_rule, sense=maximize if maxVersion else minimize, doc="Objective function" )

    # Setting initial solution
    rsol = Solution.generateRandomSolution(students,supervisors)
    g = rsol.getGraph()

    for student in students :
        for supervisor in supervisors :
            if g.isEdge(supervisor,student) :
                model.x[ student, supervisor ].set_value( 1 )
            else :
                model.x[ student, supervisor ].set_value( 0 )

    rsol.calcFitness(students,supervisors,rankWeights,fitnessCache)

    opt = None
    if studentVersion:
        opt = SolverFactory("glpk")
    else :
        opt = SolverFactory("couenne")
    
    result = opt.solve(model)
    #return model, result, opt
    return expDetails, result[ "Problem" ][0]["Lower bound"],result["Problem"][0]["Upper bound"]

def runAllExperimentsOptStudent(foldername):

    print("numberOfStudents\tnumberOfSupervisors\tquotaSum\ttestCase\tlowerBound\tupperBound")
    filenames = getExperimentFiles(foldername)

    for name in filenames :
        expDetails,aux,ub = runExperimentsOpt(name)
        expDetails,lb,aux = runExperimentsOpt(name,maxVersion=False)
        print(str(expDetails["numberOfStudents"]) + "\t" + str(expDetails["numberOfSupervisors"]) + "\t" + str(expDetails["quotaSum"]) +
                "\t" + str(expDetails["testCase"]) + "\t" + str(lb) + "\t" + str(ub) )



