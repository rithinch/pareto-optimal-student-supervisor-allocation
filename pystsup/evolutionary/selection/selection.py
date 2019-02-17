"""
    An AI Tool for Student-Supervisor Allocation.
    
    Package: pystsup
    Module: evolutionary/selection
    File: selection.py
    
    Purpose:  Contains the selection opearators.
             
    Author : Rithin Chalumuri
    Version: 1.0 
    Date   : 21/7/17
    
"""

import random

def tournamentSelection(population,popSize):
    """
    Function to select some 'good' parents from the population using tournament selection.
    This implementation selection n pairs of parents, where n = population size // 2

    Parameters:

        population (list) - list of solutions.
        popSize (int) - population size.

    Returns:
        selectedPop (list) - list of tuples that contain pairs of 'good' parents.
    """

    selectedPop = []

    #Until fill the selectedPop upto the size we want
    while len(selectedPop) < (popSize//2):

        #Select 4 parents
        player1 = random.choice(population)
        player2 = random.choice(population)
        player3 = random.choice(population)
        player4 = random.choice(population)

        #Pick the winner of player 1 and 2 to be parent1.
        if player1 < player2:
            parent1 = player1
        else:
            parent1 = player2

        #Pick the winner of player 3 and 4 to be parent2.
        if player3 < player4:
            parent2 = player3
        else:
            parent2 = player4


        #Add the tuple (parent1,parent2) to the selected population list.
            
        selectedPop.append([parent1,parent2])


    return selectedPop




def rouletteWheel(population,popSize):
    """
    Implementation of roulette wheel selection.
    This implementation selection n pairs of parents, where n = population size // 2
    Of those n pairs, half are focused on Fst and half on Fsup.
    
    Parameters:

        population (list) - list of solutions.
        popSize (int) - population size.

    Returns:
        selectedPop (list) - list of tuples that contain pairs of 'good' parents.
    
    """

    selectedPop = []

    totalFst = sum([sol.getFst() for sol in population])
    totalFsup = sum([sol.getFst() for sol in population])

    while len(selectedPop) < (popSize//4):

        pick1 = random.uniform(0,totalFst)
        pick2 = random.uniform(0,totalFst)

        curr1 = 0
        curr2 = 0
        
        for sol in population:
            curr1+= sol.getFst()
            if curr1 > pick1:
                parent1 = sol
                break

        for sol in population:
            curr2+=sol.getFst()
            if curr2 > pick2:
                parent2 = sol
                break

        selectedPop.append([parent1,parent2])


    while len(selectedPop) < (popSize//2):

        pick1 = random.uniform(0,totalFsup)
        pick2 = random.uniform(0,totalFsup)

        curr1 = 0
        curr2 = 0
        
        for sol in population:
            curr1+= sol.getFsup()
            if curr1 > pick1:
                parent1 = sol
                break

        for sol in population:
            curr2+=sol.getFsup()
            if curr2 > pick2:
                parent2 = sol
                break

        selectedPop.append([parent1,parent2])


    return selectedPop

            
    



    
    
