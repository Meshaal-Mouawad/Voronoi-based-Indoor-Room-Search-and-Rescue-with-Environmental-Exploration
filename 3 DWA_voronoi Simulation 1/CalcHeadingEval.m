
function heading=CalcHeadingEval(x,goal)
%Function to calculate heading evaluation function

theta=toDegree(x(3));%Robot orientation
goalTheta=toDegree(atan2(goal(2)-x(2),goal(1)-x(1)));%Goal direction

if goalTheta>theta
    targetTheta=goalTheta-theta;
else
    targetTheta=theta-goalTheta;
end

heading=180-targetTheta;