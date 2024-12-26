class Instance:

    def __init__(self, file_path):
        self.PRNs = []

        lines = self.read_txt(file_path)

        self.n = int(lines[0])
        self.V = int(lines[1])
        self.T = int(lines[2])
        self.M = int(lines[3])

        for i in range(4, 4 + self.M):
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


    
   

