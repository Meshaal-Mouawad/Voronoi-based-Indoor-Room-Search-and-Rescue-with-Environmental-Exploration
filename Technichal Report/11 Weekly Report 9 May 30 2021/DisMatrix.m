clear all
close all

%  **INPUT
% Adjecent Matrix: the Adjecent Matrix genereated from the Voronoi Diagram
% 
% **OUTPUT
% D: the Distant Matrix 
%
%  load the Adjecent Matrix
load B_sparse 
M=B
S = 1000000000*(ones(5)-eye(5));
%  calculate the Distant Matrix D
% D = pdist2(a,b);
D = pdist(B);
G= graph(B)
plot(G)
% to plot it with weights showings on the graph
 plot(G,'EdgeLabel',G.Edges.Weight)

F = squareform(B);
 % GraphSqrt = graph(F)
% convert to sparse
% If you want to replace all of the zeros in an array with infinity, do:
% Z=B(~B) == 1000000;  % Or A(A==0) = inf;

whos A D Z F W
