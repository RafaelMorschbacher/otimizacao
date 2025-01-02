from instance import Instance
from solution import Solution, log_and_print
import time

def run_experiment(instace_file_path, output_file_path ,max_iterations, perturbation_size):
    start_time = time.time()
    instance = Instance(instace_file_path)
    output_file = open(output_file_path, "w")
    # Create initial solution
    solution = Solution(instance, output_file)
    solution.create_initial_solution()
    #Find best solution with ILS
    best_solution = solution.ils(perturbation_size, max_iterations)

    log_and_print("=====================================================================", output_file)
    log_and_print("                        EXPERIMENT RESULTS                         ", output_file)
    log_and_print("=====================================================================", output_file)
    log_and_print(f'Initial solution objective function: {solution.objective_function()}', solution.output_file)
    log_and_print(f'Best solution objective function: {best_solution.objective_function()}', solution.output_file)
    log_and_print(f'Number of iterations: {max_iterations}', solution.output_file)
    log_and_print(f'Perturbation size: {perturbation_size}', solution.output_file)
    log_and_print("--- %.3f seconds ---" % (time.time() - start_time), solution.output_file)
    best_solution.print_solution()



def main():        
    run_experiment("./instances/dog_1.txt", "dog_1_it=150_pert=3.txt", max_iterations=150, perturbation_size=3)
   
    


main()