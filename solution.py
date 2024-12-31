from instance import Instance
import random
import time

class Solution:
    def __init__(self, instance, output_file=None):
        self.instance = instance
        #Cria matriz A, de a[i,j]
        self.allocation =  [[0 for _ in range(instance.M)] for _ in range(instance.n)]
        #Abre arquivo de saída
        self.output_file = output_file
        
    
    def create_initial_solution(self):
        for prn in range(self.instance.M):
            for gpu in range(self.instance.n):
                if self.gpu_can_fit_prn(gpu, prn):
                    self.allocate(gpu, prn)
                    break


    def check_feasibility(self) -> bool:
        # Restricao 1: Checa se o total de VRAM alocado na GPU é menor que V para todas as GPUs
        for gpu in range(self.instance.n):
            if not self.check_gpu_vram_capacity(gpu):
                self.log_and_self.log_and_print(f"Feasibility error: GPU {gpu} exceeds VRAM capacity.")
                return False
        
        # Restricao 3: Checa se cada PRN está alocado em exatamente uma GPU
        for prn in range(self.instance.M):
            total_allocations_for_prn = 0
            for gpu in range(self.instance.n):
                total_allocations_for_prn += self.allocation[gpu][prn]
            if total_allocations_for_prn != 1:
                self.log_and_self.log_and_print(f"Feasibility error: PRN {prn} is allocated {total_allocations_for_prn} times.")
                return False
            
        # TODO: adicionar outras restrições

        return True
    
    def objective_function(self):
        #soma a quantidade de tipos diferentes alocados em cada GPU
        total_allocated_types = 0
        for gpu in range(self.instance.n):
            total_allocated_types += self.get_gpu_number_of_allocated_types(gpu)
        return total_allocated_types
    
    #============================ Vizinhanca ============================

    def local_search(self, max_iterations=100):
        no_improve_count = 0
        max_no_improve = 100  # Número máximo de iterações sem melhora
        
        #Realiza busca local gerando vizinhos e aceitando o melhor.
        current_solution = self
        best_solution = current_solution
        best_objective = current_solution.objective_function()
        for _ in range(max_iterations):
            # Generate a neighbor solution
            neighbor = current_solution.generate_neighbor()
            neighbor_obj_function = neighbor.objective_function()
            # Evaluate the neighbor's objective function
            if neighbor_obj_function < best_objective:
                # If the neighbor is better, update the best solution
                self.log_and_print(f'Moving to neighbor with objective function = {neighbor_obj_function}')
                best_solution = neighbor
                best_objective = neighbor_obj_function
                current_solution = best_solution  # Move to the best neighbor
                no_improve_count = 0  # Reset contador
            else:
                no_improve_count += 1
            if no_improve_count >= max_no_improve:
                self.log_and_print("No improvement for 100 iterations. Stopping local search.")
                break
        return best_solution


    def generate_neighbor(self):
        neighbor = self.generate_copy()
        neighbor.move_random_prn()
        return neighbor

    def move_random_prn(self):
        # Randomly choose a PRN and two GPUs
        prn = random.choice(range(self.instance.M))
        current_gpu = next(gpu for gpu in range(self.instance.n) if self.allocation[gpu][prn] == 1)
        candidate_gpus = [gpu for gpu in range(self.instance.n) if gpu != current_gpu and self.gpu_can_fit_prn(gpu, prn)]

        # If there are no candidates, skip this move
        if not candidate_gpus:
            self.log_and_print(f"No valid GPUs found to move PRN {prn} from GPU {current_gpu}.")
            return False
        
        # Randomly choose a target GPU from the valid candidates
        target_gpu = random.choice(candidate_gpus)
       
        # Move PRN from the current GPU to the target GPU
        self.disallocate(current_gpu, prn)
        self.allocate(target_gpu, prn)
        
        # Check feasibility and return if the move is valid
        if self.check_feasibility():
            return True
        else:
            # If moving the PRN violates feasibility, undo the move
            self.disallocate(target_gpu, prn)
            self.allocate(current_gpu, prn)
            return False
        
    def ils(self, perturbation_size, max_iterations):
        current_solution = self
        best_solution = current_solution
        best_objective = current_solution.objective_function()
        no_improve_count = 0
        max_no_improve = 50  # Número máximo de iterações sem melhora
        self.log_and_print("=====================================================================")
        self.log_and_print("                        ITERATED LOCAL SEARCH")
        self.log_and_print("=====================================================================")
        for iteration in range(max_iterations):
            self.log_and_print(f"Iteration {iteration} - Best Objective: {best_objective}")
            
            # Busca local
            current_solution = current_solution.local_search()
            current_objective = current_solution.objective_function()

            # Atualiza melhor solução
            if current_objective < best_objective:
                best_solution = current_solution
                best_objective = current_objective
                no_improve_count = 0 
            else:
                no_improve_count += 1

            # Critério de parada baseado em falta de melhora
            if no_improve_count >= max_no_improve:
                self.log_and_print(f'No improvement for multiple iterations. Stopping ILS after {iteration+1} iterations.')
                break

            # Perturbação
            current_solution = best_solution.generate_copy()
            current_solution.perturbation(perturbation_size)

        return best_solution

    def perturbation(self, k):
        for _ in range(k):
            if not self.move_random_prn():
                continue
        # Após a perturbação, reequilibra alocações aleatórias
        for prn in range(self.instance.M):
            current_gpu = next((gpu for gpu in range(self.instance.n) if self.allocation[gpu][prn] == 1), None)
            if current_gpu is None:  # PRN desalocado, tentar realocar
                target_gpu = random.choice([gpu for gpu in range(self.instance.n) if self.gpu_can_fit_prn(gpu, prn)])
                self.allocate(target_gpu, prn)


    #============================ FIM Vizinhanca ============================

    def generate_copy(self):
        copy = Solution(self.instance, self.output_file)
        copy.allocation = [gpu.copy() for gpu in self.allocation]
        return copy

    def check_gpu_vram_capacity(self, gpu):
        return self.get_gpu_used_vram(gpu) <= self.instance.V

    def get_gpu_used_vram(self, gpu):
        used_vram = 0
        for prn in range(self.instance.M):
            if self.allocation[gpu][prn] == 1:
                used_vram += self.instance.PRNs[prn]['vram']
        
        return used_vram
    
    def gpu_can_fit_prn(self, gpu, prn):
        return self.get_gpu_used_vram(gpu) + self.instance.PRNs[prn]['vram'] <= self.instance.V
        
    def allocate(self, gpu, prn):
        self.allocation[gpu][prn] = 1

    def disallocate(self, gpu, prn):
        self.allocation[gpu][prn] = 0

    def get_gpu_number_of_allocated_types(self, gpu) -> int:
        return len(self.get_gpu_allocated_types(gpu))
    
    def get_gpu_allocated_types(self, gpu) -> set:
        allocated_types = set()
        for prn in range(self.instance.M):
            if self.allocation[gpu][prn] == 1:
                prn_type = self.instance.PRNs[prn]['type']
                allocated_types.add(prn_type)
        return allocated_types
    
    def log_and_print(self, message):
        log_and_print(message, self.output_file)


    def print_solution(self):
        self.log_and_print("=====================================================================")
        self.log_and_print("                        CURRENT SOLUTION")
        self.log_and_print("=====================================================================")
        for gpu in range(self.instance.n):
            self.log_and_print("=================================")
            self.log_and_print(f"GPU {gpu}")
            self.log_and_print(f"allocated memory: {self.get_gpu_used_vram(gpu)}")
            self.log_and_print(f"{self.get_gpu_number_of_allocated_types(gpu)} allocated types: {self.get_gpu_allocated_types(gpu)}")
            self.log_and_print("Allocated PRNs: ")
            for prn in range(self.instance.M):
                if self.allocation[gpu][prn] == 1:
                    self.log_and_print(f"PRN {prn}, size: {self.instance.PRNs[prn]['vram']}, type: {self.instance.PRNs[prn]['type']}")
        self.log_and_print("=================================")
        self.log_and_print('Feasibility: ' +str(self.check_feasibility()))
        self.log_and_print('Objective function: ' + str(self.objective_function()))
        self.log_and_print("=================================")

def log_and_print(message, output_file=None):
    print(message)
    if output_file:
        output_file.write(message + '\n')
