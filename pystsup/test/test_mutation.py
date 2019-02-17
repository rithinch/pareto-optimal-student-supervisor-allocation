"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: test
    File: test_mutation.py
    
    Purpose:  Unit Testing for Mutation Operators.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""




import unittest

from pystsup.evolutionary.mutation import mutate
from pystsup.data import Solution
from pystsup.utilities import parseFile,getPath
from pystsup.data import Student
from pystsup.data import Supervisor
from pystsup.data import BipartiteGraph

class MutationTest(unittest.TestCase):

    def setUp(self):

        #Creating a list of students and supervisors

        topicNames,topicPaths, topicIDs, levels = parseFile("pystsup/test/acm.txt")
        
        self.supervisors = {}
        self.students = {}

        stuID = "student"
        supID = "supervisor"

        stuList1 = ["MapReduce-based systems","Multidimensional range search","Open source software","Data mining","Online shopping"]
        stuList2 = ["Heuristic function construction","Multi-agent systems","Open source software","Data mining","Speech recognition"]
        stuList3 = ["Multi-agent systems","Speech recognition","Heuristic function construction","Data mining","Object identification"]
        stuList4 = ["Multi-agent systems","Intelligent agents","Speech recognition","Object identification","Heuristic function construction"]

        supList1 = ["Multi-agent systems","Intelligent agents","MapReduce-based systems","Object identification","Heuristic function construction"]
        supList2 = ["Open source software","Data mining","Speech recognition","Object identification","Heuristic function construction"]
        supList3 = ["Multi-agent systems","Intelligent agents","Speech recognition","Object identification","Heuristic function construction"]
        
        supList = [supList1,supList2,supList3]
        supQuota = [2,2,1]
        stuList = [stuList1,stuList2,stuList3,stuList4]

        for i in range(3):
            toAdd = []
            sup_list = {}
            rank = 0
            for kw in supList[i]:
                rank+=1
                sup_list[rank]=[kw,getPath(kw,topicNames,topicPaths, topicIDs)]

            sup = supID + str(i+1)
            quota = supQuota[i]

            supervisorObject = Supervisor(sup,sup_list,quota)

            self.supervisors[sup]=supervisorObject
            

        for i in range(4):
            toAdd = []
            stu_list = {}
            rank = 0
            for kw in stuList[i]:
                rank+=1
                stu_list[rank] = [kw,getPath(kw,topicNames,topicPaths, topicIDs)]

            stu = stuID + str(i+1)
            studentObject = Student(stu,stu_list)
            self.students[stu]=studentObject



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


        # Creating two graphs and solutions

        self.graph1 = BipartiteGraph()
        self.graph2 = BipartiteGraph()

        self.graph1.addEdge("supervisor1","student2")
        self.graph1.addEdge("supervisor2","student4")
        self.graph1.addEdge("supervisor3","student1")
        self.graph1.addEdge("supervisor1","student3")

        self.solution1 = Solution(self.graph1)

        self.graph2.addEdge("supervisor1","student2")
        self.graph2.addEdge("supervisor2","student1")
        self.graph2.addEdge("supervisor3","student4")
        self.graph2.addEdge("supervisor1","student3")

        self.solution2 = Solution(self.graph2)


    def test_case1(self):
        """Testing mutation function for solution 1"""
        mutationProbability = 0.3
        swapProbability = 0.5
        transferProbability = 0.5
        solution3 = mutate(self.solution1,self.supervisors,mutationProbability,swapProbability,transferProbability)

        result = solution3.isValid(self.students,self.supervisors)

        self.assertTrue(result)

    def test_case2(self):
        """Testing mutation function for solution 1 - only swap operation"""
        mutationProbability = 0.3
        swapProbability = 0.5
        transferProbability = 0
        solution3 = mutate(self.solution1,self.supervisors,mutationProbability,swapProbability,transferProbability)

        result = solution3.isValid(self.students,self.supervisors)

        self.assertTrue(result)

    def test_case3(self):
        """Testing mutation function for solution 1 - only transfer operation"""
        mutationProbability = 0.3
        swapProbability = 0
        transferProbability = 0.5
        solution3 = mutate(self.solution1,self.supervisors,mutationProbability,swapProbability,transferProbability)

        result = solution3.isValid(self.students,self.supervisors)

        self.assertTrue(result)

    def test_case4(self):
        """Testing mutation function for solution 2"""
        mutationProbability = 0.3
        swapProbability = 0.5
        transferProbability = 0.3
        solution4 = mutate(self.solution2,self.supervisors,mutationProbability,swapProbability,transferProbability)

        result = solution4.isValid(self.students,self.supervisors)

        self.assertTrue(result)


    def test_case5(self):
        """Testing mutation function for a randomly created solution 1"""
        
        mutationProbability = 0.3
        swapProbability = 0.2
        transferProbability = 0.8

        solution1 = Solution.generateRandomSolution(self.students,self.supervisors)
        
        solution2 = mutate(solution1,self.supervisors,mutationProbability,swapProbability,transferProbability)

        result = solution2.isValid(self.students,self.supervisors)

        self.assertTrue(result)


    def test_case6(self):
        """Testing mutation function for a randomly created solution 2"""
        
        mutationProbability = 0.3
        swapProbability = 0.7
        transferProbability = 0

        solution1 = Solution.generateRandomSolution(self.students,self.supervisors)
        
        solution2 = mutate(solution1,self.supervisors,mutationProbability,swapProbability,transferProbability)

        result = solution2.isValid(self.students,self.supervisors)

        self.assertTrue(result)

    

    

        
        
