"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: test
    File: test_bipartiteGraph.py
    
    Purpose:  Unit Testing for Biparted Graph Class.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""

import unittest

from pystsup.data import BipartiteGraph
from pystsup.data import Student
from pystsup.data import Supervisor
from pystsup.utilities import parseFile,getPath
from pystsup.data import Solution

class BipartiteGraphTest(unittest.TestCase):

    def setUp(self):
        
        self.graph1 = BipartiteGraph()
        self.graph2 = BipartiteGraph()

        self.graph1.addEdge("supervisor1","student1")
        self.graph1.addEdge("supervisor2","student4")
        self.graph1.addEdge("supervisor3","student3")
        self.graph1.addEdge("supervisor1","student2")

        self.graph2.addEdge("supervisor1","student4")
        self.graph2.addEdge("supervisor2","student1")
        self.graph2.addEdge("supervisor2","student3")
        self.graph2.addEdge("supervisor3","student2")

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
                sup_list[kw]=[rank,getPath(kw,topicNames,topicPaths, topicIDs)]

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
                stu_list[kw] = [rank,getPath(kw,topicNames,topicPaths, topicIDs)]

            stu = stuID + str(i+1)
            studentObject = Student(stu,stu_list)
            self.students[stu]=studentObject  


    def test_case1(self):
        """Testing addEdge function in an empty graph"""

        graph = BipartiteGraph()

        graph.addEdge("supervisor1","student1")

        val1 = graph.getStudents("supervisor1")
        val2 = graph.getSupervisors("student1")

        expected1 = ["student1"]
        expected2 = ["supervisor1"]

        self.assertEqual((val1,val2),(expected1,expected2))

    def test_case2(self):
        """Testing addEdge function in a graph with existing nodes and edges"""

        graph = BipartiteGraph()

        graph.addEdge("supervisor1","student1")
        graph.addEdge("supervisor2","student4")
        graph.addEdge("supervisor3","student3")

        val1 = graph.getSupervisorDegree("supervisor1")

        graph.addEdge("supervisor1","student2")

        curr = graph.getSupervisorDegree("supervisor1")
        val2 = graph.getSupervisors("student2")
        expected2 = ["supervisor1"]

        self.assertEqual((curr-1,expected2),(val1,val2))

    def test_case3(self):
        """Testing addEdge function when adding an edge that already exists"""

        graph = BipartiteGraph()
        graph.addEdge("supervisor1","student1")
        graph.addEdge("supervisor1","student1")

        val1 = graph.getSupervisorDegree("supervisor1")
        val2 = graph.getStudentDegree("student1")

        self.assertEqual((val1,val2),(1,1))

    def test_case4(self):
        """Testing the remove edge function in an empty graph"""

        graph = BipartiteGraph()
        self.assertRaises(KeyError, lambda: graph.removeEdge("supervisor1","student1"))


    def test_case5(self):
        """Testing the removeEdge function when trying to remove an edge that doesn't exist"""

        self.assertRaises(ValueError, lambda: self.graph1.removeEdge("supervisor2","student1"))


    def test_case6(self):
        """Testing the removeEdge function in a graph with existing nodes and edges"""

        graph = BipartiteGraph()

        graph.addEdge("supervisor1","student1")
        graph.removeEdge("supervisor1","student1")

        val1 = graph.getStudentDegree("student1")
        val2 = graph.getSupervisorDegree("supervisor1")

        self.assertEqual((val1,val2),(0,0))


    def test_case7(self):
        """Testing the merge function in two graphs"""

        graph3 = self.graph1.merge(self.graph2)

        expected = {'supervisor1':['student1','student2','student4'],'supervisor2':['student4','student1','student3'],'supervisor3':['student3','student2']}

        result = True

        for sup in expected:
            for stu in expected[sup]:
                if not graph3.isEdge(sup,stu):
                    result = False
                    break

        self.assertTrue(result)


    def test_case8(self):
        """Testing the create random graph function"""

        graph = BipartiteGraph.createRandomGraph(self.students,self.supervisors)

        solution = Solution(graph)
        
        result = solution.isValid(self.students,self.supervisors)
        
        self.assertTrue(result)

  
    def test_case9(self):
        """Testing transfer function - Cannnot transfer student when a supervisor has less than 2 students"""
        
        self.graph1.transferStudent("student3","supervisor3","supervisor2",self.supervisors)
        val1 = self.graph1.getStudentDegree("student3")
        val2 = self.graph1.getSupervisors("student3")
        expected = (1,['supervisor3'])
        
        self.assertEqual((val1,val2),expected)
        

    def test_case10(self):
        """Testing transfer function - cannot transfer student to a supervisor who reached their maximum quota"""

        self.graph1.transferStudent("student1","supervisor1","supervisor3",self.supervisors)
        
        val1 = self.graph1.getSupervisorDegree("supervisor1")
        val2 = self.graph1.getSupervisors("student1")
        val3 = self.graph1.getStudents("supervisor3")

        expected = (2,['supervisor1'],['student3'])

        self.assertEqual((val1,val2,val3),expected)


    def test_case11(self):
        """Testing transfer function - cannot transfer student if student doesn't exist in the graph"""

        self.graph1.transferStudent("student5","supervisor1","supervisor2",self.supervisors)
        
        val1 = self.graph1.getSupervisorDegree("supervisor1")
        val2 = self.graph1.getStudents("supervisor3")

        expected = (2,['student3'])

        self.assertEqual((val1,val2),expected)


    def test_case12(self):
        """Testing transfer function - cannot transfer student if the edge doesn't exist in the graph"""

        self.graph1.transferStudent("student3","supervisor1","supervisor2", self.supervisors)

        val1 = self.graph1.getSupervisorDegree("supervisor1")
        val2 = self.graph1.getStudents("supervisor2")
        val3 = self.graph1.getStudents("supervisor1")

        expected = (2,['student4'],['student1','student2'])

        self.assertEqual((val1,val2,val3),expected)


    def test_case13(self):
        """Testing transfer function - cannot transfer student if edge already exists in the supervisor transferring to"""

        self.graph1.transferStudent("student4","supervisor1","supervisor2", self.supervisors)

        val1 = self.graph1.getSupervisorDegree("supervisor1")
        val2 = self.graph1.getStudents("supervisor2")
        val3 = self.graph1.getStudents("supervisor1")

        expected = (2,['student4'],['student1','student2'])

        self.assertEqual((val1,val2,val3),expected)


    def test_case14(self):
        """Testing transfer function - a valid transfer"""

        self.graph1.transferStudent("student2","supervisor1","supervisor2",self.supervisors)

        val1 = self.graph1.getStudents("supervisor1")
        val2 = self.graph1.getStudents("supervisor2")
        val3 = self.graph1.getSupervisors("student2")

        expected = (['student1'],['student4','student2'],['supervisor2'])

        self.assertEqual((val1,val2,val3),expected)


    def test_case15(self):
        """Testing supervisor Exists function - when a supervisor does not exist"""

        result = self.graph1.supervisorExists("supervisor4")

        self.assertFalse(result)


    def test_case16(self):
        """Testing supervisor Exists function - when a supervisor exists"""

        result = self.graph1.supervisorExists("supervisor1")

        self.assertTrue(result)

    def test_case17(self):
        """Testing student exists function - when a student does not exists"""

        result = self.graph1.studentExists("student5")

        self.assertFalse(result)

    def test_case18(self):
        """Testing student exists function - when a student exists"""

        result = self.graph1.studentExists("student1")

        self.assertTrue(result)

    def test_case19(self):
        """Testing isEdge function - when a supervisor does not exist in graph"""

        result = self.graph1.isEdge("supervisor5","student1")
        self.assertFalse(result)
        

    def test_case20(self):
        """Testing isEdge function - when a student does not exist in graph"""

        result = self.graph1.isEdge("supervisor1","student5")
        self.assertFalse(result)
        

    def test_case21(self):
        """Testing isEdge function - when a edge does not exist"""

        result= self.graph1.isEdge("supervisor2","student1")

        self.assertFalse(result)

    def test_case22(self):
        """Testing isEdge function - when a edge exists"""
        
        result = self.graph1.isEdge("supervisor1","student1")

        self.assertTrue(result)

    def test_case23(self):
        """Testing getStudents function"""

        result = self.graph1.getStudents("supervisor3")
        expected = ['student3']

        self.assertEqual(result,expected)


    def test_case24(self):
        """Testing getSupervisors function"""

        result = self.graph1.getSupervisors("student1")
        expected = ['supervisor1']

        self.assertEqual(result,expected)

    def test_case25(self):
        """Testing getSupervisorDegree function"""

        result = self.graph1.getSupervisorDegree("supervisor1")
        expected = 2

        self.assertEqual(result,expected)

    def test_case26(self):
        """Testing getStudentDegree function"""

        result = self.graph1.getStudentDegree("student2")
        expected = 1

        self.assertEqual(result,expected)

    def test_case27(self):
        """Testing getStructure function"""

        result = self.graph1.getStructure()
        expected = {'supervisor1':2,'supervisor2':1,'supervisor3':1}

        self.assertEqual(result,expected)

    def test_case28(self):
        """Testing getEdges function"""

        result = self.graph1.getEdges()
        expected = {'supervisor1':['student1','student2'],'supervisor2':['student4'],'supervisor3':['student3']}

        self.assertEqual(result,expected)

    def test_case29(self):
        """Testing getStuEdges function"""

        result = self.graph1.getStuEdges()
        expected = {'student1':['supervisor1'],'student2':['supervisor1'],'student3':['supervisor3'],'student4':['supervisor2']}

        self.assertEqual(result,expected)

    def test_case30(self):
        """Testing getNumberofEdges function"""

        result = self.graph1.getNumberofEdges()
        expected = 4

        self.assertEqual(result,expected)


    def test_case31(self):
        """Testing the swap function - when 2 non-existing pairs of edges are passed"""

        self.assertRaises(ValueError, lambda: self.graph1.swapStudents("student1","supervisor2","student3","supervisor1"))


    def test_case32(self):
        """Testing the swap function - when 2 non-existing students and supervisors are passed"""

        self.assertRaises(KeyError, lambda: self.graph1.swapStudents("student5","supervisor5","student6","supervisor6"))


    def test_case33(self):
        """Testing the swap function - when 2 existing edges are passed"""
        
        self.graph1.swapStudents("student1","supervisor1","student3","supervisor3")

        result1 = self.graph1.getSupervisors("student3")
        result2 = self.graph1.getSupervisors("student1")

        expected1 = ['supervisor1']
        expected2 = ['supervisor3']

        self.assertEqual((result1,result2),(expected1,expected2))


    def test_case34(self):
        """Testing the swap function - when swaping students of same supervisor"""
        
        self.graph1.swapStudents("student1","supervisor1","student2","supervisor1")

        result1 = self.graph1.getSupervisors("student1")
        result2 = self.graph1.getSupervisors("student2")

        expected1 = ['supervisor1']
        expected2 = ['supervisor1']

        self.assertEqual((result1,result2),(expected1,expected2))

    

    

    

        

        
   
