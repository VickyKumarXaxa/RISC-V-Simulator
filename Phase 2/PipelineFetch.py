
# code modifier Sahdev & Nemaram
# here Pc, IR, clock are gloabl variable.
# Function - Fetch for pipeline

file = open("instruction.mc","r")
lines =file.readlines()
IR = ''

pc = 0x0

def opcode(inst):    # returns opcode
    return (inst&0x7f)

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
    inst = int(MCode, 16)
    if(opcode(inst)==0x63 or opcode(inst)==0x17 or opcode(inst)==0x37 or opcode(inst)==0x6f):
        print("Branch or Jump Instruction")
    return MCode


IR = Fetch(lines)


file.close()
