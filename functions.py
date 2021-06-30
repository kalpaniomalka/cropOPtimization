# import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from random import randint
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# fitness function to calculate profit
def fitness_function(yldPrd, prcPrd, perches):
    return (yldPrd*prcPrd) * perches

def find_best(cropName,prd,perches):
    BestFitness = []
    fitness_value = fitness_function(prd[0],prd[1],perches)
  
    BestFitness.append((cropName,round(fitness_value,2),(prd,round(prd[0]*prd[1],2))))
    return BestFitness

# function to generate random acres for each crop
def generate_solutions(monthStr,perches):
    solutions = []
    for s in range(1000):
        print(s)
        if(monthStr<4 or monthStr==5 or (monthStr>=8 and monthStr<=10)):
            x = np.random.randint(1, perches, size=(5,))
            while sum(x) != perches: 
                x = np.random.randint(1, perches, size=(5,))
            solutions.append( (x[0], x[1], x[2], x[3], x[4]) )
        else:
            x = np.random.randint(1, perches, size=(6,))
            while sum(x) != perches: 
                x = np.random.randint(1, perches, size=(6,))
            solutions.append( (x[0], x[1], x[2], x[3], x[4], x[5]) )
    return solutions

# function to get suitable acres and sort solution based on fitness value 
def solutions_ranking(solutions,monthStr,BestFitness):
    rankedSolutions = []
    for s in solutions:
        if(monthStr<4 or monthStr==5 or (monthStr>=8 and monthStr<=10)):
            rankedSolutions.append( (calculate_area_fitness(s[0],0,s[1],s[2],s[3],s[4],monthStr,BestFitness) , s))
        else:
            rankedSolutions.append( (calculate_area_fitness(s[0],s[1],s[2],s[3],s[4],s[5],monthStr,BestFitness) , s))
    rankedSolutions.sort()
    rankedSolutions.reverse()
    return rankedSolutions

# function to calculate suitable acres for each crop
def calculate_area_fitness(tomatoArea, potatoArea, beansArea, carrotArea, pumpkinArea, capsicumArea,monthStr,BestFitness):
    if(monthStr==4 or (monthStr>5 and monthStr<8) or monthStr>10):
        return round(BestFitness[0][2][1]*tomatoArea + BestFitness[1][2][1]*beansArea + \
            BestFitness[2][2][1]*carrotArea +  BestFitness[3][2][1]*pumpkinArea +  BestFitness[4][2][1]*capsicumArea\
            + BestFitness[5][2][1]*potatoArea,4)
    else:
        return round(BestFitness[0][2][1]*tomatoArea + BestFitness[1][2][1]*beansArea + \
            BestFitness[2][2][1]*carrotArea + BestFitness[3][2][1]*pumpkinArea +  BestFitness[4][2][1]*capsicumArea,4)

# function to combine different parents value to generate new child
def crossover(best_100,monthStr,perches):
    elements = []
    newGen = []
    for s in best_100:
        elements.append(s[1][0])
        elements.append(s[1][1])
        elements.append(s[1][2])
        elements.append(s[1][3])
        elements.append(s[1][4])
        if(monthStr==4 or (monthStr>5 and monthStr<8) or monthStr>10):
            elements.append(s[1][5])

    for _ in range(10000):
        e1 = np.random.choice(elements)
        e2 = np.random.choice(elements)
        e3 = np.random.choice(elements)
        e4 = np.random.choice(elements)
        e5 = np.random.choice(elements)
        if(monthStr==4 or (monthStr>5 and monthStr<8) or monthStr>10):
            e6 = np.random.choice(elements)
            # generating new generation
            if(e1+e2+e3+e4+e5+e6 == perches):
                newGen.append((e1,e2,e3,e4,e5,e6))
        else:
            # generating new generation
            if(e1+e2+e3+e4+e5 == perches):
                newGen.append((e1,e2,e3,e4,e5))
    return newGen

def mutateIndividual(individual):
    # select chromosomes
    mutationIndex1 = randint(0, len(individual)-1)
    mutationIndex2 = randint(0, len(individual)-1)
    value1 = individual[mutationIndex1]
    
    # apply swap mutation for selected indexes
    individual[mutationIndex1] = individual[mutationIndex2]
    individual[mutationIndex2] = value1
    return individual

def mutation(population):
    finalBestSolutions = []
    for i in range(0, len(population)): # outer loop on each individual
        pop_list = list(population[i])
        population[i] = mutateIndividual(pop_list)
        finalBestSolutions.append(population[i])
    return finalBestSolutions

def calculateTime(monthStr,dayS):
    time = []
    start_time = datetime( 2021, monthStr, dayS)
    today = datetime(2021, int(datetime.today().strftime('%m')), int(datetime.today().strftime('%d')))
    diff = today - start_time
    val = str(diff)
    
    time.append(90 - int(val.split(" ")[0]))
    time.append(120 - int(val.split(" ")[0]))
    time.append(120 - int(val.split(" ")[0]))
    time.append(120 - int(val.split(" ")[0]))
    time.append(120 - int(val.split(" ")[0]))
    if(monthStr==4 or (monthStr>5 and monthStr<8) or monthStr>10):
        time.append(90 - int(val.split(" ")[0]))
    return time