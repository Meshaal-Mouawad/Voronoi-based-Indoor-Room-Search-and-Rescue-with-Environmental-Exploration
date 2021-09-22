function stopDist=CalcBreakingDist(vel,model)
%Function to calculate braking distance from current speed according to dynamic model
global dt;
stopDist=0;
while vel>0
    stopDist=stopDist+vel*dt;%Calculation of braking distance
    vel=vel-model(3)*dt;
end


