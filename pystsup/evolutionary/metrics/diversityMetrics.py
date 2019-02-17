"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: evolutionary/metrics
    File: diversityMetrics.py
    
    Purpose:  Contains implementations of diversity metrics.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""



def calcSpacing(front):
    """
    Implementation of spacing metric (S) by Schott.

    The lower the Spacing value the better the algorithm.
    """

    n = len(front)

    if n <= 2:
        return 0

    d = []

    for sol in front:

        curr = float("inf")
        
        fst1 = sol.getFst()
        fsup1 = sol.getFsup()
        
        for sol2 in front:

            if sol != sol2:

                fst2 = sol2.getFst()
                fsup2 = sol2.getFsup()

                val = abs(fst1-fst2) + abs(fsup1-fsup2)

                if val < curr:

                    curr = val
        
        d.append(curr)
    
    dAvg = sum(d)/n

    temp = 0

    for val in d:

        temp += (val-dAvg)**2


    temp *= 1/n

    spacing = (temp)**(1/2)

    return spacing

    

        

    

                

                

                

    
