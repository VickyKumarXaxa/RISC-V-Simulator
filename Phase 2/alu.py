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

from bitstring import BitArray

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
	global RZ, pc, pc_temp, aluRZ, aludfRZ, multiClock
	
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
		
	#Updating the ALU data forwarding registers
	aludfRZ = RZ
	
	#updating the alu output
	aluRZ = RZ
	
	#Updating the Clock value
	multiClock = multiClock + 1
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

