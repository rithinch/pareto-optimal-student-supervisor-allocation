"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: data
    File: bipartiteGraph.py
    
    Purpose:  Contains BipartiteGraph class, which represents a particular possible allocation of students and supervisors.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""


import random
import copy


class BipartiteGraph:
    
    def __init__(self,edges=None,edges_Stu=None):
        """
        Initialize the BipartiteGraph object.

        Parameters:
        
            edges (dictionary) -  key = supervisor ID
                                  value = list of allocated students for that supervisor(ID's only).
                              
            edges_Stu (dictionary) -  key = student ID
                                      value = a list of supervisors for that student (ID's only).
                                      Usually contains 1 supervisor, but after merging two graphs the list can contain at the most 2 supervisors.
        
        """

        if edges_Stu:
            self._edgesStu = edges_Stu
        else:
            self._edgesStu = {}
            
        if edges:
            self._edges = edges
        else:
            self._edges = {}


    def convertToTuple(self,edges):
        """ 
        Function to convert values of a dictionary into a tuple.
        
        Parameters:
            edges (dictionary)-  the dictionary for which the values are to be converted into a tuple.
        
        Returns:
            d (dictionary) - the converted dictionary with values of type tuple.
        """
        
        d = {}
        for key,val in edges.items():
            d[key] = tuple(val)

        return d

    
    def __key(self):
        """ 
        Function to return a unique hashable key for the object i.e the student edges dictionary.
        
        Returns:
            a frozenset object - contains the (key,value) pairs of the student edges dictionary.
        """

        d = self.convertToTuple(self._edgesStu)
        
        return frozenset(d.items())


    def __hash__(self):
        """ 
        Function to return a hash value for the object so it can be used with sets, when filtering unique solutions.
        
        Returns:
            hash value - the hash value for a particular instance of this class.
        """

        return hash(self.__key())

    
    def __eq__(self,graph2):
        """ 
        Function to compare if two bipartite graphs are equal.
        
        Returns:
            A Boolean - True if both the graph's contain exactly same edges. Otherwise, False.
        """
        
        return self._edgesStu == graph2.getStuEdges()
    

    def addEdge(self,supervisor,student):
        """ 
        Function to add a new edge to the bipartite graph.
        
        Parameters:
        
            supervisor (string)-  the supervisor ID.
            student (string) - the student ID.
        
        
        """

        #Adding only if it is a new edge
        
        if (self.isEdge(supervisor,student) == False):
            
            if self.supervisorExists(supervisor):
                self._edges[supervisor].append(student)
            else:
                self._edges[supervisor] = [student]

            if self.studentExists(student):
                self._edgesStu[student].append(supervisor)
            else:
                self._edgesStu[student] = [supervisor]



    def removeEdge(self,supervisor,student):
        """ 
        Function to remove a particular edge in the bipartite graph.
        
        Parameters:
            supervisor (string)-  the supervisor ID.
            student (string) - the student ID.
        
        Raises:
            KeyError - if the supervisor/student don't exist in the graph
            ValueError - if the edge does not exist in the graph.
        """
        
        self._edges[supervisor].remove(student)
        self._edgesStu[student].remove(supervisor)


    def isEdge(self,supervisor,student):
        """ 
        Function to check if an edge exists in the bipartite graph.
        
        Returns:
            A Boolean - True if the edge exists. Otherwise, False.
        """
        
        try:
            if (student in self._edges[supervisor]) and (supervisor in self._edgesStu[student]):
                return True
            else:
                return False
            
        except KeyError:
            return False



    def supervisorExists(self,supervisor):
        """ 
        Function to check if a supervisor exists in the bipartite graph.
        
        Returns:
            A Boolean - True if the supervisor exists. Otherwise, False.
        """
        
        if supervisor in self._edges:
            return True
        else:
            return False

        

    def studentExists(self,student):
        """ 
        Function to check if a student exists in the bipartite graph.
        
        Returns:
            A Boolean - True if the student exists. Otherwise, False.
        """

        if student in self._edgesStu:
            return True
        else:
            return False
        

    def getStudents(self,supervisor):
        """ 
        Function to get the list of allocated students for a particular supervisor.

        Parameters:
            supervisor (string) - Supervisor ID.
        
        Returns:
            A List - containing all the students allocated for that supervisor.
        """
        
        return self._edges[supervisor]


    def getSupervisors(self,student):
        """ 
        Function to get the list of allocated supervisors for a particular student.

        Parameters:
            student (string) - Student ID.
        
        Returns:
            A List - containing the supervisors allocated for that student (min 1, max 2).
        """
        
        return self._edgesStu[student]

    
    def getSupervisorDegree(self,supervisor):
        """ 
        Function to get the number of students allocated for a particular supervisor.

        Parameters:
            supervisor (string) - Supervisor ID.
        
        Returns:
            An Integer - the number of students allocated for that supervisor.
        """
        
        return len(self._edges[supervisor])

    def getStudentDegree(self,student):
        """ 
        Function to get the number of supervisors allocated for a particular student.

        Parameters:
            student (string) - Student ID.
        
        Returns:
            An Integer - the number of supervisors allocated for that student.
        """
        
        return len(self._edgesStu[student])
    

    def createRandomGraph(students,supervisors):
        """
        Function to create a random bipartite graph.

        Parameters:
        
            students - dictionary of all students with their details (id, preferences)
            supervisors - dictionary of all supervisors with their details (id,preferences,quota)

        Returns:

            A BipartiteGraph Object - new graph object with random student-supervisor allocations.  
        """

        edges_Sup = {}
        edges_Stu = {}

        students_left = dict(students)
        
        supervisors_left = dict(supervisors)

        #Allocating a single student to a supervisor

        for sup in supervisors:
            
            supId = supervisors[sup].getSupervisorID()
            quota = supervisors[sup].getQuota()
            stuId = random.choice(list(students_left.keys()))

            #Adding the edge to graph
            edges_Sup[supId] = [stuId]
            edges_Stu[stuId] = [supId]
            
                    
            #Removing the allocated student
            del students_left[stuId]

            #Checking whether to remove supervisor or not
            if len(edges_Sup[supId]) >= quota:
                del supervisors_left[sup]


        #Allocating random students for random supervisors

        while len(students_left) > 0:

            supId = random.choice(list(supervisors_left.keys()))     
            quota = supervisors_left[supId].getQuota()
            stuId = random.choice(list(students_left.keys()))

            #Adding the edge to graph
            
            edges_Sup[supId].append(stuId)
            edges_Stu[stuId] = [supId]
            
            
            del students_left[stuId]
            
            if len(edges_Sup[supId]) >= quota:
                del supervisors_left[supId]
        

        return BipartiteGraph(edges_Sup,edges_Stu)



    def transferStudent(self,studentID,fromSup,toSup, supervisors):
        """ 
        Function to transfer a particular student from a supervisor to another supervisor.

        Parameters:
        
            studentID (string) - Student ID.
            
            fromSup (string) - Supervisor ID of the supervisor from which the student is being transferred.
            
            toSup (string) - Supervisor ID of the supervisor to which the student will be transferred to.
            
            supervisors (dictionary) - dictionary of all supervisors with their details (id,preferences,quota)
        
        """

        #Transfers only when the following conditions are met i.e when a transfer is possible
        
        if (self.getSupervisorDegree(fromSup)>=2) and (self.getSupervisorDegree(toSup) + 1 <= supervisors[toSup].getQuota()):

            if (self.studentExists(studentID)) and (self.isEdge(fromSup,studentID)):
                
                self.addEdge(toSup,studentID)
                self.removeEdge(fromSup,studentID)

    

    def transferStudent1(self,studentID,fromSup,toSup, supervisors):

        """ 
        Function to transfer a particular student from a supervisor to another supervisor.
        This is a modified version of the transfer function. This function doesn't check any conditions.
        It is assuming that valid parameters are passed.
        

        Parameters:
        
            studentID (string) - Student ID.
            
            fromSup (string) - Supervisor ID of the supervisor from which the student is being transferred.
            
            toSup (string) - Supervisor ID of the supervisor to which the student will be transferred to.
            
            supervisors (dictionary) - dictionary of all supervisors with their details (id,preferences,quota)
        
        """
        
        self.addEdge(toSup,studentID)
        self.removeEdge(fromSup,studentID)


    def swapStudents(self,student1,supervisor1,student2,supervisor2):

        """ 
        Function to swap a particular student from a supervisor with another student from another supervisor.

        Parameters:
        
            student1 (string) - Student ID of the first student.
            
            supervisor1 (string) - Supervisor ID of the supervisor from which student1 is being swapped.

            student2 (string) - Student ID of the second student.

            supervisor2 (string) - Supervisor ID of the supervisor from which student2 is being swapped.
        
        """
        
        self.removeEdge(supervisor1,student1)
        self.removeEdge(supervisor2,student2)
        self.addEdge(supervisor1,student2)
        self.addEdge(supervisor2,student1)


    def getStructure(self):
        """
        Function to get structure of the bipartite graph.

        Returns:

            structure (dictionary) - a dictioary with supervisorID's as keys and the number of students they supervise as values. 
        """
        

        structure = {}

        for sup in self._edges:
            structure[sup] = len(self._edges[sup])

        return structure

    def merge(self,graph2):
        """
        Function to merge two biparted graphs.

        Parameters:
        
            graph2 (BipartiteGraph) - the graph which is to be merged with.

        Returns:
        
            A BipartiteGraph Object - new graph object with merged edges from both graphs.
        """

        #Making a deepcopy so that the original graph edges are not disturbed.
        
        graph2_Edges = copy.deepcopy(graph2.getEdges()) #Get graph2 edges
        edges_Stu = copy.deepcopy(self._edgesStu)
        edges_Sup = copy.deepcopy(self._edges)
        
        for sup in edges_Sup:
            a = set(edges_Sup[sup]) #Get Students in graph1
            b = set(graph2_Edges[sup]) #Get students in graph2

            #Get thier difference, and the ones that are not present in graph1 to graph1
            
            for stu in (b.difference(a)):
                edges_Sup[sup].append(stu)
                edges_Stu[stu].append(sup)
                
        return BipartiteGraph(edges_Sup,edges_Stu)


    def getRemainingSup(self,supervisor,student):
        """
        Function to get the other supervisor for a student. Given that a student has 2 supervisors from the merged graph.

        Parameters:
        
            supervisor (string) - the Supervisor ID of the supervisor that we want to exclude.
            student (string) - the Student ID of the student that we want to get the other supervisor from.

        Returns:
        
            sup (string) - the supervisor ID of the other supervisor.
        """
        
        for sup in self._edgesStu[student]:
            if sup != supervisor:
                return sup

    def removeExcept(self,supervisor,student):
        """
        Function to Remove every supervisor except the passed supervisor in students list.

        Parameters:
        
            supervisor (string) - the Supervisor ID of the supervisor that we dont' want to remove.
            student (string) - the Student ID of the student that we want to remove supervisor's from.
        """
        
        for sup in self._edgesStu[student]:
            if sup != supervisor:
                self.removeEdge(sup,student)


    def removeExceptSup(self,supervisor,student, reqStructure):
        """
        Function to Remove every student except the passed student in supervisor's list.

        Parameters:
        
            supervisor (string) - the Supervisor ID of the supervisor that we want to remove students's from.
            student (string) - the Student ID of the student that we dont' want to remove.
            reqStructure (string) - is the structured we are trying to achieve from a crossover operator.
        """
        
        for stu in self._edges[supervisor]:
            if stu != student and (self.getSupervisorDegree(supervisor) -1 >= reqStructure):
                self.removeEdge(supervisor,stu)
                

    def getRemainingStu(self,supervisor,studentList):
        """
        Function to get all the students in supervisors List except the students the passed in studentList.

        Parameters:
        
            supervisor (string) - the Supervisor ID of the supervisor that we want to students's from.
            studentList (List) - the list of students that we want want to keep.

        Returns:
        
            toRemove (set) - the set of all students that are not in studentList.
        """

        
        stuList = set(self._edges[supervisor])
        toRemove = stuList - set(studentList)

        
        #toRemove = set()
        #for stu in self._edges[supervisor]:
            #if stu not in studentList:
                #toRemove.add(stu)

        return toRemove
    
    
    def canLock(self,sup,stu,structure,counts,lockedVertices):
        """
        Function to check if we can lock a particular edge or not.

        Parameters:
        
            sup (string) - the Supervisor ID.
            stu (string) - the Student ID.
            structure (dictionary) - the structure we are trying to achieve from crossover.
            counts (dictionary) - the current sturucture of the graph.
            lockedVertices (set) - the set of all locked vertices.

        Returns:
        
            A boolean - True if we can lock the edge. Otherwise False.
            
        """

        #If the student has only 1 supervisor, it has to be locked.
        
        if self.getStudentDegree(stu) == 1:
            return True
        
        else:
            
            remainingSup = self.getRemainingSup(sup,stu) #Get the other supervisor
            stuList = set(self.getStudents(remainingSup)) #Get the list of students of the other supervisor
            
            #availableStu = self.getAvailableEdges(remainingSup,lockedVertices) 

            availableStu = stuList - lockedVertices #Get list of students that are not locked from the other supervisor
            
            if (structure[remainingSup]-counts[remainingSup]) < len(availableStu):
                return True
            else:
                return False
            

    def getAvailableEdges(self,sup,lockedVertices):
        """Function to get the list of students of a supervisor that are not in lockedVertices"""

        available = set()
        students = self.getStudents(sup)

        for stu in students:
            if stu not in lockedVertices:
                available.add(stu)

        return available
    

    def getNumberofEdges(self):
        """Function to get the number of edges"""
        return sum(list(self.getStructure().values()))
    
    def getEdges(self):
        """Function to get the edges of the graph with supervisor ID's as key"""
        return self._edges

    def getStuEdges(self):
        """Function to get the edges of the graph with student's ID as key"""
        return self._edgesStu

    def copy(self):
        """Function to create a copy of the bipartite graph"""
        
        edges_Stu = copy.deepcopy(self._edgesStu)
        edges_Sup = copy.deepcopy(self._edges)
                
        return BipartiteGraph(edges_Sup,edges_Stu)
    

    def getAllEdges(self):
        """Return a set of all the edges in tuples format"""

        allEdges = set()
        for sup in self._edges:
            for stu in supEdges[sup]:
                allEdges.add((stu,sup))

        return allEdges
                

