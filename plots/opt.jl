using Optim
using ForwardDiff

# set the initial guess and penalty value
penalty = 10000.0
global const var = Ref{Int64}(0)

function f!(x)
    # extract a and rotation from the input vector x
    a = x[1]
    rotation = x[2]
    # check if a and rotation are within the constraints
    if a < 0.08 || a > 0.13 || rotation < 45 || rotation > 120
        # if not, apply a penalty
        return  penalty
    else
        global var[] += 1
        # call the Python script to interpolate the data at (a, rotation)
        run(`python3 vis_cassini.py $a $rotation`)
        
        # read the interpolated value from the itp.txt file
        itp_val = parse(Float64, read("itp.txt", String))
        
        # apply the penalty method to the objective function
        return -itp_val + penalty * max(0, 0.08 - a)^2 + penalty * max(0, a - 0.13)^2 + penalty * max(0, 45 - rotation)^2 + penalty * max(0, rotation - 120)^2
    end
end

function g!(G, x)
    for i = 1:length(x)
        # perturb the i-th element of x
        if i == 1
            eps = 1e-4
            x_plus = copy(x)
            x_plus[i] += eps
            x_minus = copy(x)
            x_minus[i] -= eps
        else
            eps = 1e-1
            x_plus = copy(x)
            x_plus[i] += eps
            x_minus = copy(x)
            x_minus[i] -= eps
        end
        # compute the gradient approximation using central difference
        G[i] = (f!(x_plus) - f!(x_minus)) / (2 * eps)
    end
end

function cb(os)
    vec = os.metadata["centroid"]
    
    a = vec[1]
    b = vec[2]
    
    run(`python3 vis_cassini.py $a $b`)
        
    # read the interpolated value from the itp.txt file
    itp_val = parse(Float64, read("itp.txt", String))
    
    println(string(a," ", b," ", itp_val, " ", var[]))
    return false
end


function cb1(os)
    vec = os.metadata["x"]
    
    a = vec[1]
    b = vec[2]
    
    run(`python3 vis_cassini.py $a $b`)
        
    # read the interpolated value from the itp.txt file
    itp_val = parse(Float64, read("itp.txt", String))
    
    
    println(string(a," ", b," ", itp_val, " ", var[]))
    return false
end

x0 = [0.097, 75.0]
x1 = [0.084, 115.0]
x2 = [0.113, 65.0]

point_list = [x0, x1, x2]

println("NM")
for x_ in point_list
    a = x_[1]
    b = x_[2]
    
    run(`python3 vis_cassini.py $a $b`)
        
    # read the interpolated value from the itp.txt file
    itp_val = parse(Float64, read("itp.txt", String))
    
    println(string(a," ", b," ", itp_val, " ", var[]))


    #res1 = optimize(f!, x_, NelderMead(), Optim.Options(extended_trace=true, callback=cb, f_tol=10e-3))
    #println(string(x_, "    ", res1.minimizer, "    ", var, "    ", -res1.minimum))
    println(string("-------------"))
    global var[] = 0
end


println("LBFGS-A")
for x_ in point_list
    a = x_[1]
    b = x_[2]
    
    run(`python3 vis_cassini.py $a $b`)
        
    # read the interpolated value from the itp.txt file
    itp_val = parse(Float64, read("itp.txt", String))
    
    println(string(a," ", b," ", itp_val, " ", var[]))

    #res1 = optimize(f!, x_, LBFGS(), Optim.Options(extended_trace=true, callback=cb1, f_calls_limit=150))
    #println(string(x_, "    ", res1.minimizer, "    ", var, "    ", -res1.minimum))
    println(string("-------------"))
    global var[] = 0
end


