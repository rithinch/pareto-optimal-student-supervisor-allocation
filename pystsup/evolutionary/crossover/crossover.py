"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: evolutionary/crossover
    File: crossover.py
    
    Purpose:  Contains the crossover opearators.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""

import random
from pystsup.data import Solution
from pystsup.data import BipartiteGraph
from hopcroftkarp import HopcroftKarp
import copy

def simplify(graph,structure,to_check=None,already_set=None):
   
    to_keep = []
    if not already_set:
        already_set = set()
    stuEdges = graph.getStuEdges()
    supEdges = graph.getEdges()

    if not to_check :
        to_check = set()
        for stu in stuEdges :
            to_check.add( ("stu",stu) )
        for sup in supEdges :
            to_check.add( ("sup",sup) )


    while to_check :
        (s_type,s_id) = to_check.pop()
        if (s_type,s_id) in already_set :
            continue
        if s_type == "stu" :
            if len(stuEdges[s_id]) == 0 :
                already_set.add( ("stu",s_id) ) 
            if len(stuEdges[s_id]) == 1 :
                sup = stuEdges[s_id][0]
                to_keep.append( (sup,s_id) )
                graph.removeEdge( sup, s_id )
                structure[sup] = structure[sup] - 1
                if not ("sup", sup) in already_set :
                    to_check.add( ("sup",sup) )
                already_set.add( ("stu",s_id) )
        else :
            e = list(supEdges[s_id])
            if structure[s_id] == 0 :
                already_set.add( ("sup",s_id) )
                for stu in e :
                    graph.removeEdge(s_id,stu)
                    to_check = to_check.union( ("stu",x) for x in e )
            elif len(e) == structure[s_id] and structure[s_id]>0 :
                for stu in e :
                    to_keep.append( (s_id,stu) )
                    aux=set( ("sup", x) for x in list(stuEdges[stu]) if (not ("sup",x) in already_set) and x!=s_id   )
                    to_check = to_check.union( aux )
                    graph.removeExcept(s_id,stu)
                    graph.removeEdge(s_id,stu)    
                    already_set.add( ("stu",stu) )
                

                structure[s_id] = 0
                already_set.add( ("sup",s_id) )


    return to_keep,already_set
            
def is_4_cycle(stu,graph):
    supervisors = graph.getStuEdges()[stu]
    if len(supervisors)!=2:
        return False
    supEdges = graph.getEdges()
    s1 = set( supEdges[supervisors[0]] )
    s2 = set( supEdges[supervisors[1]] )
    si = s1.intersection(s2)
    if len(si) >= 2 :
        return True

