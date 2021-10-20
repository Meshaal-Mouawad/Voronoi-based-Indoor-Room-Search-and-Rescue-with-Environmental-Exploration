# import libraries

import pulp
import pandas as pd  # to read csv file and distance matrix "dis_mat".
from scipy.spatial import distance_matrix
from matplotlib import pyplot as plt
import time
import copy

# # 1 Input the data and  problem visualization
'The csv file *"tsp_city_data.csv"* contains the names of cities in India with thier latitute and longitute ' \
'information. The first city *"Delhi"* is assumed to be starting point of trip (depot). The data input to ' \
'TSP model is the distance matrix which stores the distance (or travel time or cost) from each city (location) ' \
'to every other city. Thus, for a traveling salesman problem for N cities (location), ' \
'the distance matrix is of size N x N. The varible * no_of_locs* in the code is used to define the first n no. ' \
'of cities we want to include in our TSP problem data. The value is set 20 for now. The pyhton pandas library ' \
'is used to read csv file and distance matrix "dis_mat".'
#This function takes locations as input and plot a scatter plot
def plot_fig(loc,heading="plot"):
    plt.figure(figsize=(6,6))
    for i,row in loc.iterrows():
        if i==0:
            plt.scatter(row["x"],row["y"],c='r')
            plt.text(row["x"]+0.2, row["y"]+0.2, 'p_n1')
        else:
            plt.scatter(row["x"], row["y"], c='black')
            plt.text(row["x"] + 0.2, row["y"] + 0.2,full_data.loc[i]['local_locations'] )
        plt.ylim(0,500)
        plt.xlim(0,500)
        plt.title(heading)
# this function find all the subtour in the LP solution.
def get_plan(r0):
    r=copy.copy(r0)
    route = []
    while len(r) != 0:
        plan = [r[0]]
        del (r[0])
        l = 0
        while len(plan) > l:
            l = len(plan)
            for i, j in enumerate(r):
                if plan[-1][1] == j[0]:
                    plan.append(j)
                    del (r[i])
        route.append(plan)
    return(route)

# set no of cities
'''
The varible * no_of_locs* in the code is used to define the first n no of cities we want to include 
in our TSP problem data. '''
no_of_locs = 6

# The pyhton pandas library is used to read csv file and distance matrix "dis_mat".
# data = pd.read_csv("C:/Users/Meshaal Mouawad/Downloads/TSP-ILP-main/nodeList.csv")
data = pd.read_csv("E:/D Recover/MSUfiles/Luo/My research/Journal Voronoi Diagram July 18 2021/code/draft/TSP Python code July 22 2021/TSP-ILP-main/Local_points_pn5.csv")
full_data = data.iloc[0:no_of_locs, :]
d = full_data[['x', 'y']]
# a traveling salesman problem for N cities (location), the distance matrix is of size N x N
dis_mat = pd.DataFrame(distance_matrix(d.values, d.values), \
                       index=d.index, columns=d.index)
print("----------data--------------")
print(full_data)
print("-----------------------------")
plot_fig(d, heading="Problem Visualization")

plt.show()

# This formulation was proposed by Miller, Tucker, Zemlin. To eliminate subtours, decision variables representing
# times at which a location is visited is added. Variable for all locations except depot node are added.  ' \
# 𝑡𝑖  = time at which location i is visited , i =[2,...N] Finally what is required the constraint  𝑡𝑗  >  𝑡𝑖 ' \
# if 𝑥𝑖,𝑗=1  which can be formulated as LP constraints as follows '
# 3. MTZ Method for subtour elimination
start_t=time.time()
model=pulp.LpProblem('tsp',pulp.LpMinimize)
#define variable
x=pulp.LpVariable.dicts("x",((i,j) for i in range(no_of_locs) \
                                for j in range(no_of_locs)),\
                           cat='Binary')

t = pulp.LpVariable.dicts("t", (i for i in range(no_of_locs)), \
                             lowBound=1,upBound= no_of_locs, cat='Integer')
#set objective
model+=pulp.lpSum(dis_mat[i][j]* x[i,j] for i in range(no_of_locs) \
                      for j in range(no_of_locs))
# st constraints
for i in range(no_of_locs):
    model+=x[i,i]==0
    model+=pulp.lpSum(x[i,j] for j in range(no_of_locs))==1
    model += pulp.lpSum(x[j, i] for j in range(no_of_locs)) == 1
#eliminate subtour
for i in range(no_of_locs):
    for j in range(no_of_locs):
        if i!=j and (i!=0 and j!=0):
            model+=t[j]>=t[i]+1 - (2*no_of_locs)*(1-x[i,j])
status=model.solve()
#status=model.solver()
print("-----------------")
print(status,pulp.LpStatus[status],pulp.value(model.objective))
route=[(i,j) for i in range(no_of_locs) \
           for j in range(no_of_locs) if pulp.value(x[i,j])==1]
print(route)
plot_fig(d,heading="solution Visualization")
arrowprops = dict(arrowstyle='->', connectionstyle='arc3', edgecolor='blue')
for i, j in route:
    plt.annotate('', xy=[d.iloc[j]['x'], d.iloc[j]['y']],\
                      xytext=[d.iloc[i]['x'], d.iloc[i]['y']],\
                     arrowprops=arrowprops)
print("time taken by MTZ formulation = ", time.time()-start_t)
plt.show()