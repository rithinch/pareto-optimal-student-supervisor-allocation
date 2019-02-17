import random
from pystsup.data import Solution
from pystsup.data import BipartiteGraph

def crossover10(solution1,solution2):

    #Merging the two Graphs

    graph1 = solution1.getGraph()
    graph2 = solution2.getGraph()

    mergedGraph = graph1.merge(graph2)

    stuEdges = mergedGraph.getStuEdges()
    supEdges = mergedGraph.getEdges()

    cycles = []

    for stu in stuEdges:

        for stu2 in stuEdges:

            if stu != stu2:

                n1 = set(stuEdges[stu])
                n2 = set(stuEdges[stu2])

                if len(n1.intersection(n2))==2:
                    cycles.append((stu,stu2))

    return cycles


    
        
        

    