def solve_4_cycle(stu,structure,graph,already_set=None):
    #print("Solving 4 cycle for student",stu)
    supervisors = graph.getStuEdges()[stu] #We know it is only 2 supervisors because we only merge 2 solutions!
    supEdges = graph.getEdges()
    sup1 = supervisors[0]
    sup2 = supervisors[1]
    #print("Involved supervisors are",sup1,sup2)

    to_keep = []
    if not already_set :
        already_set = set()
    to_check = set()

    #Who gets the sudent
    selected = supervisors[random.randint(0,1)]
    to_keep.append( (selected,stu) )
    structure[selected] = structure[selected]-1
    graph.removeEdge( sup1,stu )
    graph.removeEdge( sup2, stu )
    already_set.add( ("stu",stu) )
    to_check.add(  ("sup",sup1) )
    to_check.add( ("sup",sup2) )

    #common_students = [ x for x in st1.intersection(st2).difference( [stu] ) ]
    #print("Common students aside from ",stu,"is ",common_students)
    #random.shuffle(common_students)
    #cycle_to_solve = [stu,common_students[0]]
    #print("Cycle to be solved is ",cycle_to_solve)
    #random.shuffle(cycle_to_solve)
    #let_go1 = len(supEdges[sup1]) - structure[sup1]
    #let_go2 = len(supEdges[sup2]) - structure[sup2]
    #print(sup1,"can let go",let_go1," and ",sup2, "can let go",let_go2)
    #operations = [ (0,2), (2,0), (1,1) ]
    #random.shuffle(operations)
    #for operation in operations :
    #    if let_go1 >= 2-operation[0] and structure[sup1]>=operation[0] and let_go2 >= 2-operation[1] and structure[sup2]>=operation[1] : #Valid operation :D
            #print("Operation to be carried out is ",operation)
    #        if operation[0] == 2  :
    #            to_keep.append( (sup1,cycle_to_solve[0]) )
    #            to_keep.append( (sup1,cycle_to_solve[1]) )
                #print(sup1,"keeps ",cycle_to_solve[0],cycle_to_solve[1])
    #            structure[sup1] = structure[sup1] - 2
    #        elif operation[0] == 1  :
    #            to_keep.append( (sup1,cycle_to_solve[0]) )
    #            to_keep.append( (sup2,cycle_to_solve[1]) )
                #print(sup1,"keeps ",cycle_to_solve[0]," and ",sup2, "keeps",cycle_to_solve[1])
    #            structure[sup1] = structure[sup1] - 1
    #            structure[sup2] = structure[sup2] - 1
    #        elif operation[1] == 2  :
    #            to_keep.append( (sup2,cycle_to_solve[0] ) )
    #            to_keep.append( (sup2,cycle_to_solve[1] ) )
                #print(sup2,"keeps ",cycle_to_solve[0],"and ",cycle_to_solve[1])
    #            structure[sup2] = structure[sup2] - 2
    #        break
    #graph.removeEdge(sup1,cycle_to_solve[0])
    #graph.removeEdge(sup1,cycle_to_solve[1])
    #graph.removeEdge(sup2,cycle_to_solve[0])
    #graph.removeEdge(sup2,cycle_to_solve[1])
    #already_set.add( ("stu",cycle_to_solve[0]) )
    #already_set.add( ("stu",cycle_to_solve[1]) )
    #to_check.add( ("sup",sup1) )
    #to_check.add( ("sup",sup2) )
    return to_keep, to_check, already_set

def random_allocation(stu,structure,graph,already_set=None):
    #print("Setting",stu,"in",graph.getEdges(),"with structure",structure,"having set",already_set)
    if not already_set :
        already_set = set()
    supervisors = list(graph.getStuEdges()[stu])
    #print("Associated supervisors are",supervisors)
    supEdges = graph.getEdges()
    
    selected = random.randint(0,1)
    sup = supervisors[selected]
    #print("Selected supervisor is",sup)
    to_keep = [ (sup,stu) ]
    structure[sup] = structure[sup]-1
    #print(supervisors)
    #print(supervisors[0])
    #print(supervisors[1])
    #print("Trying to remove",supervisors[0],stu,"from ",graph.getEdges())
    graph.removeEdge(supervisors[0],stu)
    #print(supervisors)
    #print("Trying to remove", supervisors[1],stu,"from ",graph.getEdges())
    graph.removeEdge(supervisors[1],stu)
    to_check= set()
    to_check.add( ("sup",supervisors[0]) )
    to_check.add( ("sup",supervisors[1]) )
    e = list(supEdges[sup])
    for student in e :
        #print("I should also check",student)
        to_check.add( ("stu",student) )
    already_set.add( ("stu",stu) )
    return to_keep, to_check, already_set

    
def hopkroft(graph,structure) :
    transformed_graph = {}
    
    supervisors = graph.getEdges()
    students = graph.getStuEdges()
    correspondence = {}
    sup_name = 0
    list_supervisors = [supervisor for supervisor in supervisors]
    list_students = [student for student in students]
    random.shuffle(list_supervisors)
    random.shuffle(list_students)
    a_to_b = {}
    for i in range(len(list_students)) :
        a_to_b[list_students[i]] = 'stu' + str(i)
    
    for supervisor in list_supervisors :
        cardinality = structure[supervisor]
        for i in range(cardinality) :
            for stu in supervisors[supervisor] :
                transformed_graph.setdefault(sup_name,set()).add( a_to_b[stu] )
            correspondence[sup_name] = supervisor
            sup_name = sup_name + 1
    m = HopcroftKarp(transformed_graph).maximum_matching()

    result = BipartiteGraph()
    for student in students :
       sup_code = m[ a_to_b[student] ]
       result.addEdge( correspondence[sup_code], student )
    return result




