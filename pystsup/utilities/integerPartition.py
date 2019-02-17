"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: utilities
    File: integerPartition.py
    
    Purpose:  Contains function to partition a particular integer into specified blocks.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""

import random
import copy

def partition(n,m,minQuota,maxQuota):
    """
    Function to partion a particular integer.

    Parameters:
        n (int) - the number we want to partition.
        m (int) - the number of blocks we want.
        minQuota (int) - the minimum size of a block.
        maxQuota (int) - the maximum size of a block.

    Returns:
        result (list) - list of 'm' numbers that sum to 'n': Where no number is lesser than 'minQuota' and greater than 'maxQuota'.
        
    """

    quotas = []

    #Insert random quotas for all
    
    while len(quotas) < m:
        x = random.randint(minQuota,maxQuota)
        quotas.append(x)

    #Shuffle the quotas
    random.shuffle(quotas)

    #Fix the quotas, such that the sum is equal to n.
    
    if sum(quotas) > n:
        #If the sum of quotas is greater than n, we need to reduce some values.

        #Filter values greater than minQuota and equal to minQuota
        
        lt = copy.deepcopy([x for x in quotas if x==minQuota])
        gt = copy.deepcopy([x for x in quotas if x>minQuota])
        
        temp = list()
        req = sum(quotas) - n

        #Decrement the greater than values until we get the sum we want.
        while req > 0:
            x = random.choice(gt)
            gt.remove(x)
            x-=1
            req -= 1
            if x == minQuota:
                temp.append(x)
            else:
                gt.append(x)
                
        
        result = gt + temp + lt
        

    elif sum(quotas) < n:
    
        #If the sum of quotas is lesser than n, we need to increase some values.
        
        req = n - sum(quotas)

        #Filter values lesser than maxQuota and equal than maxQuota
        lt2 = copy.deepcopy([x for x in quotas if x<maxQuota])
        gt2 = copy.deepcopy([x for x in quotas if x==maxQuota])
        
        temp = list()
        

        #Increment the lesser values until we get the sum we want.
        while req > 0:
            
            x = random.choice(lt2)
            lt2.remove(x)
            x+=1
            req-=1
            if x ==maxQuota:
                temp.append(x)
            else:
                lt2.append(x)

        result = gt2 + temp + lt2
        
    else:
        #If its same, then simply return it.
        result = quotas

    return result

    

    
        
    
    
    

    

    
