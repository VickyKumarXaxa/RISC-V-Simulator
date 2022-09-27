================================================
Functional Simulator for RISCV Processor
================================================

README

Table of contents
1. Work distribution
2. Requires Libraries
3. How to execute
4. Input format
5. Output format

Work Distribution
------------
1. 2019CSB1101 Nema Ram Meghwal => Step 1 (Fetch) : Functions -> Fetch()
2. 2019CSB1115 Sahdev           => Step 5 (WriteBack) : Functions -> WriteBack(), register[]
3. 2019CSB1043 Ashish Sulania   => Step 2 (Decode) : Functions -> decode()
4. 2019CSB1117 Samir P Salim    => Step 4 (Memory) : Functions -> access_memory(), initialize(),print_mem(),memory[]
5. 2019CSB1131 Vicky Kumar Xaxa => Step 3 (ALU) : Functions -> alu()


Requirements
--------------
1. Python3
2. bitstring-3.1.7 package. To install download the package from https://pypi.org/project/bitstring/


How to execute
--------------
./RISC-V-Simulator-main/python3 main.py

Input format
--------------
Input to the simulator is MEM file (instruction.mc) that contains the encoded instruction and the corresponding address in following format :
0x0 0xE3A0200A
0x4 0xE3A03002
0x8 0x003202B3

Output format
--------------
The simulator also prints messages for each stage for each instruction, for example for the third instruction above following messages are printed.
    • Fetch prints:
        ◦ INSTRUCTION : 0x003202B3
    • Decode prints:
        ◦ decode:
        ◦ instruction is of r format
        ◦ add rs1: 4 rs2: 3 rd: 5
        ◦ values [rs1]: 0 [rs2]:0   “(values that you stores initially in registers 4(rs1) and 3(rs2) here I am assuming as 0 and 0) “
    • Execute prints:
        ◦ ALU
        ◦ OPERATION Preforming :  add 
        ◦ RZ = sum : 0
    • Memory prints:
        ◦ Stored memory in the following format :
        ◦ 0x10000000 0x00101526
        ...
