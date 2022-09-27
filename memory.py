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
    global cap
    global memory
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
