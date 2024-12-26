from instance import Instance

class Solution:
    def __init__(self, instance):
        self.instance = instance
        #Cria matriz A, de a[i,j]
        self.allocation =  [[0 for _ in range(instance.M)] for _ in range(instance.n)]

        
    
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
                print(f"Feasibility error: GPU {gpu} exceeds VRAM capacity.")
                return False
        
        # Restricao 2: Checa se cada PRN está alocado em exatamente uma GPU
        for prn in range(self.instance.M):
            total_allocations_for_prn = 0
            for gpu in range(self.instance.n):
                total_allocations_for_prn += self.allocation[gpu][prn]
            if total_allocations_for_prn != 1:
                print(f"Feasibility error: PRN {prn} is allocated {total_allocations_for_prn} times.")
                return False
            
        # TODO: adicionar outras restrições

        return True
    
    def objective_function(self):
        #soma a quantidade de tipos diferentes alocados em cada GPU
        total_allocated_types = 0
        for gpu in range(self.instance.n):
            total_allocated_types += self.get_gpu_number_of_allocated_types(gpu)
        return total_allocated_types

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

    def get_gpu_number_of_allocated_types(self, gpu) -> int:
        return len(self.get_gpu_allocated_types(gpu))
    
    def get_gpu_allocated_types(self, gpu) -> set:
        allocated_types = set()
        for prn in range(self.instance.M):
            if self.allocation[gpu][prn] == 1:
                prn_type = instance.PRNs[prn]['type']
                allocated_types.add(prn_type)
        return allocated_types
    
    
    

    def print_current_solution(self):
        print("------------------")
        print('Feasibility: ' +str(self.check_feasibility()))
        print('Objective function: ' + str(self.objective_function()))
        print("------------------")
        for gpu in range(self.instance.n):
            print("=================================")
            print(f"gpu {gpu} has {self.get_gpu_used_vram(gpu)} of memory allocated and {self.get_gpu_number_of_allocated_types(gpu)} types allocated")
            print(f"Allocated types: {self.get_gpu_allocated_types(gpu)}")
            print("Allocated PRNs:")
            for prn in range(self.instance.M):
                if self.allocation[gpu][prn] == 1:
                    print(f"PRN {prn} with {self.instance.PRNs[prn]['vram']} of memory and type {self.instance.PRNs[prn]['type']}")
        

instance = Instance("./instances/dog_1.txt")
solution = Solution(instance)
solution.create_initial_solution()
solution.print_current_solution()


