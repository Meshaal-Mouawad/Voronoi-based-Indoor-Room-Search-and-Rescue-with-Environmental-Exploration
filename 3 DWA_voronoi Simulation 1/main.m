clc
close all;
clear all;

%% TSP + VD + DWA 2021/08/08 Tingjun
InputFileImage='Map4_3.png'; % input image, .jpg or .png
ROBOTRADIUS= 1; % Rotot Radius
INPUTIMAGE=imread(InputFileImage);

% figure, imshow(INPUTIMAGE); title('Input Map');  
INPUTIMAGE = flipud(INPUTIMAGE);
img=im2bw(INPUTIMAGE);
[y x]=find(img==0);
% x=(x/size(INPUTIMAGE,1))*10;  % scale the map
% y=(y/size(INPUTIMAGE,2))*10;
obstacle=[x y];

plot(x,y,'.')

%% Show Targets and start point
hold on
% figure(5)
startpoint = [420,518-450];
targets = [220, 518-220;
    200,518-40;
    150,518-430;
    40,518-250;
    450,518-300
    ];
for i=1:size(targets,1)
    plot(targets(i,1),targets(i,2),'ro','MarkerEdgeColor','r','MarkerFaceColor','y','markersize',8);
    hold on;
    text(targets(i,1)+3,targets(i,2)+6,num2str(i),'Color',[1 0 0]);
end
plot(startpoint(1,1),startpoint(1,2),'rs','MarkerEdgeColor','b','MarkerFaceColor','b','markersize',15)
text(startpoint(1,1)+3,startpoint(1,2)-8,"startpoint",'Color',[1 0 0]);
hold off


%% DWA

% x=[420 518-450 pi/2 0 0]';% Robot initial state [x(m), y(m), yaw(Rad), v(m/s), ω(rad/s)]
x=[420 518-450 pi/2 100 0]';% Robot initial state [x(m), y(m), yaw(Rad), v(m/s), ω(rad/s)]
% Goal should be VD nodes+targets
N=12;
goal=zeros(2,N);
goal(:,1)=[413	99];% VD 
goal(:,2)=[413	134];
goal(:,3)=[450 518-300];
goal(:,4)=[290	228];
goal(:,5)=[220 518-220];
goal(:,6)=[191	228];
goal(:,7)=[113	367];
goal(:,8)=[200 518-40];
goal(:,9)=[91	372];
goal(:,10)=[40 518-250];
goal(:,11)=[75	68];
goal(:,12)=[150 518-430];

% Goal position [x(m),y(m)]

obstacleR=1;	% Obstacle radius for collision detection
global dt; 
dt=1;% Increment time [s]

% Robot Dynamics Model
% [Maximum speed [m / s], Maximum turning speed [rad / s], Maximum acceleration / deceleration [m / ss], Maximum acceleration / deceleration speed [rad / ss],
% Speed resolution [m / s], Turn speed resolution [rad / s]]
Kinematic=[30.0,toRadian(10.0),1,toRadian(30.0),0.5,toRadian(1)];

% Evaluation function parameters [heading, dist, velocity, predictDT]
evalParam=[2,4,2,8.0];
area=[0 517 0 461];% Simulation area [xmin xmax ymin ymax]

%simulation result
result.x=[];
tic;
%movcount=0;
% Main loop
for k=1:1:N
for i=1:5000
    %Calculation of input value by DWA
    [u,traj]=DynamicWindowApproach(x,Kinematic,goal(:,k),evalParam,obstacle,obstacleR);
    x=f(x,u);% Movement model

    %Saving simulation results
    result.x=[result.x; x'];

    %Goal judgment
    if norm(x(1:2)-goal(:,k))<20
        disp("Arrive Goal!! "+k);break;
    end

    %====Animation====
    hold off;
    ArrowLength=0.5;%Arrow length
    %robot
    quiver(x(1),x(2),ArrowLength*cos(x(3)),ArrowLength*sin(x(3)),'ok');hold on;
    plot(result.x(:,1),result.x(:,2),'-b');hold on;
    plot(goal(1,k),goal(2,k),'*r');hold on;
    plot(obstacle(:,1),obstacle(:,2),'*k');hold on;
    % Trajectory display
    if ~isempty(traj)
        for it=1:length(traj(:,1))/5
            ind=1+(it-1)*5;
            plot(traj(ind,:),traj(ind+1,:),'-g');hold on;
        end
    end
    axis(area);
    grid on;
    drawnow;
    %movcount=movcount+1;
    %mov(movcount) = getframe(gcf);% Get an animation frame
end
end
toc
%movie2avi(mov,'movie.avi');




