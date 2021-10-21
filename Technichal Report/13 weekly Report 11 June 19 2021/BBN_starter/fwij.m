% fwij: This function computes w_ij, the weights of each cell
function wij  = fwij(rr,r,u)
if rr > 0 && rr < r
    wij = u/rr 
else
    wij = 0;
end 


end

