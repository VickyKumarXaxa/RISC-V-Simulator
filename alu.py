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

#Global variables (Same as diagram)
#RA
#RB
#RZ
#PC
#PC_temp
#MuxB
#imme
#IR
#RD
#RY

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
		RZ = RA + imme*2
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


