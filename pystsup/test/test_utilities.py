"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: test
    File: test_utilities.py
    
    Purpose:  Unit Testing for Utilities Module.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""



import unittest

from pystsup.utilities.acmParser import parseFile,getPath

class UtilitiesTest(unittest.TestCase):

    def test_case1(self):
        """Testing if the outputs of topicNames are correct"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        self.assertEqual(topicNames['Biographies'],7)


    def test_case2(self):
        """Testing if the outputs of topcID's are correct"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        
        self.assertEqual(topicIDs[456],'Buffering')


    def test_case3(self):
        """Testing if the outputs of topicPaths are correct"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        
        self.assertEqual(topicPaths[400],396)


    def test_case4(self):
        """Testing if the ouputs of topicNames are correct"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")

        self.assertEqual(topicNames['Survival analysis'],919)


    def test_case5(self):
        """Testing if the outputs of topicPaths are correct"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")

        self.assertEqual(topicPaths[1],0)
        

    def test_case6(self):
        """Checking if all the topics are stored"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")

        sizes = (len(topicNames),len(topicPaths),len(topicIDs))

        self.assertEqual(sizes,(1908,2075,2075))
        

    def test_case7(self):
        """Testing the getPath function for Survival Analysis - Level 5"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")

        retrievedPath = getPath('Survival analysis',topicNames,topicPaths, topicIDs)

        expectedPath = ['Survival analysis', 'Statistical paradigms', 'Probability and statistics', 'Mathematics of computing','ACM Computing Classification System']

        self.assertEqual(retrievedPath,expectedPath)


    def test_case8(self):
        """Testing the getPath function for Object recognition - Level 6"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")

        retrievedPath = getPath('Object recognition',topicNames,topicPaths, topicIDs)

        expectedPath = ['Object recognition', 'Computer vision problems', 'Computer vision', 'Artificial intelligence', 'Computing methodologies','ACM Computing Classification System']

        self.assertEqual(retrievedPath,expectedPath)


    def test_case9(self):
        """Testing the getPath function for Adolescents - Level 4"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")

        retrievedPath = getPath('Adolescents',topicNames,topicPaths,topicIDs)

        expectedPath = ['Adolescents', 'Age', 'User characteristics', 'Social and professional topics','ACM Computing Classification System']

        self.assertEqual(retrievedPath,expectedPath)


    def test_case10(self):
        """Testing the getPath function for General and reference - Level 2"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        
        retrievedPath = getPath('General and reference',topicNames,topicPaths,topicIDs)

        expectedPath = ['General and reference','ACM Computing Classification System']

        self.assertEqual(retrievedPath,expectedPath)


    def test_case11(self):
        """Testing the getPath function for Architectures - Level 3"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        
        retrievedPath = getPath('Architectures',topicNames,topicPaths,topicIDs)

        expectedPath = ['Architectures','Computer systems organization','ACM Computing Classification System']

        self.assertEqual(retrievedPath,expectedPath)


    def test_case12(self):
        """Testing the getPath function for Contextual software domains - Level 4"""

        topicNames,topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        
        retrievedPath = getPath('Contextual software domains',topicNames,topicPaths,topicIDs)

        expectedPath = ['Contextual software domains','Software organization and properties','Software and its engineering','ACM Computing Classification System']

        self.assertEqual(retrievedPath,expectedPath)

    def test_case13(self):
        """Testing the topics are in correct levels - level 1"""

        topicNames, topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")

        self.assertEqual(levels[1],1)


    def test_case14(self):
        """Testing the topics are in correct levels - level 7"""

        topicNames, topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        tid = topicNames['Message oriented middleware']
        self.assertEqual(levels[tid],7)


    def test_case15(self):
        """Testing the topics are in correct levels - level 3"""

        topicNames, topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        tid = topicNames['Software organization and properties']
        self.assertEqual(levels[tid],3)


    def test_case16(self):
        """Testing the topics are in correct levels - level 4"""

        topicNames, topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        tid = topicNames['Probabilistic computation']
        self.assertEqual(levels[tid],4)

    def test_case17(self):
        """Testing the topics are in correct levels - level 5"""

        topicNames, topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        tid = topicNames['Dynamic graph algorithms']
        self.assertEqual(levels[tid],5)

    def test_case18(self):
        """Testing the topics are in correct levels - level 6"""

        topicNames, topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        tid = topicNames['Linear programming']
        self.assertEqual(levels[tid],6)

    def test_case19(self):
        """Testing the topics are in correct levels - level 7"""

        topicNames, topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        tid = topicNames['CS1']
        self.assertEqual(levels[tid],7)

    def test_case20(self):
        """Testing the topics are in correct levels - level 3"""

        topicNames, topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        tid = topicNames['Artificial intelligence']
        self.assertEqual(levels[tid],3)


    def test_case21(self):
        """Testing the topics are in correct levels - level 5"""

        topicNames, topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        tid = topicNames['Adolescents']
        self.assertEqual(levels[tid],5)


    def test_case22(self):
        """Testing the topics are in correct levels - level 2"""

        topicNames, topicPaths, topicIDs,levels = parseFile("pystsup/test/acm.txt")
        tid = topicNames['Security and privacy']
        self.assertEqual(levels[tid],2)

        
        


    

    
        
        
        
