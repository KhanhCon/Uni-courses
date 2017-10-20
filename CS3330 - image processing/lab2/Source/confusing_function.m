function x = confusing_function(y , x)
    
    z = 5;
    a = -y;
    b = confusing_local_function(a,z);
    confusing_nested_function()

    function confusing_nested_function()
        b = confusing_local_function(a,b);
    end
end

function c = confusing_local_function(a,b)
    c = a + b;
    
end
