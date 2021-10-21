% defferentiate: this function is part of the ode45 solver that computes the neural
% activity (sm(b,c)) of each cel using the following equation:
% dy= (-A*y) + stimu(b,c) + exinput.
%
% stimu(b,c) is I_i in original equation.
%---------------- the original equation -------------------------
% (dx_i)/dt = -Ax_i + I_i + sum( w_ij  d(x_j) ) from (j=1) to K
% Where d(x_j) =  x_j :                if x_j > 0 
%                 beta(x_j- sigma):    if x_j < sigma
%                 o:                   otherwise
% 
%% 
function dy = differentiate(x,y)

A = 5;
% global stimu
% global c 
%global b
% global exinput
dy = (-A * y)+ stimu(b,c)+exinput

end

