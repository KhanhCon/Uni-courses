function res = normalize_vector(v)
%NORMALIZE_VECTOR Summary of this function goes here
%   Detailed explanation goes here

res= v/norm(v);
end

function n = norm(v)

n = sqrt(sum(v.^2));

end
