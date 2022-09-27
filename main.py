#code by Nema Ram Meghwal
#open file in reading mode
#global pc
#global variable IR
#local variable array
#local variable MCode
#function Fetch  
#store instruction in IR
from bitstring import BitArray

IR = ''
pc = 0x0
pc_temp = 0x0
rd = 0x0
RA = 0x0
RB = 0x0
RZ = 0x0
RY = 0x0
imme = 0x0
clock = 0
Control = 0
register = [] # global list 
memory=[]
cap=-1
for i in range(32):
    register.append(0)

register[2] = 0x7FFFFFF0 	#Stack Pointer
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


# code by ashish sulania
# assuming RA,RB,rd and imme as global variable and register as a global list 
# RA=register[rs1],RB=register[rs2]
# decode function returns mnemonic of instruction and update global variables RA,RB,rd,imme 

def opc(inst):    # returns opcode
    return (inst&0x7f)

def fun3(inst):   # returns fun3
    return ((inst >> 12)&0x7)

def fun_7(inst):  # returns fun7
    return ((inst>>25)&0x7f)

def r_d(inst):    # returns rd
    return ((inst>>7)&0x1f)

def rs_1(inst):   # returns rs1
    return ((inst>>15)&0x1f)

def rs_2(inst):   # returns rs2
    return ((inst>>20)&0x1f)

def imm_12(inst): # returns imm12 of i format
    return ((inst>>20)&0xfff)

