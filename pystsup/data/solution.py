"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: data
    File: solution.py
    
    Purpose:  Contains Solution class, which encapsulates a biparted graph and fitness values.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""


import numpy
from .bipartiteGraph import BipartiteGraph

class Solution:
    
    def __init__(self,graph=None):
        """
        Initialize the Solution object.

        Parameters:
        
            graph (BipartiteGraph) - graph representing a particular allocation.
        """
        
        if graph:
            self._graph = graph
        else :
            self._graph = BipartiteGraph()


        # Setting variables that will be used in NSGA II
        
        self._Fsup = None
        self._Fst = None
        
        self.dominationCount = None
        self.dominatedSolution = None
        self.rank = None
        self.crowdingDistance = None


    def generateRandomSolution(students, supervisors):
        """
        Function to create a new solution object with a random bipartite graph.

        Parameters:
        
            students - dictionary of all students with their details (id, preferences)
            supervisors - dictionary of all supervisors with their details (id,preferences,quota)

        Returns:

            A Solution Object - new solution object with a graph containing random student-supervisor allocations.  
        """
        
        g = BipartiteGraph.createRandomGraph(students,supervisors)
        
        return Solution(graph=g)


    def getFst(self):
        """Function to get the Student Fitness Value"""
        
        return self._Fst
    
    def getFsup(self):
        """Function to get the Supervisor Fitness Value"""
        
        return self._Fsup

    def setFst(self,Fst):
        """
        Function to set the Student Fitness Value

        Parameters:

            Fst (float) - the student fitness value
        """
        
        self._Fst = Fst

    def setFsup(self,Fsup):
        """
        Function to set the Supervisor Fitness Value

        Parameters:

            Fsup (float) - the supervisor fitness value
        """
        
        self._Fsup = Fsup

    def dominates(self,solution2):
        """
        Function to check if this solution dominates another solution.

        Parameters:
        
            solution2 (Solution) - the solution to compare with.

        Returns:
        
            A Boolean - True if this solution dominates solution2. Otherwise, False.
        """

        #Getting the fitness values from both solutions
        
        sol1Fst = self._Fst
        sol1Fsup = self._Fsup

        sol2Fst = solution2.getFst()
        sol2Fsup = solution2.getFsup()

        #Condition 1 - When both points (Fst, Fsup) of this solution are strictly greater than solution2 points
        cond1 = (sol1Fst > sol2Fst) and (sol1Fsup > sol2Fsup)
        
        #Condition 2 - When Fst of this solution is greater than or equal to and Fsup is stricly greater than
        cond2 = (sol1Fst >= sol2Fst) and (sol1Fsup > sol2Fsup)

        #Condition 3 - When Fst of this solution is strictly greater than and Fsup is greater than or equal to
        cond3 = (sol1Fst > sol2Fst) and (sol1Fsup >= sol2Fsup)

        #If any of those conditions is true it means this solution dominates solution2
        
        if cond1 or cond2 or cond3:
            return True
        else:
            return False

    def __lt__(self,sol2):
        """
        Implementation of NSGA II crowded comparision operator.
        This is to compare if a solution is better than another in terms of its position in front and crowding distance.
        Used in NSGA II when sorting the solutions of the last front and also in tournament selection operator.
        
        Parameters:
        
            sol2 (Solution) - the solution to compare with.

        Returns:
        
            A Boolean - True if this solution is better than sol2. Otherwise, False.
        """

        if isinstance(sol2, Solution):

            cond1 = self.rank < sol2.rank
            cond2 = (self.rank==sol2.rank) and (self.crowdingDistance > sol2.crowdingDistance)

            if cond1 or cond2:
                return True
            else:
                return False


    def __key(self):
        """ 
        Function to return a unique hashable key for the object i.e the bipartite graph
        
        Returns:
            A Bipartite Graph - the graph representing this a particular solution.
        """
        return self._graph

    def __hash__(self):
        """ 
        Function to return a hash value for the object so it can be used with sets, when filtering unique solutions.
        
        Returns:
            hash value - the hash value for a particular instance of this class.
        """
        
        return hash(self.__key())
    
    def __eq__(self,sol2):
        """ 
        Function to compare if two solutions are equal.
        
        Returns:
            A Boolean - True if both the graph's contain exactly same edges. Otherwise, False.
        """
        
        return (self._graph == sol2.getGraph())
        
                
    def calcRankWeights(c=0.5,n=5):
        """
        Function to calculate rank weights for the preferences. The formula applied is from Exponetial Ranking Selection technique.
        These values are used for calculating the keyword similarity between two profiles.

        Parameters:

            n (int) - the number of preferences in a profile (the number of ranks, eg. 5).
            c (float) - a value between 0 and 1.

        Returns:

            rankWeights (dictionary) - with rank as key and its weight as value.
        """
        rankWeights ={}   
        summation = 0
        for i in range(n):
            temp = c**i
            rankWeights[i+1]=temp
            summation+=temp
        for i in rankWeights:
            rankWeights[i] = rankWeights[i]/summation

        return rankWeights


    def _intersection(self,kw1,kw2):
        """
        Function to calculate the number of common elements in two lists.

        Parameters:

            kw1 (list) - the path of a keyword in ACM Classification Tree.
            kw2 (list) - the path of another keyword in ACM Classification Tree.

        Returns:

            count (int) - the number of common keywords in both the paths.
        """
        
        count = 0
        indices = (len(kw1)-1,len(kw2)-1)

        #Start checking from the end of the list until they keywords match
        
        while indices[0]>=0 and indices[1]>=0 :
            if kw1[indices[0]] == kw2[indices[1]] :
                count+=1
                indices = (indices[0]-1,indices[1]-1)
            else:
                break
            
        return count
            


    def kw_similarity(self,studentKeywords,supervisorKeywords,rankWeights):
        """
        Function to calculate the keywords similarity between two profiles.

        Parameters:

            studentKeywords (dictionary) - the rank of a keyword as key and a list with keyword and its path(list) as value.
            supervisorKeywords (dictionary) - the rank of a keyword as key and a list of with keyword and its path(list) as value.
            rankWeights (dictionary) - with rank as key and its weight as value.

        Returns:

            result1 - the value (between 0-1) of how fit "a supervisor" is for "a student".
            result2 - the value (between 0-1) of how fit "a student" is for a "supervisor".
        """
        
        studentKeywords_Size = len(studentKeywords)
        supervisorKeywords_Size = len(supervisorKeywords)
        
        result1 = 0 #fst
        result2 = 0 #fsup

        #Dictionary to keep track of the most similar keyword value and rank similarity values
        
        track = {} #for supervisor fitness
        track2 = {} #for student fitness
        
        for sup_rank in supervisorKeywords:
            
            #index 0 - most similar keyword (supervisor points) value
            #index 1 - rank similairty value for that 'most similar keyword'
            
            track[sup_rank]=[0,0]

        for stu_rank in studentKeywords:
            #index 0 - rank similarity value for the most similar keyword
            
            track2[stu_rank]=0

        for student_rank in studentKeywords:

            
            student_kw = studentKeywords[student_rank][0]
            student_path = studentKeywords[student_rank][1]
            
            curr_max1 =0 #keeps track of the most similar keyword value for student
            
            for supervisor_rank in supervisorKeywords:

                supervisor_path = supervisorKeywords[supervisor_rank][1]
                supervisor_kw = supervisorKeywords[supervisor_rank][0]
                
                common_keywords = self._intersection(student_path,supervisor_path)

                if common_keywords != 0:

                    points1 = common_keywords/len(student_path) #student points
                    points2 = common_keywords/len(supervisor_path) #supervisor points
                
                    rank_Similarity = 1/(1+abs(student_rank-supervisor_rank))

                    curr1 = points1 
                    curr2 = points2

                    #if student points is greater than previous student points then update values
                    
                    if curr1 > curr_max1:
                        curr_max1 = curr1
                        track2[student_rank]=rank_Similarity
                        
                    #if supervisor points is greater than previor supervisor points then update values
                
                    if curr2 > track[supervisor_rank][0]:
                        track[supervisor_rank][0] = curr2
                        track[supervisor_rank][1] = rank_Similarity


            #Sum the values for all the keywords of the student
            result1+= curr_max1*track2[student_rank]*rankWeights[student_rank]

        #Sum the values for all the keywords of the supervisor
        for i in track:
            if track[i]!=0: 
                result2+= track[i][0]*track[i][1]*rankWeights[i]

        return result1,result2
                
        
    def getAverageStructuralFitness(self,supervisors):
        edges =  self._graph.getEdges()
        workloads = []
        for sup in supervisors:
            quota = supervisors[sup].getQuota()
            students_allocated = edges[sup]
            workloads.append( len(students_allocated)/quota )
        wf = numpy.mean(workloads)
        return wf


    def getStructuralFitness(self,supervisors):
        edges =  self._graph.getEdges()
        workloads = []
        for sup in supervisors:
            quota = supervisors[sup].getQuota()
            students_allocated = edges[sup]
            workloads.append( len(students_allocated)/quota )
        wf = numpy.std(workloads)
        return 1/(1+wf)**2
    
    def calcFitness(self, students, supervisors, rankWeights, fitnessCache):
        """
        Function to calculate the Overall Student and Supervisor Fitness Values for a solution (Fst and Fsup).
        This function sets the Fst and Fsup attributes for the solution object.
        
        Parameters:

            studentKeywords (dictionary) - the rank of a keyword as key and a list with keyword and its path(list) as value.
            supervisorKeywords (dictionary) - the rank of a keyword as key and a list of with keyword and its path(list) as value.
            rankWeights (dictionary) - with rank as key and its weight as value.
            fitnessCache(dictionary) - with a student-supervisor pair as key and their keyword similairty score as value.

        """

        quotaSum = 0
        
        edges = self._graph.getEdges()

        fitnessSup_min = float("inf")
        fitnessSup_avg = 0
        n_sup = len(supervisors)
        n_stu = len(students)
        workloads = []

        fitness_st = float("inf")
        summation_Fst = 0
        
        for sup in edges:
            quota = supervisors[sup].getQuota()
            quotaSum+=quota
            students_allocated = edges[sup]
            
            n = len(students_allocated)
            
            temp_total = 0

            workloads.append(n/quota)

            for stu in students_allocated:

                temp_Fst, temp_fsup = fitnessCache[str((stu, sup))] #changed to str because of JSON file saving

                temp_total += temp_fsup

                summation_Fst+=temp_Fst
                
                if temp_Fst < fitness_st:
                    fitness_st = temp_Fst
                    
            average = temp_total/n #For Supervisor Fitness

            if average < fitnessSup_min:
                fitnessSup_min = average
            fitnessSup_avg+=average

        st = self.getStructuralFitness(supervisors)
        fitnessSup = (fitnessSup_avg/n_sup) * st
        if fitnessSup > 1.0 :
            print(fitnessSupi,"hola","tenemos un problema")
            print(fitnessSup_avg,n_sup)
            assert fitnessSup <= 1.0

        self._Fst = summation_Fst/n_stu
        assert self._Fst < 1.0
        if self._Fst > 1.0 :
            print("Hola tenemos otro problema", self._Fst, summation_Fst,n_stu)
            assert self._Fst <= 1.0
        self._Fsup = fitnessSup
        assert self._Fsup < 1.0
        
        

    def transferStudent(self,studentID,fromSup,toSup,supervisors):
        """ 
        Function to transfer a particular student from a supervisor to another supervisor.

        Parameters:
        
            studentID (string) - Student ID.
            
            fromSup (string) - Supervisor ID of the supervisor from which the student is being transferred.
            
            toSup (string) - Supervisor ID of the supervisor to which the student will be transferred to.
            
            supervisors (dictionary) - dictionary of all supervisors with their details (id,preferences,quota)
        
        """
        
        self._graph.transferStudent(studentID,fromSup,toSup,supervisors)
    

    def isValid(self,students,supervisors):
        """"""
        """
        Function to check if the a solution is a valid one for a particular set of students and supervisors.

        Parameters:
        
            students - dictionary of all students with their details (id, preferences)
            supervisors - dictionary of all supervisors with their details (id,preferences,quota)

        Returns:

            A Boolean Value - True if its a valid solution. Otherwise, False. 
        """

        graph = self._graph
        supEdges = graph.getEdges()
        stuEdges = graph.getStuEdges()

        #If the number of students or supervisors is not equal to the ones in data, then it's not a valid solution.

        if (len(supEdges) != len(supervisors)) or (len(stuEdges) != len(students)):
            return False

        for sup in supEdges :

            val = graph.getSupervisorDegree(sup)

            #if supervisors degree in solution is greater than their quota limit or 0,then it's not a valid solution.

            if (val > supervisors[sup].getQuota()) or (val==0):
                return False

            for stu in supEdges[sup]:

                #If supervisor doesn't exist in their student list or the number of supervisors for a student is not 1, then it's not a valid solution.

                if (sup not in graph.getSupervisors(stu)) or (graph.getStudentDegree(stu) != 1):
                    return False
                

        return True
    

    def getTransferable(self,supervisors):
        """
        Function to get the list of supervisors from and to whom we can transfer students.

        Parameters:
        
            supervisors - dictionary of all supervisors with their details (id,preferences,quota)

        Returns:

            canTransferFrom (set) - list of supervisors we can transfer students from (ID's only)
            canTransferTo (set) - list of supervisors we can transfer students to (ID's only)
        
        """
        
        supEdges = self._graph.getEdges()
        allEdges = set(list(supEdges.keys()))
        canTransferFrom = set()
        canTransferTo = set()
        
        for sup in supEdges:

            supDegree = len(supEdges[sup])
            quota = supervisors[sup].getQuota()

            #If supervisor degree is greater than 1 then we can transfer from them
            if (supDegree > 1):
                canTransferFrom.add(sup)

            #If supervisor degree is less than their quota we can transfer to them
            if (supDegree < quota):
                canTransferTo.add(sup)

        return canTransferFrom, canTransferTo


    def getGraph(self):
        """Function to get the bipartite graph"""
        
        return self._graph




    