def sp_crossover(solution1,solution2,supervisors=None,students=None,k=None):
    #print("New case!!")
    graph1 = solution1.getGraph()
    graph2 = solution2.getGraph()
    already_set=set()

    mergedGraph = graph1.merge(graph2)

    stf1 = solution1.getStructuralFitness(supervisors)
    stf2 = solution2.getStructuralFitness(supervisors)

    if random.random() <= (stf1)/(stf1+stf2) :
        structure = graph1.getStructure()
    else :
        structure = graph2.getStructure()

    original_structure = dict(structure)

    result = hopkroft(mergedGraph,original_structure)
    return Solution(result) 
    #rsupEdges = result.getEdges()
    #different_students = set()
    #for sup in rsupEdges :
        #print(sup,rsupEdges[sup],original_structure[sup])
    #    assert len(rsupEdges[sup]) == original_structure[sup]
    #    for stu in rsupEdges[sup] :
    #        different_students.add(stu)
    #        assert stu in graph1.getEdges()[sup] or stu in graph2.getEdges()[sup]
    #assert len(different_students) == len(graph1.getStuEdges())

    


def crossover(solution1,solution2,supervisors=None,students=None,k=None):
    """
    Function to perfrom crossover on two solutions.

    Parameters:
    
        solution1 (Solution) - parent solution 1
        solution2 (Solution) - parent solution 2

    Returns:

        A New Solution Object - an offspring solution from both the parent solutions.
    """
    
    #Merging the two Graphs

    graph1 = solution1.getGraph()
    graph2 = solution2.getGraph()

    mergedGraph = graph1.merge(graph2)

    stuEdges = mergedGraph.getStuEdges()
    supEdges = mergedGraph.getEdges()

    
    #Randomly getting the structure from the two graphs
    stf1 = solution1.getStructuralFitness(supervisors)
    stf2 = solution2.getStructuralFitness(supervisors)

    if random.random() <= (stf1)/(stf1+stf2) :
        structure = graph1.getStructure()
    else :
        structure = graph2.getStructure()

    lockedEdges = set()
    lockedVertices = set()

    allStudents = set(list(stuEdges.keys()))

    result = BipartiteGraph()

    counts = {} #stores the degree of the supervisors in the new offspring graph

    for sup in supEdges:
        counts[sup] = 0

    #Simplify first time here
    simplified = True
    prev_count = {}
    while prev_count != counts :
        prev_count = dict(counts)
        for sup in supEdges:
            supDegree = len(supEdges[sup])
            reqDegree = structure[sup]
            for stu in supEdges[sup]:

                if len(stuEdges[stu]) == 1 and not stu in lockedVertices:
                    mergedGraph.removeExcept(sup,stu)
                    result.addEdge(sup,stu)
                    lockedVertices.add(stu)
                    counts[sup]+=1

                    if counts[sup]==reqDegree:
                        toKeep = result.getStudents(sup)
                        toRemove = mergedGraph.getRemainingStu(sup,toKeep)

                        for i in toRemove:
                            mergedGraph.removeEdge(sup,i)

    prev = set()
    toContinue = False
    
    while len(lockedVertices) != len(stuEdges):

        for sup in supEdges:

            #If the supervisor degree is not equal to degree we want
            if counts[sup] != structure[sup]:
                
                supDegree = mergedGraph.getSupervisorDegree(sup)
                reqSupDegree = structure[sup]
                students = mergedGraph.getStudents(sup)

                #Pick a random student that is not locked from the supervior's list of students
                curr = random.choice(students)
                if (curr not in lockedVertices):

                    #If that edge can be locked, then lock it.
                    if mergedGraph.canLock(sup,curr,structure,counts,lockedVertices):

                        #Remove other supervisors in student's list of supervisors
                        
                        mergedGraph.removeExcept(sup,curr)

                        #Add it to the new graph and also locked vertices
                        result.addEdge(sup,curr)
                        lockedVertices.add(curr)

                        #Increment the degree of the supervisor
                        counts[sup]+=1

                        #If the degee is the degree we want
                        if counts[sup] == reqSupDegree:
                            
                            toKeep = result.getStudents(sup) #Get the students we want to keep
                            toRemove = mergedGraph.getRemainingStu(sup,toKeep) #Get students we dont want to keep
                            
                            #Remove those students (edges)
                            
                            for stu in toRemove:
                                mergedGraph.removeEdge(sup,stu)

        #If we can lock any further, then we break the loop
        if len(prev) != len(lockedVertices):
            prev = set(list(lockedVertices))
        else:
            toContinue = True
            break

    #Allocate remaining students to supervisors that don't meet the required degree
    if toContinue:
        availableStudents = allStudents.difference(lockedVertices)
        for sup in supEdges:
            reqDegree = structure[sup]
            supDegree = counts[sup]
            supNeeds = reqDegree - supDegree
            if supDegree != reqDegree:
                toAdd = random.sample(availableStudents,supNeeds)
                for stu in toAdd:
                    result.addEdge(sup,stu)
                    lockedVertices.add(stu)
                    counts[sup]+=supNeeds
                    availableStudents.remove(stu)
                     
    return Solution(result)


