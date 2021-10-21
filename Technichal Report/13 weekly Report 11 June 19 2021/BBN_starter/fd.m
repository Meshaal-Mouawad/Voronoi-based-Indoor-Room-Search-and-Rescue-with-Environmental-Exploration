% fd: This function computes d(x_j) using the equation: d(xj) 
%
% d(x_j) =  x_j :                if x_j > 0 
%           beta(x_j- sigma):    if x_j < sigma
%           0:                   otherwise
%% 
function d = fd(xj,sigma,beta) % x_j

if xj>0 
    d = xj;
else if xj < sigma
        d = beta * ( xj - sigma);
    else
        d = 0;
    end 
end 

end

