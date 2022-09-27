#Code by Samir P Salim
# Assume rd global variable
# TextMemory, and Datamemory are global
# RZ is global, output of ALU
# RB is detected in decode stage
# RY is a global variable


TextMemory = dict.fromkeys(range(0, 0x00000194, 4), 0)
DataMemory = dict.fromkeys(range(0x0FFFFFE8, 0x10000178, 4), 0)



StoreInst = ["sb", "sw", "sh"] 
LoadInst=["lb", "lw", "lh"]
def Memory_access(operation):
    global TextMemory, DataMemory
    if operation in StoreInst:
        TextMemory[RZ] = RB
        print(hex(RB)+" is written to "+hex(RZ))
    if operation in LoadInst:
        RY=Datamemory[RZ]
        print(hex(RY)+" is read from "+hex(RZ))
        
def Initialize():
    global Datamemory
    ile1=open("instruction.mc","r")
    lines1=file1.readlines()
    array = []
    for i in lines1:
        array.append(i.split())
        for i in array:
            if(len[i]>0):
                if(len[i][0]==10):
                    a=int(i[0][2:],16)
                    b=int(i[1][2:],16)
                    Datamemory[a]=b
                

