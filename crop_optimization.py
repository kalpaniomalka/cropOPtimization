# import libraries
import numpy as np
import csv
from numpy.lib.function_base import append
import pandas as pd
import matplotlib.pyplot as plt
from random import randint
import pickle
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
import functions as fn
import os

current_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
csv_path = current_path+"\\crop.csv"

# variables defining
tomatoPrd = [0,0]
potatoPrd = [0,0]
beansPrd = [0,0]
carrotsPrd = [0,0]
pumpkinPrd = [0,0]
capsicumPrd = [0,0]

BestFitness = []
elements = []
newGen = []
solutions = []
rankedSolutions = []
bestSolutions = []
finalBestSolutions = []
time = []

#This function makes sure the days are within the range of 1-31 and months from 1 to 12
def monthChecking(monthStart,monthEnd,dayStart,dayEnd):
    while (monthStart <= 0 or monthStart > 12):
        monthStart = int(input('Please enter the  valid starting month of crop (valid values 1-12):'))
    while (dayEnd <= 0 or dayEnd > 31):
        dayE = int(input('Please enter the  valid finishing day of crop (valid values 1-30):'))     
    while (monthEnd <= 0 or monthEnd > 12):        
        monthEnd = int(input('Please enter the  valid finishing month of crop (valid values 1-12): '))
    while (dayStart <= 0 or dayStart > 31):
        dayS = int(input('Please enter the  valid starting day of crop (valid values 1-30):'))

# Function to read data from csv
def read(monthStr):
    with open('crop.csv', 'r') as file:
        data=list(csv.reader(file))
        
        tomatoPrd[0] = round(int(data[1][2])/160,2)
        tomatoPrd[1] = round(int(data[1][3])/160,2)
        beansPrd[0] =  round(int(data[2][2])/160,2)
        beansPrd[1] = round(int(data[2][3])/160,2)
        carrotsPrd[0] = round(int(data[3][2])/160,2)
        carrotsPrd[1] = round(int(data[3][3])/160,2)
        pumpkinPrd[0] = round(int(data[4][2])/160,2)
        pumpkinPrd[1] = round(int(data[4][3])/160,2)
        capsicumPrd[0] = round(int(data[5][2])/160,2)
        capsicumPrd[1] = round(int(data[5][3])/160,2)
  
        if(monthStr==4 or (monthStr>5 and monthStr<8) or monthStr>10):
            potatoPrd[0] = round(int(data[6][2])/160,2)
            potatoPrd[1] = round(int(data[6][3])/160,2)

