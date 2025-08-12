remove_packages = ["torchvision","torchaudio","pytorch-mutex","pytorch","py3.12_cpu_0","cpuonly"]

file1 = open('requirements-original.txt', 'r')
lines = file1.readlines()

filtered_lines = []
for line in lines:
    try:
        line_prefix_index = line.index('=')
        line_prefix = substring = line[0:line_prefix_index]
    except:
        continue
    if line_prefix in remove_packages:
        print("Removed: ", line)
    else:
        filtered_lines.append(line+"\n")

# writing to file
file1 = open('requirements.txt', 'w')
file1.writelines(filtered_lines)
file1.close()