"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: evolutionary/mutation
    File: mutation.py
    
    Purpose:  Contains the mutation opearators.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""


import random
from pystsup.data import Solution
import copy


def mutate(solution,supervisors,probability,swapProbability,transferProbability):
    """
        Function to perform the mutation operator on a solution.

        Parameters:

            solution (Solution) - the solution we want to mutate.
            supervisors (dictionary) - dictionary of all supervisors with their details (id,preferences,quota)
            probability (float) - the probability of mutating an edge.
            swapProbability (float) - the probability of doing a swap on a mutating edge.
            transferProbability (float) - the probability of doing a transfer on a mutating edge.

        Returns:

            newSolutions (list) - list of mutated solutions. Same size as the given population.
        """

    #Make a copy of the solution graph
    graph = solution.getGraph().copy()

    #Get the list of supervisors to and from whom we can transfer
    canTransferFrom, canTransferTo = solution.getTransferable(supervisors)

    supEdges = copy.deepcopy(graph.getEdges())
    stuEdges = copy.deepcopy(graph.getStuEdges())
    
    allStudents = set(list(stuEdges.keys()))
    allSupervisors = set(list(supEdges.keys()))
    
    probSum = swapProbability + transferProbability
    swapProbability = swapProbability/probSum
    transferProbability = transferProbability/probSum
    
    count=0
    
    for sup in supEdges:
            
        for stu in supEdges[sup]:

            if graph.isEdge(sup,stu):
                
                n = random.random()

                if n<=probability:
                    
                    count+=1
                    
                    m = random.random()

                    if m <= transferProbability and (graph.getSupervisorDegree(sup) > 1) and not(len(canTransferTo)==1 and (sup in canTransferTo)) and len(canTransferTo)>0:
                        #Perform Transfer Operation
                        
                        if sup in canTransferTo:
                            canTransferTo.remove(sup)
                            
                        
                        toSup = random.choice(list(canTransferTo))
                        
                        graph.transferStudent1(stu,sup,toSup,supervisors)

                        
                        canTransferTo.add(sup)
                        
                        if not(graph.getSupervisorDegree(toSup) < supervisors[toSup].getQuota()):
                            canTransferTo.remove(toSup)
                        

                    else:

                        #Peform Swap Operation

                        allSupervisors.remove(sup)
                    
                        sup2 = random.choice(list(allSupervisors))
                    
                        stu2 = random.choice(graph.getStudents(sup2))
                    
                        graph.swapStudents(stu,sup,stu2,sup2)

                        allSupervisors.add(sup)


    return Solution(graph)




                    

            
    
    
