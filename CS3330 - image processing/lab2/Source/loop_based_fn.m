function y = loop_based_fn( ln )
    for i = 1:ln
        y(i) = i*cos(i) - sin(pi);
    end
   
end