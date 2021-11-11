# Meshaal_Mouawad

Abstract—In this project, we investigate of autonomous robots for mapping, navigation, with the shortest path planning to the
target. We implemented Voronoi Diagram for path planning as the global path to avoid the obstacles, we generated local targets (multiway points) and applied Travel Salesman Problem (TSP) Algorithms to find the optimal path (shortest path planning) to connect the waypoints by searching the closest edge of the Voronoi diagram, we then applied the Dynamic Window Approach method (DWA) to allow the robot to navigate locally based on the TSP and Voronoi diagram paths.  The robot was given an assignment to navigate from the start point (source) to the end point with local points targets (targets). Then the robot has to complete the assignment as the followings; from the start point find the shortest path, go to the local points (the targets), with avoiding the obstacles, complete the assignments to the end point.

# How to use the Code(s) 
a. Voronoi Diagram
1/ Open the folder for Voronoi Diagram.
2/ open the main file > go to the map and change ---- to youe map name.
3/ You may need to adjust the resolution and the robot radius.
4/ run the MATLAB code and it will generate five figuers.

5/ 

* b. Traveling Sales Man 
1/ Open the folder for TSP 

2/ run the code 

3/ open the folder for the TSP 

4/ in the code add the distant matrix you just got in b.2.

5/ run the python > at the bottom you will see "optimal path" this is the TSP shortest path you need it for the DWA.

* c. DWA algorithms
1/ open the folder for the DWA > open main.m file.

2/ change it to your map.

3/ add the start point