def fixSolution(graph,supervisors,students):

    supEdges = graph.getEdges()
    
    #Checking supervisors that must reduce, and who can get students
    needs = set()
    can_get = {}
    has_reduce = {}
    can_give = {}
    for supervisor in supervisors :
        if not supervisor in supEdges :
            needs.add(supervisor)
            can_get[supervisor] = supervisors[supervisor].getQuota()
        else :
            now = len(supEdges[supervisor])
            quota = supervisors[supervisor].getQuota()
            if now > 1 :
                can_give[supervisor] = now - 1
            if now > quota :
                has_reduce[supervisor] = now - quota
            if now < quota :
                can_get[supervisor] = quota - now
    
    while needs :
        sup1 = random.choice(list(needs))
        if has_reduce :
            where = list(has_reduce.keys())
        else :
            where = list(can_give.keys())
        sup2 = random.choice(where)
        to_transfer = random.choice(supEdges[sup2])
        graph.removeEdge(sup2,to_transfer)
        graph.addEdge(sup1,to_transfer)
        if can_give[sup2] - 1 == 0:
            del can_give[sup2]
        else :
            can_give[sup2] = can_give[sup2] - 1
        if sup2 in has_reduce and has_reduce[sup2] - 1 == 0:
            del has_reduce[sup2]
        elif sup2 in has_reduce :
            has_reduce[sup2] = has_reduce[sup2] - 1
        needs.remove(sup1)
        if can_get[sup1] - 1  == 0:
            del can_get[sup1]
        else :
            can_get[sup1] = can_get[sup1] - 1

    while has_reduce : #while has to reduce
        sup1 = random.choice(list(has_reduce.keys()))
        sup2 = random.choice(list(can_get.keys()))
        to_transfer = random.choice(supEdges[sup1])
        graph.removeEdge(sup1,to_transfer)
        graph.addEdge(sup2,to_transfer)
        if has_reduce[sup1] - 1 == 0:
            del has_reduce[sup1]
        else :
            has_reduce[sup1] = has_reduce[sup1] - 1
        if can_get[sup2] - 1 == 0 :
            del can_get[sup2]
        else :
            can_get[sup2] = can_get[sup2] - 1


