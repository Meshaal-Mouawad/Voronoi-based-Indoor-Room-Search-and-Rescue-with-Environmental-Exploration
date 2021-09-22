function dist=CalcDistEval(x,ob,R)
%Function to calculate distance evaluation value with obstacle

dist=100;
for io=1:length(ob(:,1))
    disttmp=norm(ob(io,:)-x(1:2)')-R;%Calculate norm error between path position and obstacle
    if dist>disttmp	%Find the minimum
        dist=disttmp;
    end
end

%Satisfy the evaluation value when the distance is more than twice
if dist>=2*R
    dist=2*R;
end


