function T = time_execution( fn, N )
    %This function expects a function handle 'fn' and an array of sizes 'N'
    %
    %arrayfun applies a function handle to an array or set of arrays
    %
    %We would like to apply arrayfun to our 'time_execution_basic'
    %function, but cannot because it takes two arguments, one of which (the
    %function handle) is not part of an array.
    %   To circumvernt this problem, we will write a function 'time_single'
    % which does not need to be passed the handle of the function we want
    % to time (see below).
    T = arrayfun(@time_single,N);

    %time_single's implementation is equivalent to our time_execution_basic
    %function, but does not need to be passed the handle 'fn' because it
    %shares a workspace (and thus has access to the variables of)
    %time_execution.
    function t = time_single( n )
        tic
        fn(n);
        t = toc;
    end
end