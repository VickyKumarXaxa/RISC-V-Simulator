

# Assume rd global variable
# TextMemory, and Datamemory are global
# RZ is global, output of ALU
# rd is detected in decode stage
# .


TextMemory = dict.fromkeys(range(0, 0x00000194, 4), 0)
DataMemory = dict.fromkeys(range(0x0FFFFFE8, 0x10000178, 4), 0)



#StoreInst = ["beq", "bne", "bge", "blt", "auipc", "jal", "jalr", "lui", "sb", "sw", "sh", "sd", "lb", "lw", "ld", "lh"]

def Memory_access(operation, lines):
    global DataMemory
    array = []
    if (lines):
        for i in range(len(lines)):
            if lines[i]!='\n':
                array.append(lines[i].split())
        print(array)
        for j in array:
            DataMemory[int(j[1], 16)] = int(j[0], 16)


