function y = vector_based_fn( ln )
    x = 1:ln;
    y = x.*cos(x) - sin(pi);
end