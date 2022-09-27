# code by ashish sulania
# assuming RA,RB,rd and imme as global variable and register as a global list 
# RA=register[rs1],RB=register[rs2]
# decode function returns mnemonic of instruction and update global variables RA,RB,rd,imme 
# call decode() function for non pipeline implementation and for pipeline implementation call pipelinedecode() function

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
            RA=register[rs1]
            RB=register[rs2]
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
            RA=register[rs1]
            RB=register[rs2]
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
            imme=sign_extend(imm12,12)*2
            print("beq rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
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
            imme=sign_extend(imm12,12)*2
            print("bne rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
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
            imme=sign_extend(imm12,12)*2
            print("blt rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
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
            imme=sign_extend(imm12,12)*2
            print("bge rs1:",rs1,"rs2:",rs2,"imm[12:0]:",imme)
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
        imme=sign_extend(imm20,20)*2
        print("jal rd:",rd,"imm[20:0]:",imme)
        return "jal"





# global variables imme,rd,control,multiClock
# decode buffer registers(pipeline registers) decodeRA,decodeRB,decodeRD
# decodeRA,decodeRB stores intial values contains registers rs1 and rs2 and decodeRD=rd(value of destination register)
# control=1 if there is a destination register in instruction else control=0
# datadependence=[0,0,0] is a global list for checking data hazards that stores last two instruction's rd values and current rd value
# global variable instcount defined in main initially equals to 0 

def pipelinedecode(inst):
    global imme,rd,control,multiClock
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
        return "jal"






