%This script is equivalent to loop_vs_vector_basic but, because
%time_execution can handle vector input, does not require a for loop.
sizes = [1,10,100,1000,10000];
loop_time = time_execution(@loop_based_fn,sizes);
vector_time = time_execution(@vector_based_function,sizes);

figure,plot(sizes,loop_time,sizes,vector_time)
xlabel('size')
ylabel('time (s)')
legend('loop','vector','Location','NorthWest')

clear sizes loop_time vector_time