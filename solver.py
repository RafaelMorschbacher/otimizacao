from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary, GLPK
from instance import Instance
from solution import log_and_print


def solve_instance_glpk(instance_path, time_limit, output_file):

    # ======================LER ARQUIVO======================
    instance = Instance(instance_path)
    n = instance.n
    m = instance.M
    T = instance.T
    V = instance.V
    v = [prn['vram'] for prn in instance.PRNs]
    t = [prn['type'] for prn in instance.PRNs]

    #==========================================================

    # Matriz indicando se a PRN j é do tipo k
    z = [[1 if t[j] == k + 1 else 0 for j in range(m)] for k in range(T)]

    # Model
    model = LpProblem("Optimal_Distribution", LpMinimize)

    # Variaveis de decisao
    a = [[LpVariable(f"a_{i}_{j}", cat=LpBinary) for j in range(m)] for i in range(n)]
    x = [[LpVariable(f"x_{k}_{i}", cat=LpBinary) for i in range(n)] for k in range(T)]

    # F objetivo
    model += lpSum(x[k][i] for k in range(T) for i in range(n))

    # Restrição 1: A capacidade da GPU não pode ser excedida
    for i in range(n):
        model += lpSum(v[j] * a[i][j] for j in range(m)) <= V, f"Capacity_GPU_{i}"

    # Restrição 2: Cada PRN deve ser atribuído a exatamente uma GPU
    for j in range(m):
        model += lpSum(a[i][j] for i in range(n)) == 1, f"Assignment_PRN_{j}"

    # Restrição 3: Ativar x[k][i] se um PRN do tipo k for atribuído à GPU i
    for k in range(T):
        for i in range(n):
            model += x[k][i] >= lpSum(a[i][j] * z[k][j] for j in range(m)) / m, f"Activate_Type_{k}_GPU_{i}"

    # Resolver o problema usando GLPK
    model.solve(GLPK(msg=False, timeLimit=time_limit))

    # Resultados    
    if model.status == 1:  # Sol encontrada
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

# Rodar o solver 
output_file = open("output_dog_6.txt", "w") 
instance_path = "instances/dog_6.txt"
time_limit = 60*60*12  # 12 horas
solve_instance_glpk(instance_path, time_limit, output_file)