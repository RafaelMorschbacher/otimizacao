class Instance:

    def __init__(self, file_path):
        self.PRNs = []

        lines = self.read_txt(file_path)

        self.n_gpus = int(lines[0])
        self.V_gpu_capacity = int(lines[1])
        self.T_number_of_types = int(lines[2])
        self.m_number_of_PRNs = int(lines[3])

        for i in range(4, 4 + self.m_number_of_PRNs):
            line_values = lines[i].split('\t')
            prn_type = int(line_values[0])
            prn_vram = int(line_values[1])
            self.PRNs.append({'type': prn_type, 'vram': prn_vram})
 

    def read_txt(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()
        lines = content.split('\n')
        clean_lines = [line.strip() for line in lines if line.strip()]
        return clean_lines

instance = Instance('./instances/dog_1.txt')

print(f"Number of GPUs: {instance.n_gpus}")
print(f"GPU Capacity: {instance.V_gpu_capacity}")
print(f"Number of Types: {instance.T_number_of_types}")
print(f"Number of PRNs: {instance.m_number_of_PRNs}")
print("PRNs:")
for prn in instance.PRNs:
    print(prn)


    
   

