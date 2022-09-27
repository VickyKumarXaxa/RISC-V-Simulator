from bitstring import BitArray
import math
IR = ''
pc = 0x0
pc_temp = 0x0
rd = 0x0
rs1 = 0
rs2 = 0
RA = 0x0
RB = 0x0
RZ = 0x0
RY = 0x0
imme = 0x0
clock = 0
Control = 0
multiClock = 0
register = [] # global list 
memory=[]
cap=-1
for i in range(32):
    register.append(0)

register[2] = 0x7FFFFFF0 	#Stack Pointer
dataDependence = ['0','0']
instcount = 0

#decode buffers
decodeRA = 0
decodeRB = 0
decodeRD = 0

#ALU buffers
aluRZ = 0

#Memory buffers
memRY = 0

#data forwarding registers
aludfRZ = 0
memdfRZ = 0

dataTransferCount = 0	#no of data transfer instructions
aluCount = 0	#no of mathematical instructions
controlCount = 0	#no. of control instructions
stallCount = 0		#no of stalls
dataHazard = 0		#no. of data hazard
controlHazard = 0	#no of control hazard
branchMispridiction = 0
stallDataHazard = 0
stallControlHazard = 0


knobPipeline = 'off'
knobDataFor = 'off'
knobRegister = 'off'
knobPipelineRegister = 'off'
knobSpecial = 'off'
specialInst = -1
datadependence=[0,0,0]
TextMemory = dict.fromkeys(range(0, 0x00000194, 1), 0)
DataMemory = dict.fromkeys(range(0x10000000, 0x10000194, 1), 0)
StoreInst = ["sb", "sw", "sh", "sd"]
loadInst = ["lb", "lw", "ld", "lh", "lui"]



bo_bits = 0
index_bits = 0
tag_bits = 0
data_copy = 0
cachesize = 0
blocksize = 0
n = 0
SA = {}
InsNumHits = 0
InsNUmMisses = 0

Bo = 0                  # Block offset
ind = 0                 # index bits
tag = 0                 # tags
data = 0
pc = 0x0

cachesize=int(input("Enter cache size(in bytes without unit):"))
blocksize=int(input("Enter cache block size(in bytes without unit):"))
n=int(input("Enter number of ways for Set Associative:"))
blocks=cachesize/blocksize
numsets=blocks/n


################################# Instruction Cache part ##########
def inst_fetch(lines):
    global pc, data
    global bo_bits, index_bits, tag_bits, data_copy, cachesize, blocksize, n, SA
    array = []
    for i in lines:
        array.append(i.split())
        
    MCode = ''
    for i in array:
        for j in range(len(i)):
            if i[j] == str(hex(pc)):
                MCode = i[j+1]  

    data_copy = pc
    data = int(MCode, 16)

    # instruction address sent from BTB or IAG
    # number of bits in instruction adddress
    add_bits=32                           # 32 for risc-v 32 bit ISA
    bo_bits=int(math.log2(blocksize))     # number of bits in block offset
    index_bits=int(math.log2(numsets))    # number of bits in index
    tag_bits=add_bits-bo_bits-index_bits  # number of bits in tag

    Size = int(blocks)//int(n)
    M = [ [0, 0] for j in range(Size) ]
    SA = {i:M for i in range(int(n))}
    pc+=0x4


def indexAndTag(data_copy):
    global ind, tag
    if index_bits == 0:
        ind = 0
    elif index_bits == 1:
        ind = data_copy & 1
        tag = data_copy>>1
    elif index_bits == 2:
        ind = data_copy & 3
        tag = data_copy>>2
    elif index_bits == 3:
        ind = data_copy & 7
        tag = data_copy>>3
    elif index_bits == 4:
        ind = data_copy & 15
        tag = data_copy>>4
    elif index_bits == 5:
        ind = data_copy & 31
        tag = data_copy>>5
    elif index_bits == 6:
        ind = data_copy & 63
        tag = data_copy>>6
    elif index_bits == 7:
        ind = data_copy & 127
        tag = data_copy>>7
    elif index_bits == 8:
        ind = data_copy & 255
        tag = data_copy>>8
    elif index_bits == 9:
        ind = data_copy & 511
        tag = data_copy>>9
    elif index_bits == 10:
        ind = data_copy & 1023
        tag = data_copy>>10


def BlockOffSet(data_copy):
    global Bo
    if bo_bits == 0:
        Bo = 0
    elif bo_bits == 1:
        Bo = data_copy & 1
        data_copy = data_copy>>1
    elif bo_bits == 2:
        Bo = data_copy & 3
        data_copy = data_copy>>2
    elif bo_bits == 3:
        Bo = data_copy & 7
        data_copy = data_copy>>3
    elif bo_bits == 4:
        Bo = data_copy & 15
        data_copy = data_copy>>4
    elif bo_bits == 5:
        Bo = data_copy & 31
        data_copy = data_copy>>5
    elif bo_bits == 6:
        Bo = data_copy & 63
        data_copy = data_copy>>6
    elif bo_bits == 7:
        Bo = data_copy & 127
        data_copy = data_copy>>7
    elif bo_bits == 8:
        Bo = data_copy & 255
        data_copy = data_copy>>8
    elif bo_bits == 9:
        Bo = data_copy & 511
        data_copy = data_copy>>9
    elif bo_bits == 10:
        Bo = data_copy & 1023
        data_copy = data_copy>>10
    
    indexAndTag(data_copy)


def UpdateSAInst():
    BlockOffSet(data_copy)
    global SA, ind, InsNUmMisses, InsNumHits
    predict = ""
    for way in SA:
        for index in range(len(SA[way])):
            if index == ind:
                if SA[way][index][0] == tag:
                    predict = "hit"
                    InsNumHits += 1
                    return SA[way][index][1]
                else:
                    predict = "miss"
                    InsNUmMisses += 1
                    SA[way][index][0] = tag
                    if 0x10000000<pc:
                        SA[way][index][1] = data
                    else:
                        SA[way][index][1] = data

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
    