def imm_20(inst): # returns imm20 of u format
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
    global RA,RB,imme,rd,control
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
            return "add"
        elif(fun3(inst)==0x0 and fun_7(inst)==0x20):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("sub","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "sub"
        elif(fun3(inst)==0x7 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("and","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "and"
        elif(fun3(inst)==0x6 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("or","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "or"
        elif(fun3(inst)==0x1 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("sll","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "sll"
        elif(fun3(inst)==0x2 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            print("slt","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "slt"
        elif(fun3(inst)==0x5 and fun_7(inst)==0x20):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("sra","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "sra"
        elif(fun3(inst)==0x5 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            print("srl","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "srl"
        elif(fun3(inst)==0x4 and fun_7(inst)==0x00):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("xor","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "xor"
        elif(fun3(inst)==0x0 and fun_7(inst)==0x01):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("mul","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "mul"
        elif(fun3(inst)==0x4 and fun_7(inst)==0x01):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("div","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "div"
        elif(fun3(inst)==0x6 and fun_7(inst)==0x01):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            rd=r_d(inst)
            RA=register[rs1]
            RB=register[rs2]
            print("rem","rs1:",rs1,"rs2:",rs2,"rd:",rd)
            print("values [rs1]:",RA,"[rs2]:",RB)
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
            return "addi"
        elif(fun3(inst)==0x7):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            RA=register[rs1]
            imme=sign_extend(imm12,12)
            print("andi rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value [rs1]:",RA)
            return "andi"
        elif(fun3(inst)==0x6):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            RA=register[rs1]
            imme=sign_extend(imm12,12)
            print("ori rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value [rs1]:",RA)
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
            return "lb"
        elif(fun3(inst)==0x1):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            RA=register[rs1]
            imme=sign_extend(imm12,12)
            print("lh rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value [rs1]:",RA)
            return "lh"
        elif(fun3(inst)==0x2):
            rs1=rs_1(inst)
            rd=r_d(inst)
            imm12=imm_12(inst)
            RA=register[rs1]
            imme=sign_extend(imm12,12)
            print("lw rs1:",rs1,"rd:",rd,"imm:",imme)
            print("value [rs1]:",RA)
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
            imme=sign_extend(imm12,12)
            print("beq rs1:",rs1,"rs2:",rs2,"imm[12:1]:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "beq"
        elif(fun3(inst)==0x1):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            RA=register[rs1]
            RB=register[rs2]
            imme=sign_extend(imm12,12)
            print("bne rs1:",rs1,"rs2:",rs2,"imm[12:1]:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "bne"
        elif(fun3(inst)==0x4):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            RA=register[rs1]
            RB=register[rs2]
            imme=sign_extend(imm12,12)
            print("blt rs1:",rs1,"rs2:",rs2,"imm[12:1]:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "blt"
        elif(fun3(inst)==0x5):
            rs1=rs_1(inst)
            rs2=rs_2(inst)
            imm5=r_d(inst) # imm[4:1]imm[11] 5 bits
            imm7=fun_7(inst) #imm[12]imm[10:5] 7 bits
            imm12=calsb(imm7,imm5)
            RA=register[rs1]
            RB=register[rs2]
            imme=sign_extend(imm12,12)
            print("bge rs1:",rs1,"rs2:",rs2,"imm[12:1]:",imme)
            print("values [rs1]:",RA,"[rs2]:",RB)
            return "bge"

    elif(opc(inst)==0x17):   # u format
        print("instruction is of u format")
        control=1
        rd=r_d(inst)
        imm20=imm_20(inst) #imm[31:12] 20 bits
        imme=sign_extend(imm20,20)
        print("auipc rd:",rd,"imm:",imme)
        return "auipc"
    elif(opc(inst)==0x37):
        print("instruction is of u format")
        rd=r_d(inst)
        imm20=imm_20(inst) #imm[19:0] 20 bits
        imme=sign_extend(imm20,20)
        print("lui rd:",rd,"imm:",imme)
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
        imme=sign_extend(imm20,20)
        print("jal rd:",rd,"imm[20:1]:",imme)
        return "jal"

#Code by Vicky Kumar Xaxa
#Assuming MuxB, RA, RB, IR, RZ, PC, PC_temp, imme are global variables.
#decode fills MuxB, RA, RB, imme
#MuxB = 0 for value from RB to ALU. MuxB = 1 for imme to ALU
#Decodes outputs the name (string, lowercase) of instruction in variable operation:-
#add, and, or, sll, slt, sra, srl, sub, xor, mul, div, rem
#addi, andi, ori, lb, ld, lh, lw, jalr
#sb, sw, sd, sh
#beq, bne, bge, blt
#auipc, lui
#jal

#Output of alu will be in register(global variable) RZ

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
		RZ = RA + imme
		print("RZ = target address : ", RZ)
		
	elif operation == "sw":
		RZ = RA + imme
		print("RZ = target address : ", RZ)
		
	elif operation == "sd":
		RZ = RA + imme
		print("RZ = target address : ", RZ)
		
	elif operation == "sh":
		RZ = RA + imme
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

"""
Code By Samir P Salim
Assumptions:
cap, memory[],registers[],operation,RZ are global variables.
"""

def eight_digit(a): #converting a less than 8 digit hexadecimal number to a 8 digit hexadecimal number
    if(len(a)<10):
        b=len(a)
        ans=[]
        ans.append(a[0])
        ans.append(a[1])
        for i in range(10-b):
            ans.append('0')
        for i in range(b-2):
            ans.append(a[i+2])
        return(ans)
    else:
        return a
    
def print_reg(register): #function to print all registers
    for i in range(32):
        a=eight_digit(hex(register(i)))
        print("x"+str(i)+" "+a[0]+a[1]+a[2]+a[3]+a[4]+a[5]+a[6]+a[7]+a[8]+a[9])

def print_mem(memory,cap): #function to print all components of memory
    i=0
    while(cap>=i):
        if(cap-i>=3):
            a=hex(memory[i])
            b=hex(memory[i+1])
            c=hex(memory[i+2])
            d=hex(memory[i+3])
            print(hex(i+0x10000000)+" 0x"+a[2:]+b[2:]+c[2:]+d[2:])
        elif(cap-i>=2):
           a=hex(memory[i])
           b=hex(memory[i+1])
           c=hex(memory[i+2]) 
           print(hex(i+0x10000000)+" 0x00"+a[2:]+b[2:]+c[2:])
        elif(cap-i>=1):
           a=hex(memory[i])
           b=hex(memory[i+1])
           print(hex(i+0x10000000)+" 0x0000"+a[2:]+b[2:])
        elif(cap-i>=0):
           a=hex(memory[i])
           print(hex(i+0x10000000)+" 0x000000"+a[2:])
        i+=4
    

def convert(a,b): #function to convert a two digit hexadecimal number 0x<a><b> to decimal number
    ans=0
    if(a=='0'):
        ans+=0
    elif(a=='1'):
        ans+=1
    elif(a=='2'):
        ans+=2
    elif(a=='3'):
        ans+=3
    elif(a=='4'):
        ans+=4
    elif(a=='5'):
        ans+=5
    elif(a=='6'):
        ans+=6
    elif(a=='7'):
        ans+=7
    elif(a=='8'):
        ans+=8
    elif(a=='9'):
        ans+=2
    elif(a=='A'):
        ans+=10
    elif(a=='B'):
        ans+=11
    elif(a=='C'):
        ans+=12
    elif(a=='D'):
        ans+=13
    elif(a=='E'):
        ans+=14
    elif(a=='F'):
        ans+=15
    ans*=16
    if(b=='0'):
        ans+=0
    elif(b=='1'):
        ans+=1
    elif(b=='2'):
        ans+=2
    elif(b=='3'):
        ans+=3
    elif(b=='4'):
        ans+=4
    elif(b=='5'):
        ans+=5
    elif(b=='6'):
        ans+=6
    elif(b=='7'):
        ans+=7
    elif(b=='8'):
        ans+=8
    elif(b=='9'):
        ans+=2
    elif(b=='A'):
        ans+=10
    elif(b=='B'):
        ans+=11
    elif(b=='C'):
        ans+=12
    elif(b=='D'):
        ans+=13
    elif(b=='E'):
        ans+=14
    elif(b=='F'):
        ans+=15
    return ans

def initialize(cap, memory): #function to initialize memory in the form of an array which store two digit hexadecimal numbers
    file1=open("instruction.mc","r")
    lines1=file1.readlines()
    array = []
    for i in lines1:
        array.append(i.split())
    for i in array:
        if(len(i[0])==10):
            if(len(i[1])>9):
                memory.append(convert(i[1][8],i[1][9]))
                cap+=1
            elif(len(i[1])<10 and len(i[1])>8):
                memory.append(convert(i[1][8],'0'))
                cap+=1
            if(len(i[1])>7):
                memory.append(convert(i[1][6],i[1][7]))
                cap+=1
            elif(len(i[1])<8 and len(i[1])>6):
                memory.append(convert(i[1][6],'0'))
                cap+=1
            if(len(i[1])>5):
                memory.append(convert(i[1][4],i[1][5]))
                cap+=1
            elif(len(i[1])<6 and len(i[1])>4):
                memory.append(convert(i[1][4],'0'))
                cap+=1
            if(len(i[1])>3):
                memory.append(convert(i[1][2],i[1][3]))
                cap+=1
            elif(len(i[1])<4 and len(i[1])>2):
                memory.append(convert(i[1][2],'0'))
                cap+=1
    return cap

def access_memory(operation):
    global memory
    global cap
    if(operation=="lb"):
        marker=RZ-0x10000000
        if(marker<=cap):
            if(memory[marker]<128):
                return memory[marker]
            else:
                return (memory[marker]+0xffffff00)%4294967296
        else:
            return 0
    elif(operation=="lh"):
        marker=RZ-0x10000000
        if(marker+1<=cap):
            p=memory[marker]+256*memory[marker+1]
            if(p<32768):
                return p
            else:
                return (p+0xffffffff)%4294967296
        elif(marker==cap):
            p=memory[marker]
            return (p+0xffffffff)%4294967296
        else:
            return 0
    elif(operation=="lw"):
        marker=RZ-0x10000000
        if(marker+3<=cap):
            p=memory[marker]+256*memory[marker+1]+256*256*memory[marker+2]+256*256*256*memory[marker+3]
            return (p+0xffffffff)%4294967296
        elif(marker+2==cap):
            p=memory[marker]+256*memory[marker+1]+256*256*memory[marker+2]
            return p
        elif(marker+1==cap):
            p=memory[marker]+256*memory[marker+1]
            return p
        elif(marker==cap):
            p=memory[marker]
            return p
        else:
            return 0
    elif (operation=="sw"):
        marker=RZ-0x10000000
        if(marker+3<=cap):
            memory[marker]=RB%256
            memory[marker+1]=(RB//256)%256
            memory[marker+2]=(RB//(256*256))%256
            memory[marker+3]=(RB//(256*256*256))%256
        elif(marker+2==cap):
            memory[marker]=RB%256
            memory[marker+1]=(RB//256)%256
            memory[marker+2]=(RB//(256*256))%256
            memory.append((RB//(256*256*256))%256)
            cap+=1
        elif(marker+1==cap):
            memory[marker]=RB%256
            memory[marker+1]=(RB//256)%256
            memory.append((RB//(256*256))%256)
            memory.append((RB//(256*256*256))%256)
            cap+=2
        elif(marker==cap):
            memory[marker]=RB%256
            memory.append((RB//256)%256)
            memory.append((RB//(256*256))%256)
            memory.append((RB//(256*256*256))%256)
            cap+=3
        elif(marker-1==cap):
            memory.append(RB%256)
            memory.append((RB//256)%256)
            memory.append((RB//(256*256))%256)
            memory.append((RB//(256*256*256))%256)
            cap+=4
        else:
            while(cap<marker):
                memory.append(0)
                cap+=1
            memory.append(RB%256)
            memory.append((RB//256)%256)
            memory.append((RB//(256*256))%256)
            memory.append((RB//(256*256*256))%256)
            cap+=3
    elif (operation=="sh"):
        marker=RZ-0x10000000
        if(marker+1<=cap):
            memory[marker]=RB%256
            memory[marker+1]=(RB//256)%256
        elif(marker==cap):
            memory[marker]=RB%256
            memory.append((RB//256)%256)
            cap+=1
        elif(marker-1==cap):
            memory.append(RB%256)
            memory.append((RB//256)%256)
            cap+=2
        else:
            while(cap<marker):
                memory.append(0)
                cap+=1
            memory.append(RB%256)
            memory.append((RB//256)%256)
            cap+=1
    elif (operation=="sb"):
        marker=RZ-0x10000000
        if(marker<=cap):
            memory[marker]=RB%256
        elif(marker-1==cap):
            memory.append(RB%256)
            cap+=1
        else:
            while(cap<marker):
                memory.append(0)
                cap+=1
            memory.append(RB%256)
    return RY
# Code by Sahdev
# rd : global variable ; detected in decode stage
# RY is output of stage 4.
            # control : initalised with 0 #####
# 	is a global variable : it should come from decode stage.
#  	it will detect the type of instructon
# 	control will become 1 for r-type, i-type, u-type, uj-type


def WriteBack():	
	if(Control==1):
		RY = RZ
		register[rd] = RY


def main():
	global clock, Control,cap
	global memory
	cap=initialize(cap, memory)
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
		access_memory(operation)
		print_mem(memory,cap)
		WriteBack()
		IR = Fetch(lines)
		clock = clock + 1
		print()
		
	print("CLOCK : ", clock)
	file.close()
	
	
	
if __name__ == '__main__':
	main()
































