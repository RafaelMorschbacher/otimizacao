from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, GLPK
from instance import Instance
from solution import log_and_print


def solve_instance_glpk(instance_path, time_limit, output_file):
    # Parameters
    #n = 4                # Number of GPUs
    #m = 8                # Number of PRNs (neural network parts)
    #T = 3                # Number of PRN types
    #V = 16               # Maximum VRAM capacity per GPU
    #v = [4, 6, 5, 3, 7, 2, 8, 4]  # VRAM consumption of each PRN
    #t = [1, 1, 2, 3, 2, 3, 1, 2]  # Type of each PRN

    # ======================READING FILE======================
    instance = Instance(instance_path)
    n = instance.n
    m = instance.M
    T = instance.T
    V = instance.V
    v = [prn['vram'] for prn in instance.PRNs]
    t = [prn['type'] for prn in instance.PRNs]

    #==========================================================

    # Generate the z_kj matrix (constant values indicating if PRN j is of type k)
    z = [[1 if t[j] == k + 1 else 0 for j in range(m)] for k in range(T)]

    # Model
    model = LpProblem("Optimal_Distribution", LpMinimize)

    # Decision variables
    a = [[LpVariable(f"a_{i}_{j}", cat=LpBinary) for j in range(m)] for i in range(n)]
    x = [[LpVariable(f"x_{k}_{i}", cat=LpBinary) for i in range(n)] for k in range(T)]

    # Objective function: Minimize the number of GPUs with distinct types
    model += lpSum(x[k][i] for k in range(T) for i in range(n))

    # Constraint 1: GPU capacity cannot be exceeded
    for i in range(n):
        model += lpSum(v[j] * a[i][j] for j in range(m)) <= V, f"Capacity_GPU_{i}"

    # Constraint 2: Each PRN must be assigned to exactly one GPU
    for j in range(m):
        model += lpSum(a[i][j] for i in range(n)) == 1, f"Assignment_PRN_{j}"

    # Constraint 3: Activate x[k][i] if a PRN of type k is assigned to GPU i
    for k in range(T):
        for i in range(n):
            model += x[k][i] >= lpSum(a[i][j] * z[k][j] for j in range(m)) / m, f"Activate_Type_{k}_GPU_{i}"

    # Solve the problem using GLPK
    model.solve(GLPK(msg=False, timeLimit=time_limit))

    # Output the results    
    if model.status == 1:  # Optimal solution found
        log_and_print("Optimal solution found!", output_file)
        log_and_print(f"Objective value (number of distinct GPU types): {model.objective.value()}", output_file)

        log_and_print("\nPRN Allocation:",output_file)
        for i in range(n):
            allocated_prns = [j + 1 for j in range(m) if a[i][j].value() == 1]
            log_and_print(f"GPU {i + 1}: PRNs {allocated_prns}", output_file)

        log_and_print("\nGPU Types:", output_file)
        for i in range(n):
            active_types = [k + 1 for k in range(T) if x[k][i].value() == 1]
            log_and_print(f"GPU {i + 1}: Types {active_types}", output_file)
    else:
        log_and_print("No optimal solution found.", output_file)


output_file = open("output_dog_6.txt", "w") 
instance_path = "instances/dog_6.txt"
time_limit = 60*60*12  # 12 hours
solve_instance_glpk(instance_path, time_limit, output_file)