from instance import Instance

class Solution:
    def __init__(self, instance):
        self.instance = instance
        #Cria matriz A, de a[i,j]
        self.allocation =  [[0 for _ in range(instance.M)] for _ in range(instance.n)]

        
    
    def create_initial_solution(self):
        for prn in range(self.instance.M):
            for gpu in range(self.instance.n):
                if self.get_gpu_used_vram(gpu) + self.instance.PRNs[prn]['vram'] <= self.instance.V:
                    self.allocate(gpu, prn)
                    break


    def check_feasibility(self) -> bool:
        # Checa se o total de VRAM alocado na GPU é menor que V para todas as GPUs
        for gpu in range(self.instance.n):
            if not self.check_gpu_vram_capacity(gpu):
                return False
        # TODO: adicionar outras restrições

        return True
    

    def check_gpu_vram_capacity(self, gpu):
        return self.get_gpu_used_vram(gpu) <= self.instance.V

    def get_gpu_used_vram(self, gpu):
        used_vram = 0
        for prn in range(self.instance.M):
            if self.allocation[gpu][prn] == 1:
                used_vram += self.instance.PRNs[prn]['vram']
        
        return used_vram
    
        
    def allocate(self, gpu, prn):
        self.allocation[gpu][prn] = 1

    def print_current_solution(self):
        print("------------------")
        print('Feasibility: ' +str(self.check_feasibility()))
        print("------------------")
        for gpu in range(self.instance.n):
            print("=================================")
            print(f"gpu {gpu} has {self.get_gpu_used_vram(gpu)} of memory allocated")
            print("Allocated PRNs:")
            for prn in range(self.instance.M):
                if self.allocation[gpu][prn] == 1:
                    print(f"PRN {prn} with {self.instance.PRNs[prn]['vram']} of memory")
        

instance = Instance("./instances/dog_1.txt")
solution = Solution(instance)
solution.create_initial_solution()
solution.print_current_solution()


