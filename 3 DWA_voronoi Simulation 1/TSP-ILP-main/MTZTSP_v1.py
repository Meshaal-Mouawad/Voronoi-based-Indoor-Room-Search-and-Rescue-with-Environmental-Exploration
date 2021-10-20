# _*_coding:utf-8 _*_
from __future__ import print_function
from __future__ import division, print_function
from gurobipy import *
import re;
import math;
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
from matplotlib.lines import lineStyles
import time

starttime = time.time()
'''
# function to read data from .txt files   
def readData(path, nodeNum):
    nodeNum = nodeNum;
    cor_X = []
    cor_Y = []
    
    f = open(path, 'r');
    lines = f.readlines();
    count = 0;
    # read the info
    for line in lines:
        count = count + 1;
        if(count >= 10 and count <= 10 + nodeNum):
            line = line[:-1]
            str = re.split(r" +", line)
            cor_X.append(float(str[2]))
            cor_Y.append(float(str[3]))
                
    # compute the distance matrix
    disMatrix = [([0] * nodeNum) for p in range(nodeNum)]; 
    # data.disMatrix = [[0] * nodeNum] * nodeNum]; 
    for i in range(0, nodeNum):
        for j in range(0, nodeNum):
            temp = (cor_X[i] - cor_X[j])**2 + (cor_Y[i] - cor_Y[j])**2;
            disMatrix[i][j] = (int)(math.sqrt(temp));
#             disMatrix[i][j] = 0.1 * (int)(10 * math.sqrt(temp));
#             if(i == j):
#                 data.disMatrix[i][j] = 0;
#             print("%6.0f" % (math.sqrt(temp)), end = " ");
            temp = 0;
    
    return disMatrix;
'''
def printData(disMatrix):
    print("-------cost matrix-------\n");
    for i in range(len(disMatrix)):
        for j in range(len(disMatrix)):
            #print("%d   %d" % (i, j));
            print("%6.1f" % (disMatrix[i][j]), end = " ");
#             print(disMatrix[i][j], end = " ");
        print();
        
def reportMIP(model, Routes):
    if model.status == GRB.OPTIMAL:
        print("Best MIP Solution: ", model.objVal, "\n")
        var = model.getVars()
        for i in range(model.numVars):
            if(var[i].x > 0):
                print(var[i].varName, " = ", var[i].x)
                print("Optimal route:", Routes[i])
                     
def getValue(var_dict, nodeNum): 
    x_value = np.zeros([nodeNum + 1, nodeNum + 1]) 
    for key in var_dict.keys():   
        a = key[0]
        b = key[1]
        x_value[a][b] = var_dict[key].x  
            
    return x_value    

def getRoute(x_value):


    x = copy.deepcopy(x_value)
#     route_temp.append(0)
    previousPoint = 0
    route_temp = [previousPoint] 
    count = 0 
    while(len(route_temp) < len(x)): 
        #print('previousPoint: ', previousPoint )
        if(x[previousPoint][count] > 0): 
            previousPoint = count  
            route_temp.append(previousPoint) 
            count = 0 
            continue
        else:
            count += 1
    return route_temp

# toy example
#cost = [[0, 15, 2, 1, 5],
#        [15, 0, 10, 6, 8],
 #       [2, 10, 0, 4, 2],
  #      [1, 6, 4, 0, 9],
   #     [5, 8, 2, 9, 0]]
# cost = [[0.0000, 103.23759, 122.91867],[103.23759, 0.00000, 22.56103], [122.91867, 22.56103, 0.0000]]
cost =[[0.000000,  304.795013,  465.295605,  270.739727,  429.418211,  152.970585],
[304.795013,    0.000000,  181.107703,  221.359436,  182.482876,  243.515913],
[465.295605,  181.107703,    0.000000,  393.192065,  264.007576,  360.693776],
[270.739727,  221.359436,  393.192065,    0.000000,  210.950231,  326.955654],
[429.418211,  182.482876,  264.007576,  210.950231,    0.000000,  413.037529],
[152.970585,  243.515913,  360.693776,  326.955654,  413.037529,    0.000000]]

# nodeNum = 5 
nodeNum =6

'''
path='C:/Users/regis/Downloads/In/c201.txt';
cost = readData(path, nodeNum)
'''

printData(cost)

model = Model('TSP')

# creat decision variables 
X = {} 
mu = {}  
for i in range(nodeNum + 1):  
    mu[i] = model.addVar(lb = 0.0
                         , ub = 100 #GRB.INFINITY
                          # , obj = distance_initial
                         , vtype = GRB.CONTINUOUS
                         , name = "mu_" + str(i)  
                        )

    for j in range(nodeNum + 1): 
        if(i != j):
            X[i, j] = model.addVar(vtype = GRB.BINARY
                                  , name = 'x_' + str(i) + '_' + str(j) 
                                  )

# set objective function
obj = LinExpr(0)
for key in X.keys():
    i = key[0]
    j = key[1]
    if(i < nodeNum and j < nodeNum):
        obj.addTerms(cost[key[0]][key[1]], X[key])
    elif(i == nodeNum):
        obj.addTerms(cost[0][key[1]], X[key])
    elif(j == nodeNum):
        obj.addTerms(cost[key[0]][0], X[key])
        
model.setObjective(obj, GRB.MINIMIZE)

# add constraints 1 
for j in range(1, nodeNum + 1): 
    lhs = LinExpr(0)
    for i in range(0, nodeNum): 
        if(i != j):
            lhs.addTerms(1, X[i, j])
    model.addConstr(lhs == 1, name = 'visit_' + str(j))

# add constraints 2
for i in range(0, nodeNum):
    lhs = LinExpr(0)
    for j in range(1, nodeNum + 1): 
        if(i != j):
            lhs.addTerms(1, X[i, j])
    model.addConstr(lhs == 1, name = 'visit_' + str(j))

# add MTZ constraints
# for key in X.keys():
#     org = key[0]
#     des = key[1]
#     if(org != 0 or des != 0):
# #         pass 
#         model.addConstr(mu[org] - mu[des] + 100 * X[key] <= 100 - 1) 
for i in range(0, nodeNum):
    for j in range(1, nodeNum + 1):
        if(i != j):
            model.addConstr(mu[i] - mu[j] + 100 * X[i, j] <= 100 - 1) 

model.write('model.lp')  
model.optimize()

x_value = getValue(X, nodeNum) 
route = getRoute(x_value)
print('optimal route:', route) 