def opcode(inst):  
    if type(inst)==str:
        return ''
    return (inst&0x7f)

def pipelineFetch(lines):
    global pc, multiClock
    multiClock = multiClock + 1

    array = []
    for i in lines:
        array.append(i.split())

    MCode = ''
    for i in array:
        for j in range(len(i)):
            if i[j] == str(hex(pc)):
                MCode = i[j+1]

    pc+=0x4
    inst = 0
    if MCode != '':
        inst = int(MCode, 16)
    if(opcode(inst)==0x63 or opcode(inst)==0x17 or opcode(inst)==0x37 or opcode(inst)==0x6f):
        print("Branch or Jump Instruction")
    return MCode

####################################################################################

# code by ashish sulania
# assuming RA,RB,rd and imme as global variable and register as a global list 
# RA=register[rs1],RB=register[rs2]
# decode function returns mnemonic of instruction and update global variables RA,RB,rd,imme 
# call decode() function for non pipeline implementation and for pipeline implementation call pipelinedecode() function

def opc(inst):    # returns opcode
    if type(inst)==str:
        return ''
    return (inst&0x7f)

def fun3(inst):   # returns fun3
    if type(inst)==str:
        return ''
    return ((inst >> 12)&0x7)

def fun_7(inst):  # returns fun7
    if type(inst)==str:
        return ''
    return ((inst>>25)&0x7f)

def r_d(inst):    # returns rd
    if type(inst)==str:
        return ''
    return ((inst>>7)&0x1f)

def rs_1(inst):   # returns rs1
    if type(inst)==str:
        return ''
    return ((inst>>15)&0x1f)

def rs_2(inst):   # returns rs2
    if type(inst)==str:
        return ''
    return ((inst>>20)&0x1f)

def imm_12(inst): # returns imm12 of i format
    if type(inst)==str:
        return ''
    return ((inst>>20)&0xfff)

def imm_20(inst): # returns imm20 of u format
    if type(inst)==str:
        return ''
    return ((inst>>12)&0xfffff)

def sign_extend(value, bits):  # compare sign extended number and returns appropriate integer
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

def cals(a,b):    # calculates 12 bits of s format  imm[11:0]=imm[11:5]imm[4:0]
    a=a<<5
    a=a|b
    return a

def calsb(imm7,imm5):  # calculates 12 bits of sb format imm[12:1]=imm[12]imm[11]imm[10:5]imm[4:1]
    imm11=imm5&0x1     #imm[11] 1 bit
    imm4=imm5>>1       # imm[4:1] 4 bits
    imm6=imm7&0x3f     # imm[10:5] 6 bits
    imm10=(imm6<<4)|imm4     # imm[10:1] 10 bits
    imm11=(imm11<<10)|imm10  # imm[11:1] 11 bits
    imm12=imm7>>6            # imm[12] 1 bit
    imm12=(imm12<<11)|imm11  # imm[12:1] 12 bits
    return imm12


