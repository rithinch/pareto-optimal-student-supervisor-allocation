"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: test
    File: test_solution.py
    
    Purpose:  Unit Testing for Solution Class.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""



import unittest

from pystsup.data import Solution
from pystsup.utilities import parseFile,getPath
from pystsup.data import Student
from pystsup.data import Supervisor
from pystsup.data import BipartiteGraph

class SolutionTest(unittest.TestCase):

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
        """Testing the create random solution function"""

        solution1 = Solution.generateRandomSolution(self.students,self.supervisors)
        
        result = solution1.isValid(self.students,self.supervisors)

        self.assertEqual(result,True)


    def test_case2(self):
        """Testing the calculate Rank Weights function when c = 1"""

        rankWeights = Solution.calcRankWeights(c=1)

        result = True
        
        expected = 0.2
        
        for i in rankWeights:

            if rankWeights[i] != expected:

                result = False
                break

        self.assertTrue(result)


    def test_case3(self):
        """Testing the calculate rank weights function when c = 0.3"""

        rankWeights = Solution.calcRankWeights(c=0.3)

        result = round(sum(rankWeights.values()),15)

        expected = {1: 0.701705143, 2: 0.210511543, 3: 0.063153463, 4: 0.0189460389, 5: 0.005683812}

        result2 = True

        for i in rankWeights:

            if round(rankWeights[i],8) != round(expected[i],8):
                result2 = False
                break
        

        self.assertEqual((result,result2),(1,True))


    def test_case4(self):
        """Testing the calculate rank weights function when c=0 and n=0"""

        rankWeights = Solution.calcRankWeights(c=0,n=0)
        expected = {}

        self.assertEqual(rankWeights,expected)


    def test_case5(self):
        """Testing similarity function with 2 non-similar profiles (0)"""

        dummySolution = Solution()

        supervisorKeywords = self.supervisors["supervisor3"].getKeywords()
        studentKeywords = self.students["student1"].getKeywords()
        
        f_stu,f_sup = dummySolution.kw_similarity(studentKeywords,supervisorKeywords,self.rankWeights)

        expected_fstu = 0.1217742
        expected_fsup = 0.1416129

        expected = (round(expected_fstu,6),round(expected_fsup,6))
        retrieved = (round(f_stu,6),round(f_sup,6))
        
        self.assertEqual(retrieved,expected)


    def test_case6(self):
        """Testing similarity function with 2 identical profiles (1)"""

        dummySolution = Solution()

        supervisorKeywords = self.supervisors["supervisor3"].getKeywords()
        studentKeywords = self.students["student4"].getKeywords()
        
        f_stu,f_sup = dummySolution.kw_similarity(studentKeywords,supervisorKeywords,self.rankWeights)

        self.assertEqual((f_stu,f_sup),(1,1))


    def test_case7(self):
        """Testing similarity function between 2 mostly similar profiles """
        
        dummySolution = Solution()

        supervisorKeywords = self.supervisors["supervisor3"].getKeywords()
        studentKeywords = self.students["student3"].getKeywords()

        f_stu,f_sup = dummySolution.kw_similarity(studentKeywords,supervisorKeywords,self.rankWeights)

        expected_fstu = 0.708333
        expected_fsup = 0.726882

        expected = (round(expected_fstu,6),round(expected_fsup,6))
        retrieved = (round(f_stu,6),round(f_sup,6))

        self.assertEqual(retrieved,expected)


    def test_case8(self):
        """Testing similarity function between 2 less similar profiles """
        
        dummySolution = Solution()

        supervisorKeywords = self.supervisors["supervisor3"].getKeywords()
        studentKeywords = self.students["student2"].getKeywords()

        f_stu,f_sup = dummySolution.kw_similarity(studentKeywords,supervisorKeywords,self.rankWeights)

        expected_fstu = 0.255645
        expected_fsup = 0.522043

        expected = (round(expected_fstu,6),round(expected_fsup,6))
        retrieved = (round(f_stu,6),round(f_sup,6))

        self.assertEqual(retrieved,expected)


    def test_case9(self):
        """Testing intersection function - between 2 non-intersecting lists"""

        list1 = self.supervisors["supervisor1"].getKeywords()[1][1]
        list2 = self.students["student1"].getKeywords()[1][1]

        result = self.dummySolution._intersection(list1,list2)

        self.assertEqual(result,1)


    def test_case10(self):
        """Testing intersection function - between 2 lists with 1 common element"""

        list1 = ["Document types","General and reference"]
        list2 = ["Cross-computing tools and techniques","General and reference"]


        result = self.dummySolution._intersection(list1,list2)

        self.assertEqual(result,1)


    def test_case11(self):
        """Testing intersection function - between 2 lists with 2 common element"""

        list1 = ["Reference works","Document types","General and reference"]
        list2 = ["Surveys and overviews","Document types","General and reference"]

        result = self.dummySolution._intersection(list1,list2)

        self.assertEqual(result,2)


    def test_case12(self):
        """Testing intersection function - between 2 lists with 3 common element"""

        list1 = ["Digital signal processing","Signal processing systems","Communication hardware, interfaces and storage","Hardware"]
        list2 = ["Beamforming","Signal processing systems","Communication hardware, interfaces and storage","Hardware"]

        result = self.dummySolution._intersection(list1,list2)

        self.assertEqual(result,3)


    def test_case13(self):
        """Testing intersection function - between 2 identical lists"""

        list1 = self.supervisors["supervisor1"].getKeywords()[1][1]
        list2 = self.students["student4"].getKeywords()[1][1]

        result = self.dummySolution._intersection(list1,list2)

        self.assertEqual(result,5)


    def test_case14(self):
        """Testing the calc fitness function for a bad solution"""
        
        self.solution1.calcFitness(self.students,self.supervisors,self.rankWeights,self.fitnessCache)
        F_st = self.solution1.getFst()
        F_sup = self.solution1.getFsup()

        retrieved = (round(F_sup,6),round(F_st,6))
        expected = (0.600813,1.457903)

        self.assertEqual(retrieved,expected)

    def test_case15(self):
        """Testing the calc fitness function for a fairly good solution"""
        
        self.solution2.calcFitness(self.students,self.supervisors,self.rankWeights,self.fitnessCache)
        F_st = self.solution2.getFst()
        F_sup = self.solution2.getFsup()
        
        retrieved = (round(F_sup,7),round(F_st,7))
        expected = (1.1482502,2.1678495)

        self.assertEqual(retrieved,expected)


    def test_case16(self):
        """Testing transfer function - a valid transfer"""

        self.solution1.transferStudent("student3","supervisor1","supervisor2",self.supervisors)

        solutionGraph = self.solution1.getGraph()
        val1 = solutionGraph.getStudents("supervisor1")
        val2 = solutionGraph.getStudents("supervisor2")
        val3 = solutionGraph.getSupervisors("student3")

        expected = (['student2'],['student4','student3'],['supervisor2'])

        self.assertEqual((val1,val2,val3),expected)


    def test_case17(self):
        """Testing getGraph function"""

        solutionGraph = self.solution1.getGraph()

        val1 = isinstance(solutionGraph,BipartiteGraph)
        val2 = solutionGraph.getStuEdges()

        result = (val1,val2)

        expected1 = True
        expected2 = {'student1':['supervisor3'],'student2':['supervisor1'],'student3':['supervisor1'],'student4':['supervisor2']}

        expected = (expected1,expected2)

        self.assertEqual(result,expected)


    def test_case18(self):
        """Testing the isValid function - passing a null graph"""

        graph = BipartiteGraph()
        solution = Solution(graph)
        
        result = solution.isValid(self.students,self.supervisors)

        self.assertFalse(result)


    def test_case19(self):
        """Testing the isValid function - when number of supervisors less than actual"""

        graph = BipartiteGraph()
        
        graph.addEdge("supervisor1","student1")
        graph.addEdge("supervisor2","student4")
        graph.addEdge("supervisor2","student3")
        graph.addEdge("supervisor1","student2")

        solution = Solution(graph)

        result = solution.isValid(self.students,self.supervisors)

        self.assertFalse(result)


    def test_case20(self):
        """Testing the isValid function - when number of students less than actual"""

        graph = BipartiteGraph()
        
        graph.addEdge("supervisor1","student1")
        graph.addEdge("supervisor3","student3")
        graph.addEdge("supervisor2","student2")

        solution = Solution(graph)

        result = solution.isValid(self.students,self.supervisors)

        self.assertFalse(result)
        

    def test_case21(self):
        """Testing the isValid function - when a supervisor's allocation exceeds their quota"""

        self.graph1.addEdge("supervisor3","student2")

        solution = Solution(self.graph1)

        result = solution.isValid(self.students,self.supervisors)

        self.assertFalse(result)


    def test_case22(self):
        """Testing the isValid function - when a supervisor's degree is 0"""

        self.graph1.removeEdge("supervisor3","student1")

        solution = Solution(self.graph1)

        result = solution.isValid(self.students,self.supervisors)

        self.assertFalse(result)
        


    def test_case23(self):
        """Testing the isValid function - when a student's degree is not equal to 1"""

        self.graph1.addEdge("supervisor2","student3")

        solution = Solution(self.graph1)

        result = solution.isValid(self.students,self.supervisors)

        self.assertFalse(result)


    def test_case24(self):
        """Testing is valid function - when a correct graph is passed"""

        result1 = self.solution1.isValid(self.students,self.supervisors)
        result2 = self.solution2.isValid(self.students,self.supervisors)

        self.assertEqual((result1,result2),(True,True))


    def test_case25(self):
        """Testing 'dominates' function - when both Fst and Fsup are greater in solution1 than solution2"""

        solution1 = Solution()
        solution2 = Solution()

        solution1.setFst(29.5)
        solution1.setFsup(0.4)

        solution2.setFst(27.5)
        solution2.setFsup(0.2)

        result = solution1.dominates(solution2)

        self.assertTrue(result)


    def test_case26(self):
        """Testing 'dominates' function - when only Fsup is greater in solution2 than solution1"""

        solution1 = Solution()
        solution2 = Solution()

        solution1.setFst(29.5)
        solution1.setFsup(0.4)

        solution2.setFst(27.5)
        solution2.setFsup(0.6)

        result = solution1.dominates(solution2)

        self.assertFalse(result)


    def test_case27(self):
        """Testing 'dominates' function - when Fsup is same in solution2 and solution1"""

        solution1 = Solution()
        solution2 = Solution()

        solution1.setFst(29.5)
        solution1.setFsup(0.4)

        solution2.setFst(27.5)
        solution2.setFsup(0.4)

        result = solution1.dominates(solution2)

        self.assertTrue(result)


    def test_case28(self):
        """Testing 'dominates' function - when only Fst is greater in solution2 and solution1"""

        solution1 = Solution()
        solution2 = Solution()

        solution1.setFst(26.5)
        solution1.setFsup(0.4)

        solution2.setFst(27.5)
        solution2.setFsup(0.2)

        result = solution1.dominates(solution2)

        self.assertFalse(result)
        

    def test_case29(self):
        """Testing 'dominates' function - when both Fst and Fsup are lesser in solution1 than solution2"""

        solution1 = Solution()
        solution2 = Solution()

        solution1.setFst(26.5)
        solution1.setFsup(0.2)

        solution2.setFst(27.5)
        solution2.setFsup(0.4)

        result = solution1.dominates(solution2)

        self.assertFalse(result)
        

    def test_case30(self):
        """Testing 'dominates' function - when Fst is same in solution2 and solution1"""

        solution1 = Solution()
        solution2 = Solution()

        solution1.setFst(29.5)
        solution1.setFsup(0.6)

        solution2.setFst(29.5)
        solution2.setFsup(0.4)

        result = solution1.dominates(solution2)

        self.assertTrue(result)
        

    def test_case31(self):
        """Testing 'dominates' function - when Fst is same in solution2 and solution1"""

        solution1 = Solution()
        solution2 = Solution()

        solution1.setFst(29.5)
        solution1.setFsup(0.2)

        solution2.setFst(29.5)
        solution2.setFsup(0.4)

        result = solution1.dominates(solution2)

        self.assertFalse(result)
        

    def test_case32(self):
        """Testing 'dominates' function - when Fst and Fsup are same in solution2 and solution1"""

        solution1 = Solution()
        solution2 = Solution()

        solution1.setFst(29.5)
        solution1.setFsup(0.4)

        solution2.setFst(29.5)
        solution2.setFsup(0.4)

        result = solution1.dominates(solution2)

        self.assertFalse(result)

    
    
        
        
