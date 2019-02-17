"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: evolutionary
    File: geneticAlgorithm.py
    
    Purpose:  Contains GeneticAlgorithm class, which is an implementation of NSGA II.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""


import random
from pystsup.data import Solution
import copy
from .metrics import calcSpacing
import time
from pygmo import hypervolume

class GeneticAlgorithm:

    def __init__(self,students,supervisors,fitnessCache,rankWeights,mutationOp,crossoverOp,selectionOp,mutation=True,crossover=True):
        """
        Initialize the GeneticAlgorithm object.

        Parameters:
        
            students - dictionary of all students with their details (id, preferences)
            supervisors - dictionary of all supervisors with their details (id,preferences,quota)
            fitnessCache(dictionary) - with a student-supervisor pair as key and their keyword similairty score as value.
            rankWeights (dictionary) - with rank as key and its weight as value.
            mutationOp (Function) - the mutation operator to use.
            crossoverOp (Function) - the crossover operator to use.
            selectionOp (Function) - the selection operator to use.
            
        """
        
        self.supervisors = supervisors
        self.students = students
        self._mutate = mutationOp
        self._crossover = crossoverOp
        self._selection = selectionOp
        self.fitnessCache = fitnessCache
        self.rankWeights = rankWeights
        self._mutation_flag = mutation
        self._crossover_flag = crossover


    def initializePopulation(self,size):
        """
        Function to create a pool of random solutions of a given size.
        Used in the begining of the GA run to create intial population.

        Parameters:
            size (int) - the size of the population.

        Returns:

            population (list) - list containing 'n' randomly created Solution Objects, where n is the specified size.
        """

        population = []
        
        count = 0
        while count < size:
            #Generate random solution, calculate and set Fst and Fsup values, then append to population list until its of the size we want.

            new = Solution.generateRandomSolution(self.students,self.supervisors)
            new.calcFitness(self.students,self.supervisors,self.rankWeights,self.fitnessCache)
            population.append(new)
            count+=1
        return population


    def mutation(self,population,mutationProbability,swapProbability,transferProbability):
        """
        Function to perform the mutation operator on a given population.
        This function mutates all the solutions in the given population.

        Parameters:

            population (list) - list of solutions to mutate.
            mutationProbability (float) - the probability of mutating an edge.
            swapProbability (float) - the probability of doing a swap on a mutating edge.
            transferProbability (float) - the probability of doing a transfer on a mutating edge.

        Returns:

            newSolutions (list) - list of mutated solutions. Same size as the given population.
        """

        newSolutions = []

        for solution in population:

            #Mutate solution, calculate and set Fst and Fsup values, then append to new solutions list.
            
            new = self._mutate(solution,self.supervisors,mutationProbability,swapProbability,transferProbability)
            new.calcFitness(self.students,self.supervisors,self.rankWeights,self.fitnessCache)
            newSolutions.append(new)
                               
        return newSolutions


    def crossover(self,population,k=None):
        """
        Function to perform the crossover operator on a given population.

        Parameters:

            population (list of tuples) - list of tuples containing a pair of solution objects.
            k (int) - the value of 'k' in case of K-Point crossover. (Used only for experiments)

        Returns:

            newSolutions (list) - list of crossover-ed solutions.
        """
        
        newSolutions = []

        for parents in population:
            
            sol1 = parents[0]
            sol2 = parents[1]

            #Crossover Solutions, calculate and set Fst and Fsup values, then append to new solutions list.
            
            new = self._crossover(sol1,sol2,self.supervisors,self.students,k)
            new.calcFitness(self.students,self.supervisors,self.rankWeights,self.fitnessCache)
            newSolutions.append(new)
            

        return newSolutions


    def makeNewPopulation(self,population,size,mutationProbability,swapProbability,transferProbability,k=None):
        """
        Function to make new population of crossover-ed and mutated solutions (offsprings) from given population.

        Parameters:

            population (list) - list of parent solutions.
            size (int) - the population size set for the GA run.
            mutationProbability (float) - the probability of mutating an edge.
            swapProbability (float) - the probability of doing a swap on a mutating edge.
            transferProbability (float) - the probability of doing a transfer on a mutating edge.
            k (int) - the value of 'k' in case of K-Point crossover. (Used only for experiments)

        Returns:

            newSolutions (list) - list of children solutions (offsprings)
        """
        
        newPopulation = [] #offspring population

        #Get the mutated solutions
        
        mutatedSolutions = self.mutation(population,mutationProbability,swapProbability,transferProbability) if self._mutation_flag else []

        #Select parents for crossover using selection operator
        
        crossoverPop = self._selection(population,size)

        #crossover the selected parents
        
        crossoverSolutions = self.crossover(crossoverPop,k) if self._crossover_flag else []


        #combine both mutated and crossover-ed solution to create an offspring population
        
        newPopulation.extend(mutatedSolutions)
        newPopulation.extend(crossoverSolutions)
        
        return newPopulation



    def fast_non_dominated_sort(self,population):
        """
        Function to divide the population into fronts using the fast non dominated sort approach of NSGA II.

        Parameters:

            population (list) - list of solutions to be sorted into fronts.

        Returns:

            fronts (list) - list of lists, each list representing a front. Non domintated solutions are always in the first front (index 0).
        """
        
        fronts = [[]]
        
        for solution1 in population:

            solution1.dominatedSolutions = [] 
            solution1.dominationCount = 0
            
            for solution2 in population:
                if solution1.dominates(solution2):
                    solution1.dominatedSolutions.append(solution2)
                elif solution2.dominates(solution1):
                    solution1.dominationCount +=1
         
            if solution1.dominationCount == 0:

                solution1.rank = 0 #In the first front
                fronts[0].append(solution1)

        i = 0

        while len(fronts[i]) != 0:

            nextFront = []

            for solution1 in fronts[i]:

                for solution2 in solution1.dominatedSolutions:

                    solution2.dominationCount -= 1

                    if solution2.dominationCount == 0:

                        solution2.rank = i + 1
                        nextFront.append(solution2)

            i+=1
            fronts.append(nextFront)
        
        return fronts


    def crowding_distance_assignment(self,front,maxFst,minFst,maxFsup,minFsup):
        """
        Function to calculate the crowding distance values of solutions in a given front into using the crowding distance assignment of NSGA II.

        Parameters:

            front (list) - list of solutions in the front.
            

        Returns:

            fronts (list) - list of lists, each list representing a front. Non domintated solutions are always in the first front (index 0).
        """

        lenFront = len(front)

        if lenFront == 0:
            return

        for sol in front:
            sol.crowdingDistance = 0


        sortedFst = sorted(front, key=lambda x: x.getFst())
        sortedFsup = sorted(front,key=lambda x: x.getFsup())
        
        sortedFst[0].crowdingDistance = float("inf")
        sortedFst[-1].crowdingDistance = float("inf")
        sortedFsup[0].crowdingDistance = float("inf")
        sortedFsup[-1].crowdingDistance = float("inf")


        for index in range(1,lenFront-1):
            sortedFst[index].crowdingDistance += (sortedFst[index+1].getFst() - sortedFst[index-1].getFst())/(maxFst - minFst)
            
            
        for index in range(1,lenFront-1):
            sortedFsup[index].crowdingDistance += (sortedFsup[index+1].getFsup() - sortedFsup[index-1].getFsup())/(maxFsup - minFsup)
            



    def crowded_comparision_operator(self,solution1,solution2):
        """
        Implementation of NSGA II crowded comparision operator.
        This is to compare if a solution is better than another in terms of its position in front and crowding distance.
        Used in NSGA II when sorting the solutions of the last front.
        This function is also implemented as a "__lt__"  for Solution Class, so that it is easier to sort and compare.
        Note that this method is not called anywhere. "__lt__" method for Solution class is being used instead.
        
        Parameters:
        
            solution1 (Solution) - the solution comparing to.
            solution2 (Solution) - the solution comparing with.

        Returns:
        
            A Boolean - True if solution1 is better than solution2. Otherwise, False.
        """
        
        cond1 = solution1.rank < solution2.rank
        cond2 = (solution1.rank == solution2.rank) and (solution1.crowdingDistance > solution2.crowdingDistance)

        if cond1 or cond2:
            return True
        else:
            return False



    def filterPopulation(self,population,size):
        """
        Function to filter the population by keeping only the unique solutions as much as possible.
        

        Parameters:

            population (list) - list of solutions.
            size (int) - the population size set for the GA run.

        Returns:

            newSolutions (list) - list of children solutions (offsprings)
        """
        
        s = []

        seen = set()
        repeating = []

        for i in population:
            if i not in seen:
                s.append(i)
                seen.add(i)
            else:
                repeating.append(i)

        currFront = 0

        repeating = sorted(repeating,key=lambda x: x.rank)

        required = size - len(s)

        s.extend(repeating[:required])

        return s

    def SMetric(pareto_frontier,reference_point=(1,1)):
        hv = hypervolume(sorted(pareto_frontier,reverse=True))
        return hv.compute(reference_point)


   

    def start(self,popSize,genLimit,mutationProbability,swapProbability,transferProbability,population=None,k=None):
        """
        Function to start the GA run.

        Parameters:

            popSize (int) - population size to start the GA with.
            genLimit (int) - the stopping criteria; the number iterations till the same front (until converged)
            mutationProbability (float) - the probability of mutating an edge.
            swapProbability (float) - the probability of doing a swap on a mutating edge.
            transferProbability (float) - the probability of doing a transfer on a mutating edge.
            population (list) - Optional. Can pass a population to start GA (Used in experiments)
            k (int) - the value of 'k' in case of K-Point crossover. (Used only for experiments)

        Returns:

            metricData (dictionary) - dictionary containing all the metric data associated with the GA run.
            front - the non dominated solutions after the GA run (Pareto Optimal Frontier; the first front.)
            
        """
        
        #Initialize the population
        
        if not population:
            population = self.initializePopulation(popSize)

        tic1 = time.time()
        
        fronts = self.fast_non_dominated_sort(population)
        
        best_hv = float("inf")
        best_front = None
        hv = GeneticAlgorithm.SMetric( [ (x.getFst(),x.getFsup()) for x in  fronts[0] ] )
        no_impr = 0

        
        toc1 = time.time() - tic1
        
        offsprings = []
        
        count = 0
        genCount = 0
        prev = set()

        metricData = {}

        #Metrics Data
        
        initial_maxFst = max(population, key=lambda x: x.getFst()).getFst()
        initial_minFst = min(population, key=lambda x: x.getFst()).getFst()
        initial_maxFsup = max(population, key=lambda x: x.getFsup()).getFsup()
        initial_minFsup = min(population, key=lambda x: x.getFsup()).getFsup()

        evolution_front = []

        tic1 = time.time()
        
        while ( no_impr <= 20 ):

            print("Generation " + str(genCount) + " no improvement in " + str(no_impr))

            #Combine parent and offspring population
            
            population.extend(offsprings)


            #Divide the population into fronts
            
            fronts = self.fast_non_dominated_sort(population)
            hv = GeneticAlgorithm.SMetric( [ (x.getFst(),x.getFsup()) for x in  fronts[0] ] )
            if hv >= best_hv :
                no_impr = no_impr + 1
            else :
                no_impr = 0
                best_hv = hv
                best_front = fronts[0]

            maxFst = max(population, key=lambda x: x.getFst()).getFst()
            minFst = min(population, key=lambda x: x.getFst()).getFst()

            maxFsup = max(population, key=lambda x: x.getFsup()).getFsup()
            minFsup = min(population, key=lambda x: x.getFsup()).getFsup()

            newPopulation = []
            frontCount = 0

            evolution_front.append( sorted([ (x.getFst(),x.getFsup()) for x in fronts[0] ]) )

            #Until inclusion possible, calculate the crowding distance and add to new population
            while len(newPopulation) + len(fronts[frontCount]) <= popSize:
                
                self.crowding_distance_assignment(fronts[frontCount],maxFst,minFst,maxFsup,minFsup)
                newPopulation.extend(fronts[frontCount])
                frontCount+=1
                if frontCount == len(fronts):
                    break

            
            #Select the required amount of solutions from the last non-visted front to fill the population to the specified size
            if len(newPopulation) != popSize:
                
                self.crowding_distance_assignment(fronts[frontCount],maxFst,minFst,maxFsup,minFsup)
                
                fronts[frontCount] = sorted(fronts[frontCount]) 
                
                needed = popSize - len(newPopulation)
                newPopulation.extend(fronts[frontCount][:needed])

            population = newPopulation


            #Filter population to keep as much unique solutions as possible

            filteredPop = self.filterPopulation(population,popSize)

            #Make offspring population from the filtered population
            offsprings = self.makeNewPopulation(filteredPop,popSize,mutationProbability,swapProbability,transferProbability,k)

            #Checking if solutions in frontier are the same as previous. If the same for 10 times, then the GA run stops.
            
            curr = set([(i._Fst,i._Fsup) for i in fronts[0]])
               
            
            if len(curr - prev) != 0:
                count=0
                prev = copy.deepcopy(curr)
            else:
                count+=1
            
            genCount+=1
            

        toc1 += time.time() - tic1

        #Adding Metrics Data

        
        final_maxFst = maxFst
        final_maxFsup = maxFsup
        final_minFst = minFst
        final_minFsup = minFsup

        metricData['initial_maxFst']=initial_maxFst
        metricData['initial_minFst']=initial_minFst
        metricData['initial_maxFsup']=initial_maxFsup
        metricData['initial_minFsup']=initial_minFsup

        metricData['final_maxFst']=final_maxFst
        metricData['final_minFst']=final_minFst
        metricData['final_maxFsup']=final_maxFsup
        metricData['final_minFsup']=final_minFsup

        metricData['evolution'] = evolution_front
        metricData['diversity'] = calcSpacing(best_front)

        metricData['numberOfGenerations'] = genCount
        metricData['non_dominated_solutions'] = set([(i._Fst,i._Fsup) for i in best_front])
        
        metricData['total_time_generations'] = toc1
        metricData['avg_time_generation'] = toc1/genCount
        
        
        print("GA Run Finished..")

        
        return metricData,best_front




