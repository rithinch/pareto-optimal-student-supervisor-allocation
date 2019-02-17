"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: test
    File: test_geneticAlgorithm.py
    
    Purpose:  Unit Testing for Genetic Algorithm Class.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""



from pystsup.evolutionary.crossover import crossover
from pystsup.evolutionary.selection import tournamentSelection
from pystsup.evolutionary.mutation import mutate
from pystsup.evolutionary import GeneticAlgorithm
from pystsup.evolutionary.metrics import calcSpacing
from pystsup.data import Solution
from pystsup.utilities import parseFile,getPath,createRandomData
from pystsup.data import Student
from pystsup.data import Supervisor
from pystsup.data import BipartiteGraph
import unittest



class GATest(unittest.TestCase):

    def setUp(self):

        self.students,self.supervisors = createRandomData(4,8,18)
        
        # Generating rank weights for c = 0.5
        self.rankWeights = Solution.calcRankWeights()

        #Creating fitness cache
        
        self.dummySolution = Solution()
        self.fitnessCache = {}
        for sup in self.supervisors:
            supervisorKeywords = self.supervisors[sup].getKeywords()
            for stu in self.students:
                studentKeywords = self.students[stu].getKeywords()
                f_stu,f_sup = self.dummySolution.kw_similarity(studentKeywords,supervisorKeywords, self.rankWeights)
                self.fitnessCache[str((stu,sup))] = (f_stu,f_sup)


        #Setting up the GA Object

        self.mutationOp = mutate
        self.selectionOp = tournamentSelection
        self.crossoverOp = crossover

        self.geneticAlgorithm = GeneticAlgorithm(self.students,self.supervisors,self.fitnessCache,self.rankWeights,self.mutationOp,self.crossoverOp,self.selectionOp)


        #Parameters for GA

        self.numberOfGenerations = 20
        self.populationSize = 10
        self.mutationProbability = 0.1
        self.swapProbability = 0.3
        self.transferProbability = 0.5

        #Initializing population
        self.population = self.geneticAlgorithm.initializePopulation(self.populationSize)
        self.maxFst = max(self.population, key=lambda x: x.getFst()).getFst()
        self.minFst = min(self.population, key=lambda x: x.getFst()).getFst()

        self.maxFsup = max(self.population, key=lambda x: x.getFsup()).getFsup()
        self.minFsup = min(self.population, key=lambda x: x.getFsup()).getFsup()



    def test_case1(self):
        """Testing the initalize population function - size of 10"""

        pop = self.geneticAlgorithm.initializePopulation(10)
        result = True
        
        for sol in pop:
            if not (isinstance(sol, Solution)):
                result = False

        if len(pop) != 10:
            result = False

        self.assertTrue(result)


    def test_case2(self):
        """Testing the fast non-dominated sort function"""

        pop = self.geneticAlgorithm.initializePopulation(7)
        points = [(25,0.6),(27,0.2),(27,0.5),(29,0.8),(30,0.1),(30,0.9),(27,0.5)]
        
        for i,sol in enumerate(pop):
            sol.setFst(points[i][0])
            sol.setFsup(points[i][1])


        fronts = self.geneticAlgorithm.fast_non_dominated_sort(pop)

        expectedFront0 = [pop[5]]
        expectedFront1 = [pop[3],pop[4]]
        expectedFront2 = [pop[0],pop[2],pop[6]]
        expectedFront3 = [pop[1]]

        expected = [expectedFront0,expectedFront1,expectedFront2,expectedFront3]

        result = True
        
        for i in range(len(expected)):
            for sol in expected[i]:
                if sol not in fronts[i]:
                    result = False
        
        self.assertTrue(result)


    def test_case3(self):
        """Testing the crowding distance assignment"""
        
        pop = self.geneticAlgorithm.initializePopulation(7)
        points = [(25,0.6),(27,0.2),(27,0.5),(29,0.8),(30,0.1),(30,0.9),(27,0.5)]
        
        for i,sol in enumerate(pop):
            sol.setFst(points[i][0])
            sol.setFsup(points[i][1])

        maxFst = max(pop, key=lambda x: x.getFst()).getFst()
        minFst = min(pop, key=lambda x: x.getFst()).getFst()

        maxFsup = max(pop, key=lambda x: x.getFsup()).getFsup()
        minFsup = min(pop, key=lambda x: x.getFsup()).getFsup()

        self.geneticAlgorithm.crowding_distance_assignment(pop,maxFst,minFst,maxFsup,minFsup)

        expected = [float("inf"),0.9,0.375,0.975,float("inf"),float("inf"),0.525]

        result = [round(sol.crowdingDistance,5) for sol in pop]

        self.assertEqual(result,expected)


    def test_case4(self):
        """Testing the crowding distance assignment function - when only 1 element in frontier"""

        pop = self.geneticAlgorithm.initializePopulation(7)
        points = [(25,0.6),(27,0.2),(27,0.5),(29,0.8),(30,0.1),(30,0.9),(27,0.5)]
        
        for i,sol in enumerate(pop):
            sol.setFst(points[i][0])
            sol.setFsup(points[i][1])

        maxFst = max(pop, key=lambda x: x.getFst()).getFst()
        minFst = min(pop, key=lambda x: x.getFst()).getFst()

        maxFsup = max(pop, key=lambda x: x.getFsup()).getFsup()
        minFsup = min(pop, key=lambda x: x.getFsup()).getFsup()

        self.geneticAlgorithm.crowding_distance_assignment([pop[0]],maxFst,minFst,maxFsup,minFsup)

        expected = [float("inf")]

        result = [round(sol.crowdingDistance,5) for sol in [pop[0]]]

        self.assertEqual(result,expected)


    def test_case5(self):
        """Testing the crowding distance assignment function - when only 2 element in frontier"""

        pop = self.geneticAlgorithm.initializePopulation(7)
        points = [(25,0.6),(27,0.2),(27,0.5),(29,0.8),(30,0.1),(30,0.9),(27,0.5)]
        
        for i,sol in enumerate(pop):
            sol.setFst(points[i][0])
            sol.setFsup(points[i][1])

        maxFst = max(pop, key=lambda x: x.getFst()).getFst()
        minFst = min(pop, key=lambda x: x.getFst()).getFst()

        maxFsup = max(pop, key=lambda x: x.getFsup()).getFsup()
        minFsup = min(pop, key=lambda x: x.getFsup()).getFsup()

        self.geneticAlgorithm.crowding_distance_assignment(pop[0:2],maxFst,minFst,maxFsup,minFsup)

        expected = [float("inf"),float("inf")]

        result = [round(sol.crowdingDistance,5) for sol in pop[0:2]]

        self.assertEqual(result,expected)


    def test_case6(self):
        """Testing the crowding distance assignment function - when only 3 element in frontier"""

        pop = self.geneticAlgorithm.initializePopulation(7)
        points = [(25,0.6),(27,0.2),(27,0.5),(29,0.8),(30,0.1),(30,0.9),(27,0.5)]
        
        for i,sol in enumerate(pop):
            sol.setFst(points[i][0])
            sol.setFsup(points[i][1])

        maxFst = max(pop, key=lambda x: x.getFst()).getFst()
        minFst = min(pop, key=lambda x: x.getFst()).getFst()

        maxFsup = max(pop, key=lambda x: x.getFsup()).getFsup()
        minFsup = min(pop, key=lambda x: x.getFsup()).getFsup()

        self.geneticAlgorithm.crowding_distance_assignment(pop[0:3],maxFst,minFst,maxFsup,minFsup)

        expected = [float("inf"),float("inf"),float("inf")]

        result = [round(sol.crowdingDistance,5) for sol in pop[0:3]]

        self.assertEqual(result,expected)


    def test_case7(self):
        """Testing the crowding distance assignment function - when only 4 element in frontier"""

        pop = self.geneticAlgorithm.initializePopulation(7)
        points = [(25,0.6),(27,0.2),(27,0.5),(29,0.8),(30,0.1),(30,0.9),(27,0.5)]
        
        for i,sol in enumerate(pop):
            sol.setFst(points[i][0])
            sol.setFsup(points[i][1])

        maxFst = max(pop, key=lambda x: x.getFst()).getFst()
        minFst = min(pop, key=lambda x: x.getFst()).getFst()

        maxFsup = max(pop, key=lambda x: x.getFsup()).getFsup()
        minFsup = min(pop, key=lambda x: x.getFsup()).getFsup()

        self.geneticAlgorithm.crowding_distance_assignment(pop[0:4],maxFst,minFst,maxFsup,minFsup)

        expected = [float("inf"),float("inf"),0.9,float("inf")]

        result = [round(sol.crowdingDistance,5) for sol in pop[0:4]]

        self.assertEqual(result,expected)


    def test_case8(self):
        """Tesitng make new Population function"""

        fronts = self.geneticAlgorithm.fast_non_dominated_sort(self.population)
        self.geneticAlgorithm.crowding_distance_assignment(self.population,self.maxFst,self.minFst,self.maxFsup,self.minFsup)
        
        newPop = self.geneticAlgorithm.makeNewPopulation(self.population,self.populationSize,self.mutationProbability,self.swapProbability,self.transferProbability)

        result = True

        for sol in newPop:
            if not (isinstance(sol, Solution)):
                result = False

        if len(newPop) != ((self.populationSize)+(self.populationSize//2)):
            result = False

        

        self.assertTrue(result)



    def test_case9(self):
        """Testing the calc Spacing Metric function - when 2 elements in frontier"""

        pop = self.geneticAlgorithm.initializePopulation(2)
        points = [(25,0.6),(27,0.2)]
        
        for i,sol in enumerate(pop):
            sol.setFst(points[i][0])
            sol.setFsup(points[i][1])


        result = calcSpacing(pop)

        self.assertEqual(result,0)


    def test_case10(self):
        """Testing the calc Spacing Metric function - when multiple elements in frontier"""

        pop = self.geneticAlgorithm.initializePopulation(7)
        points = [(25,0.6),(27,0.2),(27,0.5),(29,0.8),(30,0.1),(30,0.9),(27,0.5)]
        
        for i,sol in enumerate(pop):
            sol.setFst(points[i][0])
            sol.setFsup(points[i][1])


        result = calcSpacing(pop)
        expected = 0.683927116

        self.assertAlmostEqual(result,expected,places=5)


    def test_case11(self):
        """Testing the calc Spacing Metric function - when 1 element in frontier"""

        pop = self.geneticAlgorithm.initializePopulation(1)
        points = [(25,0.6)]
        
        for i,sol in enumerate(pop):
            sol.setFst(points[i][0])
            sol.setFsup(points[i][1])


        result = calcSpacing(pop)

        self.assertEqual(result,0)
        

    def test_case12(self):
        """Testing the calc Spacing Metric function - when 0 elements in frontier"""

        pop = self.geneticAlgorithm.initializePopulation(0)

        result = calcSpacing(pop)

        self.assertEqual(result,0)
        

        

        

        
        
        
                                              
        




    

    

        

        

        

        


        
        