def cropOptimization(data):
    acres = int(data["acres"])
    dayS = int(data["dayS"])
    monthStr = int(data["monthStr"])
    dayE = int(data["dayE"])
    monthE = int(data["monthE"])

    # Convert acres to perch
    perches = acres*160

    print("Optimizing....")
    # call the function
    monthChecking(monthStr,monthE,dayS,dayE)
    read(monthStr)

    # find best fitness
    result = fn.find_best("Tomato",tomatoPrd,perches)
    BestFitness.append(result[0])
    result = fn.find_best("Beans",beansPrd,perches)
    BestFitness.append(result[0])
    result = fn.find_best("Carrot",carrotsPrd,perches)
    BestFitness.append(result[0])
    result = fn.find_best("Pumpkin",pumpkinPrd,perches)
    BestFitness.append(result[0])
    result = fn.find_best("Capsicum",capsicumPrd,perches)
    BestFitness.append(result[0])
    if(monthStr==4 or (monthStr>5 and monthStr<8) or monthStr>10):
        result = fn.find_best("Potato",potatoPrd,perches)
        BestFitness.append(result[0])

    # getting overall best fitness value 
    overallBestFitnessValue = 0
    for value in BestFitness:
        if value[1] > overallBestFitnessValue:
            overallBestFitnessValue = value[1]

    print("Started to generate solutions")
    solutions = fn.generate_solutions(monthStr,perches)
    print(len(solutions))
    print("Started to rank generated solutions")
    rankedSolutions = fn.solutions_ranking(solutions,monthStr,BestFitness)
    print(len(rankedSolutions))
   
    # get best 100 solutions
    best_100_Solutions = rankedSolutions[:100]
    print(len(best_100_Solutions))
    print("Creating a new generation using best 100 solutions")
    newGen = fn.crossover(best_100_Solutions,monthStr,perches)

    print("Mutation start")
    finalBestSolutions = fn.mutation(newGen)

    finalBestSolutions_with_fitness = []
    for fbs in finalBestSolutions:
        fbs_in_acres = []
        fbs_in_acres.append(fbs[0]/160)
        fbs_in_acres.append(fbs[1]/160)
        fbs_in_acres.append(fbs[2]/160)
        fbs_in_acres.append(fbs[3]/160)
        fbs_in_acres.append(fbs[4]/160)
        if(monthStr<4 or monthStr==5 or (monthStr>=8 and monthStr<=10)):
            finalBestSolutions_with_fitness.append((fn.calculate_area_fitness(fbs[0],fbs[1],fbs[2],fbs[3],fbs[4],0,monthStr,BestFitness) , fbs_in_acres))
        else:
            fbs_in_acres.append(fbs[5]/160)
            finalBestSolutions_with_fitness.append((fn.calculate_area_fitness(fbs[0],fbs[1],fbs[2],fbs[3],fbs[4],fbs[5],monthStr,BestFitness) , fbs_in_acres))
        
    finalBestSolutions_with_fitness.sort()
    finalBestSolutions_with_fitness.reverse()
    print(finalBestSolutions_with_fitness)

    print("\n-----------------------------------------------------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------------------------------------")
    print("Total Acres: "+str(acres))
    print("BestFitnessValue, Tomatoes(Acres), Benas(Acres), Carrots(Acres), Pumpkin(Acress), Capsicum(Acres), Potatoes(Acres)")
    print(finalBestSolutions_with_fitness[0])
    print("-----------------------------------------------------------------------------------------------------------------")

    time = fn.calculateTime(monthStr,dayS) 
 
    Yield = []
    j = 0
    for i in finalBestSolutions_with_fitness[0][1]:
        Yield.append(round((i * BestFitness[j][2][0][0])*160,2))
        j += 1

    # get price and yield for acres
    price = []
    yields = []

    for value in BestFitness:
        yields.append(value[2][0][0]*160)
        price.append(value[2][0][1]*160)
    
    # profit of each crop

    #Tomatoes
    monthly_profit_tomato = round((yields[0]*finalBestSolutions_with_fitness[0][1][0]) * price[0],2)

    #Beans
    monthly_profit_beans = round((yields[0]*finalBestSolutions_with_fitness[1][1][0]) * price[1],2)

    #Carrots
    total_profit_carrots = round((yields[0]*finalBestSolutions_with_fitness[2][1][0]) * price[2],2)

    # Pumpkin
    monthly_profit_pumpkin = round((yields[0]*finalBestSolutions_with_fitness[3][1][0]) * price[3],2)

    #Capsicum
    monthly_profit_capsicum = round((yields[0]*finalBestSolutions_with_fitness[4][1][0]) * price[4],2)

    #Potatoes
    if(monthStr==4 or (monthStr>5 and monthStr<8) or monthStr>10):
        total_profit_potatoes = round((yields[0]*finalBestSolutions_with_fitness[5][1][0]) * price[5],2)
        
    final_acres = []
    for value in finalBestSolutions_with_fitness[0][1]:
        final_acres.append(round(value,2))

    # with open('Outputs\\results.csv', 'w') as f:
    #     thewriter = csv.writer(f)
    
    #     if(monthStr<4 or monthStr==5 or (monthStr>=8 and monthStr<=10)):
    #         thewriter.writerow(['Acres(Tomatoes)','Yield(Tomatoes)','Time(Tomatoes)','Profit(Tomatoes)',\
    #         'Acres(Beans)','Yield(Beans)','Time(Beans)','Profit(Beans)','Acres(Carrots)','Yield(Carrots)','Time(Carrots)','Profit(Carrots)',\
    #         'Acres(Pumpkin)','Yield(Pumpkin)','Time(Pumpkin)','Profit(Pumpkin)','Acres(Capsicum)','Yield(Capsicum)','Time(Capsicum)','Profit(Capsicum)'])
    #         thewriter.writerow([final_acres[0],Yield[0],time[0],monthly_profit_tomato,final_acres[1],Yield[1],time[1],\
    #             monthly_profit_beans,final_acres[2],Yield[2],time[2],total_profit_carrots,final_acres[3],Yield[3],time[3],\
    #             monthly_profit_pumpkin,final_acres[4],Yield[4],time[4],monthly_profit_capsicum])
    #     else:
    #         thewriter.writerow(['Acres(Tomatoes)','Yield(Tomatoes)','Time(Tomatoes)','Profit(Tomatoes)',\
    #         'Acres(Beans)','Yield(Beans)','Time(Beans)','Profit(Beans)','Acres(Carrots)','Yield(Carrots)','Time(Carrots)','Profit(Carrots)',\
    #         'Acres(Pumpkin)','Yield(Pumpkin)','Time(Pumpkin)','Profit(Pumpkin)','Acres(Capsicum)','Yield(Capsicum)','Time(Capsicum)','Profit(Capsicum)',\
    #         'Acres(Potatoes)','Yield(Potatoes)','Time(Potatoes)','Profit(Potatoes'])
    #         thewriter.writerow([final_acres[0],Yield[0],time[0],monthly_profit_tomato,final_acres[1],Yield[1],time[1],\
    #             monthly_profit_beans,final_acres[2],Yield[2],time[2],total_profit_carrots,final_acres[3],Yield[3],time[3],\
    #             monthly_profit_pumpkin,final_acres[4],Yield[4],time[4],monthly_profit_capsicum,final_acres[5],\
    #             Yield[5],time[5],total_profit_potatoes])
    
    if(monthStr==4 or (monthStr>5 and monthStr<8) or monthStr>10):
        best_matching_data = {
            "Tomatoes(Acres)": final_acres[0],
            "Tomatoes (Yield)": Yield[0],
            "Tomato Time(Days)" : time[0],
            "Tomato Profit(LKR)": monthly_profit_tomato,
            "Beans(Acres)": final_acres[1],
            "Beans (Yield)": Yield[1],
            "Beans Time(Days)" : time[1],
            "Beans Profit(LKR" : monthly_profit_beans,
            "Carrots(Acres)": final_acres[2],
            "Carrots (Yield)": Yield[2],
            "Carrots Time(Days)" : time[2],
            "Carrots Profit(LKR)" : total_profit_carrots,
            "Pumpkin(Acres)": final_acres[3],
            "Pumpkin (Yield)": Yield[3],
            "Pumpkin Time(Days)": time[3],
            "Pumpkin Profit(LKR)" : monthly_profit_pumpkin,
            "Capsicum(Acres)": final_acres[4],
            "Capsicum (Yield)": Yield[4],
            "Capsicum Time(Days)": time[4],
            "Capsicum Profit(LKR)": monthly_profit_capsicum,
            "Potatoes(Acres)": final_acres[5],
            "Potatoes (Yield)": Yield[5],
            "Potatoes Time(Days)" : time[5],
            "Potatoes Profit(LKR)": total_profit_potatoes
        }
    else:
        best_matching_data = {
            "Tomatoes(Acres)": final_acres[0],
            "Tomatoes (Yield)": Yield[0],
            "Tomato Time(Days)" : time[0],
            "Tomato Profit(LKR)": monthly_profit_tomato,
            "Beans(Acres)": final_acres[1],
            "Beans (Yield)": Yield[1],
            "Beans Time(Days)" : time[1],
            "Beans Profit(LKR" : monthly_profit_beans,
            "Carrots(Acres)": final_acres[2],
            "Carrots (Yield)": Yield[2],
            "Carrots Time(Days)" : time[2],
            "Carrots Profit(LKR)" : total_profit_carrots,
            "Pumpkin(Acres)": final_acres[3],
            "Pumpkin (Yield)": Yield[3],
            "Pumpkin Time(Days)": time[3],
            "Pumpkin Profit(LKR)" : monthly_profit_pumpkin,
            "Capsicum(Acres)": final_acres[4],
            "Capsicum (Yield)": Yield[4],
            "Capsicum Time(Days)": time[4],
            "Capsicum Profit(LKR)": monthly_profit_capsicum
    }

    # filename = 'Outputs\\final_results.pickle'
    # pickle.dump(best_matching_data, open(filename, 'wb'))

    return best_matching_data

#cropOptimization()