def decode(inst):
    global RA,RB,imme,rd,control,rs1,rs2, dataTransferCount, aluCount, controlCount
    print("decode:")
    if(opc(inst)==0x33):  # r format 
        print("instruction is of r format")
        control=1
        if(fun3(inst)==0x0 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("add","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "add"
        elif(fun3(inst)==0x0 and fun_7(inst)==0x20):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("sub","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "sub"
        elif(fun3(inst)==0x7 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("and","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "and"
        elif(fun3(inst)==0x6 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("or","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "or"
        elif(fun3(inst)==0x1 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("sll","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "sll"
        elif(fun3(inst)==0x2 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("slt","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "slt"
        elif(fun3(inst)==0x5 and fun_7(inst)==0x20):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("sra","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "sra"
        elif(fun3(inst)==0x5 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("srl","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "srl"
        elif(fun3(inst)==0x4 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("xor","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "xor"
        elif(fun3(inst)==0x0 and fun_7(inst)==0x01):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("mul","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "mul"
        elif(fun3(inst)==0x4 and fun_7(inst)==0x01):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("div","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "div"
        elif(fun3(inst)==0x6 and fun_7(inst)==0x01):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("rem","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            aluCount = aluCount + 1
            return "rem"

    elif(opc(inst)==0x13):  # i format
        print("instruction is of i format(arithmetic)")
        control=1
        if(fun3(inst)==0x0):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            RA=register[rs1]
            imme=sign_extend(imm12,12)
            print("addi rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value [rs1]:",RA)
            aluCount = aluCount + 1
            return "addi"
        elif(fun3(inst)==0x7):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            RA=register[rs1]
            imme=sign_extend(imm12,12)
            print("andi rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value [rs1]:",RA)
            aluCount = aluCount + 1
            return "andi"
        elif(fun3(inst)==0x6):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            RA=register[rs1]
            imme=sign_extend(imm12,12)
            print("ori rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value [rs1]:",RA)
            aluCount = aluCount + 1
            return "ori"
    elif(opc(inst)==0x03):
        print("instruction is of i format(load)")
        control=1
        if(fun3(inst)==0x0):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            RA=register[rs1]
            imme=sign_extend(imm12,12)
            print("lb rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value [rs1]:",RA)
            dataTransferCount = dataTransferCount + 1
            return "lb"
        elif(fun3(inst)==0x1):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            RA=register[rs1]
            imme=sign_extend(imm12,12)
            print("lh rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value [rs1]:",RA)
            dataTransferCount = dataTransferCount + 1
            return "lh"
        elif(fun3(inst)==0x2):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            RA=register[rs1]
            imme=sign_extend(imm12,12)
            print("lw rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value [rs1]:",RA)
            dataTransferCount = dataTransferCount + 1
            return "lw"
    elif(opc(inst)==0x67 and fun3(inst)==0x0):
        print("instruction is of i format")
        control=1
        rs1=rs_1(inst)
        rd=r_d(inst)
        imm12=imm_12(inst)
        RA=register[rs1]
        imme=sign_extend(imm12,12)
        print("jalr rs1:",rs1,"rd:",rd,"imm:",imme)
        print("value [rs1]:",RA)
        controlCount = controlCount + 1
        return "jalr"

    elif(opc(inst)==0x23):  # s format
        print("instruction is of s format")
        control=0
        if(fun3(inst)==0x0):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:0] 5 bits
            imm7=fun_7(inst) #imm[11:5] 7 bits
            imm12=cals(imm7,imm5)
            RA=register[rs1]
            RB=register[rs2]
            imme=sign_extend(imm12,12)
            print("sb rs1:",rs1,"rs2:",rs2,"imm:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            dataTransferCount = dataTransferCount + 1
            return "sb"
        elif(fun3(inst)==0x1):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:0] 5 bits
            imm7=fun_7(inst) #imm[11:5] 7 bits
            imm12=cals(imm7,imm5)
            RA=register[rs1]
            RB=register[rs2]
            imme=sign_extend(imm12,12)
            print("sh rs1:",rs1,"rs2:",rs2,"imm:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            dataTransferCount = dataTransferCount + 1
            return "sh"
        elif(fun3(inst)==0x2):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:0] 5 bits
            imm7=fun_7(inst) #imm[11:5] 7 bits
            imm12=cals(imm7,imm5)
            RA=register[rs1]
            RB=register[rs2]
            imme=sign_extend(imm12,12)
            print("sw rs1:",rs1,"rs2:",rs2,"imm:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            dataTransferCount = dataTransferCount + 1
            return "sw"

    elif(opc(inst)==0x63):  # sb format
        print("instruction is of sb format(branch)")
        control=0
        if(fun3(inst)==0x0):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            RA=register[rs1]
            RB=register[rs2]
            imme=sign_extend(imm12,12)*2
            print("beq rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            controlCount = controlCount + 1
            return "beq"
        elif(fun3(inst)==0x1):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            RA=register[rs1]
            RB=register[rs2]
            imme=sign_extend(imm12,12)*2
            print("bne rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            controlCount = controlCount + 1
            return "bne"
        elif(fun3(inst)==0x4):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            RA=register[rs1]
            RB=register[rs2]
            imme=sign_extend(imm12,12)*2
            print("blt rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            controlCount = controlCount + 1
            return "blt"
        elif(fun3(inst)==0x5):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            RA=register[rs1]
            RB=register[rs2]
            imme=sign_extend(imm12,12)*2
            print("bge rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            controlCount = controlCount + 1
            return "bge"

    elif(opc(inst)==0x17):   # u format
        print("instruction is of u format")
        control=1
        rd=r_d(inst)
        imm20=imm_20(inst) #imm[31:12] 20 bits
        imme=sign_extend(imm20,20)
        print("auipc rd:",rd,"imm:",imme)
        aluCount = aluCount + 1
        return "auipc"
    elif(opc(inst)==0x37):
        print("instruction is of u format")
        rd=r_d(inst)
        imm20=imm_20(inst) #imm[19:0] 20 bits
        imme=sign_extend(imm20,20)
        print("lui rd:",rd,"imm:",imme)
        dataTransferCount = dataTransferCount + 1
        return "lui"

    elif(opc(inst)==0x6f):  # uj format
        print("instruction is of uj format")
        control=1
        rd=r_d(inst)
        imm19=(inst>>12)&0xff   # imm[19:12] 8 bits
        imm11=(inst>>20)&0x1    # imm[11] 1 bit
        imm10=(inst>>21)&0x3ff  # imm[10:1] 10 bits
        imm20=(inst>>31)&0x1    # imm[20] 1 bit
        imm11=(imm11<<10)|imm10 # imm[11:1] 11 bits
        imm19=(imm19<<11)|imm11 # imm[19:1] 19 bits
        imm20=(imm20<<19)|imm19 # imm[20:1] 20 bits
        imme=sign_extend(imm20,20)*2
        print("jal rd:",rd,"imm[20:0]:",imme)
        controlCount = controlCount + 1
        return "jal"


# global variables imme,rd,control,multiClock
# decode buffer registers(pipeline registers) decodeRA,decodeRB,decodeRD
# decodeRA,decodeRB stores intial values contains registers rs1 and rs2 and decodeRD=rd(value of destination register)
# control=1 if there is a destination register in instruction else control=0
# datadependence=[0,0,0] is a global list for checking data hazards that stores last two instruction's rd values and current rd value
# global variable instcount defined in main initially equals to 0 

def pipelinedecode(inst):
    global imme,rd,control,multiClock,rs1,rs2, datadependence, aluCount, controlCount, dataTransferCount
    global decodeRA,decodeRB,decodeRD,instcount
    instcount=instcount + 1     # counts number of instructions
    multiClock = multiClock + 1  # updating multiclock
    if(instcount>3):
        datadependence[0]=datadependence[1]
        datadependence[1]=datadependence[2]
    print("decode:")
    if(opc(inst)==0x33):  # r format 
        print("instruction is of r format")
        control=1
        if(fun3(inst)==0x0 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("add","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "add"
        elif(fun3(inst)==0x0 and fun_7(inst)==0x20):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("sub","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "sub"
        elif(fun3(inst)==0x7 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("and","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "and"
        elif(fun3(inst)==0x6 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("or","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "or"
        elif(fun3(inst)==0x1 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("sll","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "sll"
        elif(fun3(inst)==0x2 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("slt","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "slt"
        elif(fun3(inst)==0x5 and fun_7(inst)==0x20):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("sra","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "sra"
        elif(fun3(inst)==0x5 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("srl","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "srl"
        elif(fun3(inst)==0x4 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("xor","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "xor"
        elif(fun3(inst)==0x0 and fun_7(inst)==0x01):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("mul","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "mul"
        elif(fun3(inst)==0x4 and fun_7(inst)==0x01):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("div","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "div"
        elif(fun3(inst)==0x6 and fun_7(inst)==0x01):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            decodeRD=rd
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("rem","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            aluCount = aluCount + 1
            return "rem"

    elif(opc(inst)==0x13):  # i format
        print("instruction is of i format(arithmetic)")
        control=1
        if(fun3(inst)==0x0):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            decodeRA=register[rs1]
            decodeRD=rd
            imme=sign_extend(imm12,12)
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("addi rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value in buffer register decodeRA:",decodeRA)
            aluCount = aluCount + 1
            return "addi"
        elif(fun3(inst)==0x7):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            decodeRA=register[rs1]
            decodeRD=rd
            imme=sign_extend(imm12,12)
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("andi rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value in buffer register decodeRA:",decodeRA)
            aluCount = aluCount + 1
            return "andi"
        elif(fun3(inst)==0x6):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            decodeRA=register[rs1]
            decodeRD=rd
            imme=sign_extend(imm12,12)
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("ori rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value in buffer register decodeRA:",decodeRA)
            aluCount = aluCount + 1
            return "ori"
    elif(opc(inst)==0x03):
        print("instruction is of i format(load)")
        control=1
        if(fun3(inst)==0x0):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            decodeRA=register[rs1]
            decodeRD=rd
            imme=sign_extend(imm12,12)
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("lb rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value in buffer register decodeRA:",decodeRA)
            dataTransferCount = dataTransferCount + 1
            return "lb"
        elif(fun3(inst)==0x1):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            decodeRA=register[rs1]
            decodeRD=rd
            imme=sign_extend(imm12,12)
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("lh rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value in buffer register decodeRA:",decodeRA)
            dataTransferCount = dataTransferCount + 1
            return "lh"
        elif(fun3(inst)==0x2):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            decodeRA=register[rs1]
            decodeRD=rd
            imme=sign_extend(imm12,12)
            if(instcount==1):
                datadependence[0]=rd
            elif(instcount==2):
                datadependence[1]=rd
            elif(instcount>=3):
                datadependence[2]=rd
            print("lw rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value in buffer register decodeRA:",decodeRA)
            dataTransferCount = dataTransferCount + 1
            return "lw"
    elif(opc(inst)==0x67 and fun3(inst)==0x0):
        print("instruction is of i format")
        control=1
        rs1=rs_1(inst)
        rd=r_d(inst)
        imm12=imm_12(inst)
        decodeRA=register[rs1]
        decodeRD=rd
        imme=sign_extend(imm12,12)
        if(instcount==1):
            datadependence[0]=rd
        elif(instcount==2):
            datadependence[1]=rd
        elif(instcount>=3):
            datadependence[2]=rd
        print("jalr rs1:",rs1,"rd:",rd,"imm:",imme)
        print("value in buffer register decodeRA:",decodeRA)
        controlCount = controlCount + 1
        return "jalr"

    elif(opc(inst)==0x23):  # s format
        print("instruction is of s format")
        control=0
        if(fun3(inst)==0x0):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:0] 5 bits
            imm7=fun_7(inst) #imm[11:5] 7 bits
            imm12=cals(imm7,imm5)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            imme=sign_extend(imm12,12)
            print("sb rs1:",rs1,"rs2:",rs2,"imm:",imme)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            dataTransferCount = dataTransferCount + 1
            return "sb"
        elif(fun3(inst)==0x1):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:0] 5 bits
            imm7=fun_7(inst) #imm[11:5] 7 bits
            imm12=cals(imm7,imm5)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            imme=sign_extend(imm12,12)
            print("sh rs1:",rs1,"rs2:",rs2,"imm:",imme)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            dataTransferCount = dataTransferCount + 1
            return "sh"
        elif(fun3(inst)==0x2):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:0] 5 bits
            imm7=fun_7(inst) #imm[11:5] 7 bits
            imm12=cals(imm7,imm5)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            imme=sign_extend(imm12,12)
            print("sw rs1:",rs1,"rs2:",rs2,"imm:",imme)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            dataTransferCount = dataTransferCount + 1
            return "sw"

    elif(opc(inst)==0x63):  # sb format
        print("instruction is of sb format(branch)")
        control=0
        if(fun3(inst)==0x0):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            imme=sign_extend(imm12,12)*2
            print("beq rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            controlCount = controlCount + 1
            return "beq"
        elif(fun3(inst)==0x1):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            imme=sign_extend(imm12,12)*2
            print("bne rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            controlCount = controlCount + 1
            return "bne"
        elif(fun3(inst)==0x4):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            imme=sign_extend(imm12,12)*2
            print("blt rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            controlCount = controlCount + 1
            return "blt"
        elif(fun3(inst)==0x5):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            decodeRA=register[rs1]
            decodeRB=register[rs2]
            imme=sign_extend(imm12,12)*2
            print("bge rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
            print("values in pipeline buffers decodeRA:",decodeRA,"decodeRB:",decodeRB)
            controlCount = controlCount + 1
            return "bge"

    elif(opc(inst)==0x17):   # u format
        print("instruction is of u format")
        control=1
        rd=r_d(inst)
        imm20=imm_20(inst) #imm[31:12] 20 bits
        imme=sign_extend(imm20,20)
        decodeRD=rd
        if(instcount==1):
            datadependence[0]=rd
        elif(instcount==2):
            datadependence[1]=rd
        elif(instcount>=3):
            datadependence[2]=rd
        print("auipc rd:",rd,"imm:",imme)
        aluCount = aluCount + 1
        return "auipc"
    elif(opc(inst)==0x37):
        print("instruction is of u format")
        rd=r_d(inst)
        imm20=imm_20(inst) #imm[19:0] 20 bits
        imme=sign_extend(imm20,20)
        decodeRD=rd
        if(instcount==1):
            datadependence[0]=rd
        elif(instcount==2):
            datadependence[1]=rd
        elif(instcount>=3):
            datadependence[2]=rd
        print("lui rd:",rd,"imm:",imme)
        controlCount = controlCount + 1
        return "lui"

    elif(opc(inst)==0x6f):  # uj format
        print("instruction is of uj format")
        control=1
        rd=r_d(inst)
        imm19=(inst>>12)&0xff   # imm[19:12] 8 bits
        imm11=(inst>>20)&0x1    # imm[11] 1 bit
        imm10=(inst>>21)&0x3ff  # imm[10:1] 10 bits
        imm20=(inst>>31)&0x1    # imm[20] 1 bit
        imm11=(imm11<<10)|imm10 # imm[11:1] 11 bits
        imm19=(imm19<<11)|imm11 # imm[19:1] 19 bits
        imm20=(imm20<<19)|imm19 # imm[20:1] 20 bits
        imme=sign_extend(imm20,20)*2
        decodeRD=rd
        if(instcount==1):
            datadependence[0]=rd
        elif(instcount==2):
            datadependence[1]=rd
        elif(instcount>=3):
            datadependence[2]=rd
        print("jal rd:",rd,"imm[20:0]:",imme)
        controlCount = controlCount + 1
        return "jal"


def dependenceChecker(operation):
	global dataDependence, stallCount, stallDataHazard
	
	if(rs1 == datadependence[0]):
		dataDependence[0] = 'H1'
		if (knobDataFor == 'off'):
			if operation in loadInst:
				stallCount = stallCount + 2
				stallDataHazard = stallDataHazard + 2
			elif operation in StoreInst:
				stallCount = stallCount + 2
				stallDataHazard = stallDataHazard + 2
			else:
				stallCount = stallCount + 1
				stallDataHazard = stallDataHazard + 1
	elif(rs1 == datadependence[1]):
		dataDependence[0] = 'H2'
		if (knobDataFor == 'off'):
			if operation in loadInst:
				stallCount = stallCount + 3
				stallDataHazard = stallDataHazard + 3
			elif operation in StoreInst:
				stallCount = stallCount + 3
				stallDataHazard = stallDataHazard + 3
			else:
				stallCount = stallCount + 2
				stallDataHazard = stallDataHazard + 2
	else:
		dataDependence[0] = 'none'
	
	if(rs2 == datadependence[0]):
		dataDependence[1] = 'H1'
		if (knobDataFor == 'off'):
			if operation in loadInst:
				stallCount = stallCount + 2
				stallDataHazard = stallDataHazard + 2
			elif operation in StoreInst:
				stallCount = stallCount + 2
				stallDataHazard = stallDataHazard + 2
			else:
				stallCount = stallCount + 1
				stallDataHazard = stallDataHazard + 1
	elif(rs2 == datadependence[1]):
		dataDependence[1] = 'H2'
		if (knobDataFor == 'off'):
			if operation in loadInst:
				stallCount = stallCount + 3
				stallDataHazard = stallDataHazard + 3
			elif operation in StoreInst:
				stallCount = stallCount + 3
				stallDataHazard = stallDataHazard + 3
			else:
				stallCount = stallCount + 2
				stallDataHazard = stallDataHazard + 2
	else:
		dataDependence[1] = 'none'

#Assuming MuxB, RA, RB, IR, RZ, PC, PC_temp, imme are global variables.

#Output of alu will be in register(global variable) RZ

#Global variables (Same as diagram)
#RA RB RZ PC PC_temp MuxB imme
#IR RD RY
# ----------------------------------------

# PHASE 2 EXTENSION
# ----------------------------------------
# If PIPELINE is on in main(), call pipelineAlu()
# Else call alu()
# multiClock -> variable for clock in pipeline
# Buffer variables

#Data dependence History table->
#Stores the register address of last two instruction

#checks for data dependece on current instruction with last 2
#and gives the list dataDependence
#dataDependence[0] = H1		if RA dependent on 2nd last instruction
#dataDependence[1] = H1		if RB dependent on 2nd last instruction
#if dependence with 2nd last instruction
# Here Memory to Alu data forwarding

#dataDependence[0] = H2		
#dataDependence[1] = H2
#if data dependence with last instruction
#Here ALU to ALU data forwarding path

#dataDependence =  {"none", "none"} if no data dependence

#Decode Buffer registers -> stores current decode values ->
#decodeRA, decodeRB, decodeRD 

#ALU Buffer registers -> stores current register values after ALU operation -> aluRZ

#Alu Data forwarding registers -> aludfRZ
#Memory data forwarding register -> memdfRZ

#-----------------------------------------

def alu(operation):
	global RZ, pc, pc_temp
	
	print("ALU")
	print("OPERATION Preforming : ", operation)
	
	if operation == "add":
		RZ = RA + RB
		print("RZ = sum : ", RZ)
		
	elif operation == "addi":
		RZ = RA + imme
		print("RZ = sum : ", RZ)
		
	elif operation == "sub":
		RZ = RA - RB
		print("RZ = diff : ", RZ)
		
	elif operation == "mul":
		RZ = RA * RB
		print("RZ = product : ", RZ)
		
	elif operation == "div":
		RZ = int(RA / RB)
		print("RZ = quotient : ", RZ)
		
	elif operation == "rem":
		RZ = RA % RB
		print("RZ = remainder : ", RZ)
		
	elif operation == "xor":
		RZ = RA ^ RB
		print("RZ = xor : ", RZ)
		
	elif operation == "and":
		RZ = RA & RB
		print("RZ = and : ", RZ)
		
	elif operation == "andi":
		RZ = RA & imme
		print("RZ = and : ", RZ)
		
	elif operation == "or":
		RZ = RA | RB
		print("RZ = or : ", RZ)
		
	elif operation == "ori":
		RZ = RA | imme
		print("RZ = or : ", RZ)
		
	elif operation == "sll":
		RZ = BitArray(int = RA, length = 32) << RB		#Restricting size to 32 bits
		RZ = RZ.int 	#Converting back to int
		print("RZ = lshift L : ", RZ)
		
	elif operation == "srl":
		RZ = BitArray(int = RA, length = 32) >> RB
		RZ = RZ.int
		print("RZ = rshift L : ", RZ)
		
	elif operation == "sra":
		RZ = RA >> RB
		print("RZ = rshift A : ", RZ)
		
	elif operation == "slt":
		if RA < RB:
			RZ = 1
		else:
			RZ = 0
		print("RZ = slt : ", RZ)
		
	elif operation == "beq":
		if RA == RB:
			RZ = (pc - 4) + imme*2
			pc = RZ
		else:
			RZ = pc
		print("RZ = Target address : ", RZ)
		
	elif operation == "bne":
		if RA != RB:
			RZ = (pc - 4) + imme*2
			pc = RZ
		else:
			RZ = pc
		print("RZ = target address : ", RZ)
		
	elif operation == "bge":
		if RA >= RB:
			RZ = (pc - 4) + imme*2
			pc = RZ
		else:
			RZ = pc
		print("RZ = target address : ", RZ)
		
	elif operation == "blt":
		if RA < RB:
			RZ = (pc - 4) + imme*2
			pc = RZ
		else:
			RZ = pc
		print("RZ = target address : ", RZ)
		
	elif operation == "auipc":
		RZ = (pc - 4) + (imme << 12)
		print("RZ = target address : ", RZ)
		
	elif operation == "jal":
		RZ = (pc - 4) + imme*2
		pc_temp = pc
		pc = RZ
		print("RZ = target address : ", RZ)
		
	elif operation == "jalr":
		RZ = RA + imme
		pc_temp = pc
		pc = RZ
		print("RZ = target address : ", RZ)
		
	elif operation == "lui":
		RZ = BitArray(int = imme, length = 32) << 12
		RZ = RZ.int
		print("RZ = integer : ", RZ)
		
	elif operation == "sb":
		RZ = RB + imme
		print("RZ = target address : ", RZ)
		
	elif operation == "sw":
		RZ = RB + imme
		print("RZ = target address : ", RZ)
		
	elif operation == "sd":
		RZ = RB + imme
		print("RZ = target address : ", RZ)
		
	elif operation == "sh":
		RZ = RB + imme
		print("RZ = target address : ", RZ)
		
	elif operation == "lb":
		RZ = RA + imme
		print("RZ = target address : ", RZ)
		
	elif operation == "ld":
		RZ = RA + imme
		print("RZ = target address : ", RZ)
		
	elif operation == "lh":
		RZ = RA + imme
		print("RZ = target address : ", RZ)
	elif operation == "lw":
		RZ = RA + imme
		print("RZ = target address : ", RZ)


#Data dependence History table->
#Stores the register address of last two instruction

#checks for data dependece on current instruction with last 2
#and gives the list dataDependence
#dataDependence[0] = H1		if RA dependent on 2nd last instruction
#dataDependence[1] = H1		if RB dependent on 2nd last instruction
#if dependence with 2nd last instruction
# Here Memory to Alu data forwarding

#dataDependence[0] = H2		
#dataDependence[1] = H2
#if data dependence with last instruction
#Here ALU to ALU data forwarding path

#dataDependence =  {"none", "none"} if no data dependence

#Decode Buffer registers -> stores current decode values ->
#decodeRA, decodeRB, decodeRD 

#ALU Buffer registers -> stores current register values after ALU operation -> aluRZ

#Alu Data forwarding registers -> aludfRZ
#Memory data forwarding register -> memdfRZ

def pipelineAlu(operation):
    global RZ, pc, pc_temp, aluRZ, aludfRZ, multiClock, RA, RB
	
    dependenceChecker(operation)
	
    #Mem to ALU data forwarding
    if dataDependence[0] == 'H1':
        RA = memdfRZ	
    #ALU to AlU data forwarding
    elif dataDependence[0] == 'H2':
        RA = aludfRZ	
    #No data dependence
    elif dataDependence[0] == 'none':
        RA = decodeRA
	
    #Similarly for RB	
    if dataDependence[1] == 'H1':
        RB = memdfRZ
    elif dataDependence[1] == 'H2':
        RB = aludfRZ
    elif dataDependence[1] == 'none':
        RB = decodeRB
	
    print("ALU")
    print("OPERATION Preforming : ", operation)
	
    if operation == "add":
        RZ = RA + RB
        print("RZ = sum : ", RZ)
		
    elif operation == "addi":
        RZ = RA + imme
        print("RZ = sum : ", RZ)
		
    elif operation == "sub":
        RZ = RA - RB
        print("RZ = diff : ", RZ)
		
    elif operation == "mul":
        RZ = RA * RB
        print("RZ = product : ", RZ)
		
    elif operation == "div":
        RZ = int(RA / RB)
        print("RZ = quotient : ", RZ)
		
    elif operation == "rem":
        RZ = RA % RB
        print("RZ = remainder : ", RZ)
		
    elif operation == "xor":
        RZ = RA ^ RB
        print("RZ = xor : ", RZ)
		
    elif operation == "and":
        RZ = RA & RB
        print("RZ = and : ", RZ)
		
    elif operation == "andi":
        RZ = RA & imme
        print("RZ = and : ", RZ)
		
    elif operation == "or":
        RZ = RA | RB
        print("RZ = or : ", RZ)
		
    elif operation == "ori":
        RZ = RA | imme
        print("RZ = or : ", RZ)
		
    elif operation == "sll":
        RZ = BitArray(int = RA, length = 32) << RB		#Restricting size to 32 bits
        RZ = RZ.int 	#Converting back to int
        print("RZ = lshift L : ", RZ)
		
    elif operation == "srl":
        RZ = BitArray(int = RA, length = 32) >> RB
        RZ = RZ.int
        print("RZ = rshift L : ", RZ)
		
    elif operation == "sra":
        RZ = RA >> RB
        print("RZ = rshift A : ", RZ)
		
    elif operation == "slt":
        if RA < RB:
            RZ = 1
        else:
            RZ = 0
        print("RZ = slt : ", RZ)
		
    elif operation == "beq":
        if RA == RB:
            RZ = (pc - 8) + imme*2	#pipeline
            pc = RZ
        else:
            RZ = pc
        print("RZ = Target address : ", RZ)
		
    elif operation == "bne":
        if RA != RB:
            RZ = (pc - 8) + imme*2	#pipeline
            pc = RZ
        else:
            RZ = pc
        print("RZ = target address : ", RZ)
		
    elif operation == "bge":
        if RA >= RB:
            RZ = (pc - 8) + imme*2	#pipeline
            pc = RZ
        else:
            RZ = pc
        print("RZ = target address : ", RZ)
		
    elif operation == "blt":
        if RA < RB:
            RZ = (pc - 8) + imme*2	#pipeline
            pc = RZ
        else:
            RZ = pc
        print("RZ = target address : ", RZ)
		
    elif operation == "auipc":
        RZ = (pc - 8) + (imme << 12)	#pipeline
        print("RZ = target address : ", RZ)
		
    elif operation == "jal":
        RZ = (pc - 8) + imme*2		#pipelne
        pc_temp = pc
        pc = RZ
        print("RZ = target address : ", RZ)
		
    elif operation == "jalr":
        RZ = RA + imme
        pc_temp = pc
        pc = RZ
        print("RZ = target address : ", RZ)
		
    elif operation == "lui":
        RZ = BitArray(int = imme, length = 32) << 12
        RZ = RZ.int
        print("RZ = integer : ", RZ)
		
    elif operation == "sb":
        RZ = RB + imme
        print("RZ = target address : ", RZ)
		
    elif operation == "sw":
        RZ = RB + imme
        print("RZ = target address : ", RZ)
		
    elif operation == "sd":
        RZ = RB + imme
        print("RZ = target address : ", RZ)
		
    elif operation == "sh":
        RZ = RB + imme
        print("RZ = target address : ", RZ)
		
    elif operation == "lb":
        RZ = RA + imme
        print("RZ = target address : ", RZ)
		
    elif operation == "ld":
        RZ = RA + imme
        print("RZ = target address : ", RZ)
		
    elif operation == "lh":
        RZ = RA + imme
        print("RZ = target address : ", RZ)
    elif operation == "lw":
        RZ = RA + imme
        print("RZ = target address : ", RZ)
		
    #Updating the ALU data forwarding registers
    aludfRZ = RZ
	
    #updating the alu output
    aluRZ = RZ
	
    #Updating the Clock value
    multiClock = multiClock + 1
    print("Multiclock: ", multiClock)
	


def initMemory():
    global TextMemory, DataMemory
    file = open("instruction.mc","r")
    lines =file.readlines()
    if (lines):
        for i in range(len(lines)):
            if lines[i]!='\n':
                array = []
                array.append(lines[i].split())

                if(int(array[0][0], 16) >= 0x10000000):
                    DataMemory[int(array[0][0], 16)] = int(array[0][1], 16)
                else:
                    TextMemory[int(array[0][0], 16)] = int(array[0][1], 16)
					
    file.close()
	
######################## EDING ######

def Data_cache(address):        # Address will come from ALU
    global bo_bits, index_bits, tag_bits, data_copy, cachesize, blocksize, n, SA
    data_copy = address

    # instruction address sent from BTB or IAG
    # number of bits in instruction adddress

    add_bits=32                           # 32 for risc-v 32 bit ISA
    bo_bits=int(math.log2(blocksize))     # number of bits in block offset
    index_bits=int(math.log2(numsets))    # number of bits in index
    tag_bits=add_bits-bo_bits-index_bits  # number of bits in tag

def UpdateSAData():
    global SA, ind, DataMemory, TextMemory, DataNumHits, DataNumMisses
    predict = ""
    for way in SA:
        for index in range(len(SA[way])):
            if index == ind:
                if SA[way][index][0] == tag:
                    predict = "hit"
                    DataNumHits += 1
                    return SA[way][index][1]
                else:
                    predict = "miss"
                    DataNumMisses += 1
                    SA[way][index][0] = tag
                    if 0x0FFFFFE8<=address:
                        SA[way][index][1] = DataMemory[address]
                    else:
                        SA[way][index][1] = TextMemory[address]

def pipelineMemory_access(operation, lines):
	global DataMemory, RY, multiClock
	multiClock = multiClock + 1
    
	if operation in loadInst:
		RY = DataMemory[aluRZ]
		memRY = RY
	elif operation in StoreInst:
		DataMemory[aluRZ] = RA
	else:
		RY = RZ
		memRY = RY
		
	memdfRZ = RY
		 
	
def Memory_access(operation, lines):
    global DataMemory, RY
    
    if operation in loadInst:
        RY = DataMemory[aluRZ]
    elif operation in StoreInst:
        DataMemory[aluRZ] = RA
    print("DataMemory: ", DataMemory)

#########################################################

def WriteBack():
    global register, multiClock
    if(knobPipeline == 'on'):
        multiClock = multiClock + 1
    if (Control==1):  
        register[rd] = RY
    print("Registers: ", register)

def Pipeline():
    global clock, Control, cap
    global memory
    file = open("instruction.mc","r")
    lines =file.readlines()
    n = len(lines)
    IR = pipelineFetch(lines)
    lines = lines[1:]

    IR = int(IR, 16)
    Operation = pipelinedecode(IR); IR = pipelineFetch(lines)

    pipelineAlu(Operation); Operation = pipelinedecode(int(IR, 16)); IR = pipelineFetch(lines)

    if IR!='':
        pipelineMemory_access(Operation, Operation); pipelineAlu(Operation); Operation = pipelinedecode(int(IR, 16)); IR = pipelineFetch(lines)
    else:
        pipelineMemory_access(Operation, Operation); pipelineAlu(Operation); Operation = pipelinedecode(IR); IR = pipelineFetch(lines)
    for i in range(n):
        if IR!='':
            WriteBack(); pipelineMemory_access(Operation, Operation); pipelineAlu(Operation); Operation = pipelinedecode(int(IR, 16)); IR = pipelineFetch(lines)
        else:
            WriteBack(); pipelineMemory_access(Operation, Operation); pipelineAlu(Operation); Operation = pipelinedecode(IR); IR = pipelineFetch(lines)

def CachePipeline():
    global clock, Control, cap
    global memory
    file = open("instruction.mc","r")
    lines =file.readlines()
    n = len(lines)
    IR = inst_fetch(lines); IR = UpdateSAInst(lines)
    lines = lines[1:]

    IR = int(IR, 16)
    Operation = pipelinedecode(IR); inst_fetch(lines); IR = UpdateSAInst(lines)

    pipelineAlu(Operation); Operation = pipelinedecode(int(IR, 16)); inst_fetch(lines); IR = UpdateSAInst(lines)

    if IR!='':
        Data_cache(RY); UpdateSAData(); pipelineAlu(Operation); Operation = pipelinedecode(int(IR, 16)); inst_fetch(lines); IR = UpdateSAInst(lines)
    else:
        Data_cache(RY); UpdateSAData(); pipelineAlu(Operation); Operation = pipelinedecode(IR); inst_fetch(lines); IR = UpdateSAInst(lines)
    for i in range(n):
        if IR!='':
            WriteBack(); Data_cache(RY); UpdateSAData(); pipelineAlu(Operation); Operation = pipelinedecode(int(IR, 16)); inst_fetch(lines); IR = UpdateSAInst(lines)
        else:
            WriteBack(); Data_cache(RY); UpdateSAData(); pipelineAlu(Operation); Operation = pipelinedecode(IR); inst_fetch(lines); IR = UpdateSAInst(lines)
            
    file.close()


def nonPipeline():
    global clock, Control,cap
    global memory
    #cap=initialize(cap, memory)
    file = open("instruction.mc","r")
    lines =file.readlines()
    IR = Fetch(lines)
    while IR != '':
        print ("INSTRUCTION : ", IR)
        IR = int(IR, 16)
        operation = decode(IR)
        Control = 0
        if operation in ['add', 'and', 'or', 'sll', 'slt', 'sra', 'srl', 'sub', 'xor', 'mul', 'div', 'rem', 'addi', 'andi', 'ori', 'lb', 'ld', 'lh', 'lw', 'lui', 'auipc']:
            Control = 1
		
        alu(operation)
        Memory_access(operation, lines)
        WriteBack()
        IR = Fetch(lines)
        print("IR = ", IR)
        clock = clock + 1
        print()
        
    file.close()



def main():
    initMemory()
    global knobPipeline, knobDataFor, knobRegister, knobPipelineRegister, knobSpecial, specialInst, multiClock, instcount
    knobPipeline = input('Enter "on/off" to Enable/Disable Pipeline : ')
    knobPipeline.lower()
    knobRegister = input('Enter "on/off" to Enable/Disable Printing registers in Cycle : ')
    knobRegister.lower()
    if (knobPipeline == 'on'):
        knobDataFor = input('Enter "on/off" to Enable/Disable Data Forwarding : ')
        knobDataFor.lower()
        knobPipelineRegister = input('Enter "on/off" to Enable/Disable Printing Pipeline registers in Cycle : ')
        knobPipelineRegister.lower()
        knobSpecial = input('Enter "on/off" to Enable/Disable Printing Pipeline registers in Specific Instruction : ')
        knobSpecial.lower()
        if(knobSpecial == 'on'):
            specialInst = int(input('Enter the Instruction number (in decimal base) : '))
        CachePipeline()
        
        print('Total Cycles : ', multiClock)
        print('Total Instructions : ', instcount)
        print('CPI : ', multiClock//instcount)
        print('No. of Data Transfer : ', dataTransferCount)
        print('No. of ALU Instructions : ', aluCount)
        print('No. of Control Instructions : ', controlCount)
        print('Stall Count : ', stallCount)
        print('No. of data Hazards : ', dataHazard)
        print('No. of control Hazards : ', controlHazard)
        print('No. of branch mispredictions : ', branchMispridiction)
        print('No. of data Hazard stall : ', stallDataHazard)
        print('No. of control Hazard stall : ', stallControlHazard)

        print("\n")
        print("\nData Cache: ")
        print("Number of accesess:_____ ", InsNUmMisses+InsNumHits)
        print("Number of Hits:_____ ", InsNumHits)
        print("Number of misses:_____ ", InsNUmMisses)
        print("\n")

        print("\nData Cache: ")
        print("Number of accesess:_____ ", DataNumMisses+DataNumHits)
        print("Number of Hits:_____ ", DataNumHits)
        print("Number of misses:_____ ", DataNumMisses)
        print("\n")

    elif(knobPipeline == 'off'):
        nonPipeline()
        print('Total Cycles : ', clock )
        print('Total Instructions : ', instcount)
        print('CPI : ', clock//instcount)
        print('No. of Data Transfer : ', dataTransferCount)
        print('No. of ALU Instructions : ', aluCount)
        print('No. of Control Instructions : ', controlCount)
    else:
        print("Enter only on/off")
        main()

		

if __name__ == '__main__':
	main()
