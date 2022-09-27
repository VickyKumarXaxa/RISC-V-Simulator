#code by Nema Ram Meghwal
#open file in reading mode
#global pc
#global variable IR
#local variable array
#local variable MCode
#function Fetch  
#store instruction in IR

file = open("instruction.mc","r")
lines =file.readlines()
IR = ''

pc = 0x0

def Fetch(lines):
    global pc
    
    array = []
    for i in lines:
        array.append(i.split())
        
        
    MCode = ''
    for i in array:
        for j in range(len(i)):
            if i[j] == str(hex(pc)):
                MCode = i[j+1]
                
                
    pc+=0x4
    
    return MCode


IR = Fetch(lines)
print(IR)

file.close()