def uniform(solution1,solution2,supervisors,students,k=None):
    """
    An implementation of uniform crossover
    """
    graph1 = solution1.getGraph()
    graph2 = solution2.getGraph()

    stuEdges1 = graph1.getStuEdges()
    stuEdges2 = graph2.getStuEdges()

    g = BipartiteGraph()
    for stu in students :
        if random.random() < 0.5 :
            sup = stuEdges1[stu][0]
        else :
            sup = stuEdges2[stu][0]
        g.addEdge(sup,stu)

    fixSolution(g,supervisors,students)
    return Solution(g)

def kPoint(solution1,solution2,supervisors,students,k=5):
    """
    An Implementation of K-Point crossover for this problem.
    """
    graph1 = solution1.getGraph()
    graph2 = solution2.getGraph()

    stuEdges1 = graph1.getStuEdges()
    stuEdges2 = graph2.getStuEdges()
    supEdges1 = graph1.getEdges()
    
    #Randomly getting the structure from the two graphs
    
    num = random.randint(1,2)
    if num == 1:
        structure = graph1.getStructure()
    else:
        structure = graph2.getStructure()

    #Setting up the vectors
    
    students = list(stuEdges1.keys())
    sol1 = []
    sol2 = []
    for i in range(len(students)):
        sol1.append(stuEdges1[students[i]][0])
        sol2.append(stuEdges2[students[i]][0])


    #Dividing the both solutions into k-points
        
    sol1Points = []
    sol2Points = []

    points = sorted(random.sample(range(1,len(students)),k))
    curr = 0
    
    for i in range(k-1):
        sol1Points.append(sol1[curr:points[i]])
        sol2Points.append(sol2[curr:points[i]])
        curr=points[i]

    sol1Points.append(sol1[curr:])
    sol2Points.append(sol2[curr:])


    #Perform the crossover
    
    result = []

    if k==0:
        n=random.randint(1,2)
        if n==1:
            result = sol1
        else:
            result = sol2

    else:
        
        for point in range(k):
            n = random.randint(1,2)
            if n == 1:
                result.extend(sol1Points[point])
            else:
                result.extend(sol2Points[point])


    graph = BipartiteGraph()
    for i in range(len(students)):
        graph.addEdge(result[i],students[i])

    
    fixSolution(graph,supervisors,students)
        #supEdges = graph.getEdges()
        #availableStudents = set()
        #reqSup = set(list(supEdges1.keys())).difference(set(list(supEdges.keys())))
        
        #sol3 = Solution(graph)
        #canTransferFrom,canTransferTo = sol3.getTransferable(supervisors)
        
        #for sup in supEdges:
        #    supDegree = len(supEdges[sup])
        #    supQuota = supervisors[sup].getQuota()
        #    if supDegree > supQuota:
        #        excess = supDegree - supQuota
        #        for i in random.sample(supEdges[sup],excess):
        #            availableStudents.add(i)
        #    elif supDegree == 0:
        #        reqSup.add(sup)

        #for sup in reqSup:
            
        #    if len(availableStudents)==0:
        #        fromSup = random.choice(list(canTransferFrom))
        #        stu = random.choice(graph.getStudents(fromSup))
        #        availableStudents.add(stu)
            
        #    x = random.choice(list(availableStudents))
        #    availableStudents.remove(x)
        #    oldSup = graph.getSupervisors(x)[0]
        #    graph.transferStudent1(x,oldSup,sup,supervisors)

        #sol3 = Solution(graph)
        #canTransferFrom,canTransferTo = sol3.getTransferable(supervisors)
    
        #for stu in availableStudents:
        #    con = False
        #    oldSup = graph.getSupervisors(stu)[0]

        #    if oldSup in canTransferTo:
        #        canTransferTo.remove(oldSup)
        #        con=True
           
        #    toSup = random.choice(list(canTransferTo))

        #    graph.transferStudent1(stu,oldSup,toSup,supervisors)

        #    if con:
        #        canTransferTo.add(oldSup)
        
        #    if not(graph.getSupervisorDegree(toSup) < supervisors[toSup].getQuota()):
        #        canTransferTo.remove(toSup)


    return Solution(graph)



