from instance import Instance

class Solution:
    def __init__(self, instance):
        self.instance = instance
        #Cria matriz A, de a[i,j]
        self.allocation =  [[0 for _ in range(instance.M)] for _ in range(instance.n)]
        
    
    def create_initial_solution(self):
        pass


    def check_feasibility(self) -> bool:
        # Checa se o total de VRAM alocado na GPU é menor que V para todas as GPUs
        for gpu in range(self.instance.n):
            if not self.check_gpu_vram_capacity(gpu):
                return False
        # TODO: adicionar outras restrições
        
        return True
    

    def get_gpu_used_vram(self, gpu):
        return sum(self.allocation[gpu])
    
    def check_gpu_vram_capacity(self, gpu):
        return self.get_gpu_used_vram(gpu) <= self.instance.V

        
    def allocate(self, gpu, prn):
        self.allocation[gpu][prn] = 1

instance = Instance("./instances/dog_1.txt")
solution = Solution(instance)
solution.create_initial_solution()

