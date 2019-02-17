"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: test
    File: test_crossover.py
    
    Purpose:  Unit Testing for Crossover Operators.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""

import unittest

from pystsup.evolutionary.mutation import mutate 
from pystsup.evolutionary.crossover import simplify,crossover,kPoint, sp_crossover
from pystsup.data import Solution
from pystsup.utilities import parseFile,getPath,createRandomData
from pystsup.data import Student
from pystsup.data import Supervisor
from pystsup.data import BipartiteGraph


class CrossoverTest(unittest.TestCase):

    def setUp(self):

        #Creating a list of students and supervisors

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        
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

        # Creating test for simplify function
        self.graph3 = BipartiteGraph()
        self.graph3.addEdge("s1","st1")
        self.graph3.addEdge("s1","st4")
        self.graph3.addEdge("s2","st1")
        self.graph3.addEdge("s2","st2")
        self.graph3.addEdge("s3","st3")
        self.graph3.addEdge("s3","st5")
        self.graph3.addEdge("s4","st3")
        self.graph3.addEdge("s4","st5")
        self.structure3 = { "s1":2, "s2":1, "s3":1, "s4":1 }

        self.graph4 = BipartiteGraph()
        self.graph4.addEdge( "s1","st1")
        self.graph4.addEdge( "s1","st3")
        self.graph4.addEdge( "s1","st4")
        self.graph4.addEdge( "s2","st3")
        self.graph4.addEdge( "s2","st4")
        self.graph4.addEdge( "s3","st1")
        self.graph4.addEdge( "s3","st2")
        self.structure4 = { "s1":1, "s2":2, "s3":1 }
        
        #Creating 60-400 data set

        self.students2,self.supervisors2 = createRandomData(60,400,405)
        # m,n,quotaSum,level=3,maxQuota=10,minQuota=4,no_topics=5
        self.students3,self.supervisors3 = createRandomData(3,5,8,minQuota=1,maxQuota=3)
        self.problem_instances = [ #createRandomData(6,10,16,minQuota=1) 
                createRandomData(60,400,405) ]

        

        #def test_case_special_cr(self):
        #for (students,supervisors) in self.problem_instances :
            #for i in range(100):
             #   sol1 = Solution.generateRandomSolution(students,supervisors)
             #   sol2 = Solution.generateRandomSolution(students,supervisors)
             #   sp_crossover(sol1,sol2)

    def test_case_simplify1(self):
       response, already_set = simplify(self.graph3,self.structure3)
       self.assertTrue( ("s1","st1") in response )
       self.assertTrue( ("s1","st4") in response )
       self.assertTrue( ("s2","st2") in response )
       self.assertEqual( self.structure3["s1"], 0 )
       self.assertEqual( self.structure3["s2"], 0 )
       self.assertEqual( self.structure3["s3"], 1 )
       self.assertEqual( self.structure3["s4"], 1 )
       self.assertTrue( ("stu","st1") in already_set )
       self.assertTrue( ("stu","st4") in already_set )
       self.assertTrue( ("stu","st2") in already_set )
       self.assertTrue( ("sup","s1") in already_set )
       self.assertTrue( ("sup","s2") in already_set )
       self.assertEqual( len(response), 3 )

    def test_case_simplify2(self):
       response, already_set = simplify(self.graph4,self.structure4)
       self.assertTrue( ("s1","st1") in response )
       self.assertTrue( ("s2","st3") in response )
       self.assertTrue( ("s2","st4") in response )
       self.assertTrue( ("s3","st2") in response )
       self.assertEqual( self.structure4["s1"], 0 )
       self.assertEqual( self.structure4["s2"], 0 )
       self.assertEqual( self.structure4["s3"], 0 )
       self.assertTrue( ("stu","st1") in already_set )
       self.assertTrue( ("stu","st3") in already_set )
       self.assertTrue( ("stu","st4") in already_set )
       self.assertTrue( ("stu","st2") in already_set )
       self.assertTrue( ("sup", "s1") in already_set )
       self.assertTrue( ("sup", "s2") in already_set )
       self.assertTrue( ("sup", "s3") in already_set )
       self.assertEqual( len(response), 4 )


    def test_case1(self):
        """Testing the ERX Modified Crossover function - for 3sup:4stu solution"""

        solution3 = crossover(self.solution1,self.solution2,self.supervisors,self.students)

        structureResult = (solution3.getGraph().getStructure() == self.solution1.getGraph().getStructure()) or (solution3.getGraph().getStructure() == self.solution2.getGraph().getStructure())
        result = (solution3.isValid(self.students,self.supervisors)) and (structureResult)

        self.assertTrue(result)


    def test_case2(self):
        """Testing the kPoint crossover function - for 3sup:4stu solution"""

        solution3 = kPoint(self.solution1,self.solution2,self.supervisors,self.students,k=3)
        result = solution3.isValid(self.students,self.supervisors)
        self.assertTrue(result)

    def test_case3(self):
        """Testing the EDX Modified crossover function - when one valid and one dummy solution are passed"""

        self.assertRaises(KeyError, lambda: crossover(self.solution1,self.dummySolution,self.supervisors,self.students))
        

    def test_case4(self):
        """Testing the K Point Crossover function - when one valid and one dummy solution are passed"""

        self.assertRaises(KeyError, lambda: kPoint(self.solution2,self.dummySolution,self.supervisors,self.students,k=3))


    def test_case5(self):
        """Testing the ERX Modified Crossover function - for random 3sup:4stu solution"""

        solution1 = Solution.generateRandomSolution(self.students,self.supervisors)
        solution2 = Solution.generateRandomSolution(self.students,self.supervisors)

        solution3 = crossover(solution1,solution2,self.supervisors,self.students)

        structureResult = (solution3.getGraph().getStructure() == solution1.getGraph().getStructure()) or (solution3.getGraph().getStructure() == solution2.getGraph().getStructure())
        result = (solution3.isValid(self.students,self.supervisors)) and (structureResult)

        self.assertTrue(result)


    def test_case6(self):
        """Testing the K Point Crossover function - for random 3sup:4stu solution"""

        solution1 = Solution.generateRandomSolution(self.students,self.supervisors)
        solution2 = Solution.generateRandomSolution(self.students,self.supervisors)

        solution3 = kPoint(solution1,solution2,self.supervisors,self.students,k=3)
        
        result = solution3.isValid(self.students,self.supervisors)

        self.assertTrue(result)
        

    def test_case7(self):
        """Testing the K Point crossover function - when k=0"""

        solution3 = kPoint(self.solution1,self.solution2,self.supervisors,self.students,k=0)
        
        structureResult = (solution3.getGraph().getStructure() == self.solution1.getGraph().getStructure()) or (solution3.getGraph().getStructure() == self.solution2.getGraph().getStructure())
        result = (solution3.isValid(self.students,self.supervisors)) and (structureResult)

        self.assertTrue(result)
        

    def test_case8(self):
        """Testing the K Point crossover function - when k=1"""

        solution3 = kPoint(self.solution1,self.solution2,self.supervisors,self.students,k=1)

        result = solution3.isValid(self.students,self.supervisors)

        self.assertTrue(result)
        

    def test_case9(self):
        """Testing the K Point crossover function - when k > no_students"""

        self.assertRaises(ValueError, lambda: kPoint(self.solution1,self.solution2,self.supervisors,self.students,k=6))


    def test_case10(self):
        """Testing the ERX Modified crossover function - for random 60sup:400stu solution"""

        solution1 = Solution.generateRandomSolution(self.students2,self.supervisors2)
        solution2 = Solution.generateRandomSolution(self.students2,self.supervisors2)

        solution3 = crossover(solution1,solution2, self.supervisors2, self.students2)

        structureResult = (solution3.getGraph().getStructure() == solution1.getGraph().getStructure()) or (solution3.getGraph().getStructure() == solution2.getGraph().getStructure())
        result = (solution3.isValid(self.students2,self.supervisors2)) and (structureResult)

        self.assertTrue(result)


    def test_case11(self):
        """Testing the ERX Modified crossover function - for random 60sup:400stu solution"""

        solution1 = Solution.generateRandomSolution(self.students2,self.supervisors2)
        solution2 = Solution.generateRandomSolution(self.students2,self.supervisors2)

        solution3 = crossover(solution1,solution2, self.supervisors, self.supervisors2, self.students2)

        structureResult = (solution3.getGraph().getStructure() == solution1.getGraph().getStructure()) or (solution3.getGraph().getStructure() == solution2.getGraph().getStructure())
        result = (solution3.isValid(self.students2,self.supervisors2)) and (structureResult)

        self.assertTrue(result)


    def test_case12(self):
        """Testing the kPoint crossover function - for random 60sup:400stu solution"""

        solution1 = Solution.generateRandomSolution(self.students2,self.supervisors2)
        solution2 = Solution.generateRandomSolution(self.students2,self.supervisors2)

        solution3 = kPoint(solution1,solution2,self.supervisors2,self.students2,k=15)
        
        result = solution3.isValid(self.students2,self.supervisors2) 

        self.assertTrue(result)


    def test_case13(self):
        """Testing the kPoint crossover function - for random 60sup:400stu solution"""

        solution1 = Solution.generateRandomSolution(self.students2,self.supervisors2)
        solution2 = Solution.generateRandomSolution(self.students2,self.supervisors2)

        solution3 = kPoint(solution1,solution2,self.supervisors2,self.students2,k=15)
        
        result = solution3.isValid(self.students2,self.supervisors2)

        self.assertTrue(result)
        

        

    

        

        


        
        
        
    
        


        
    
