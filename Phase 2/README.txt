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

Work Performed (Phase 1) 
------------
1. 2019CSB1101 Nema Ram Meghwal => Step 1 (Fetch) : Functions -> Fetch()
2. 2019CSB1115 Sahdev           => Step 5 (WriteBack) : Functions -> WriteBack(), register[]
3. 2019CSB1043 Ashish Sulania   => Step 2 (Decode) : Functions -> decode()
4. 2019CSB1117 Samir P Salim    => Step 4 (Memory) : Functions -> access_memory(), initialize()
5. 2019CSB1131 Vicky Kumar Xaxa => Step 3 (ALU) : Functions -> alu()

Work Perfored (Phase 2)
------------
1. 2019CSB1115 Sahdev
    => Pipelined extension of memory access and writeback stage
    => Addition of static branch predictor in fetch
    => DataMemory and TextMemory hash tables
2. 2019CSB1043 Ashish Sulania
    => Pipelined extension of decode
    => data dependence list to store the register names of last two instructions
    => Decode Buffer variables
3. 2019CSB1131 Vicky Kumar Xaxa
    => Pipelined extension of ALU
    => dependenceChecker() for checking data dependence according to the data dependence table
    => AlU Buffer and alu data forwarding variables

Requirements
--------------
1. Python3
2. bitstring-3.1.7 package. To install download the package from https://pypi.org/project/bitstring/


How to execute
--------------
./RISC-V-Simulator-main/python3 main.py

Input on/off for the following variables when asked
1.knobPipeline (for turning pipeline on/off)
2.knobDataFor (for turning data forwarding on/off)
3.knobRegister (for printing registers after each cycle)
4.knobPipelineRegister (for printing pipeline buffer variables after each cycle)
5.knobSpecial (for printing pipeline buffer variables for specific instruction no.)

Input format of MEM file
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

At the end of the execution the program outputs the following :
1. If pipeline is turned off
   Total Cycles
   Total Instructions
   CPI
   No. of Data Transfer
   No. of ALU Instructions
   No. of Control Instructions

2. If pipeline is turned on
    Total Cycles
    Total Instructions
    CPI
    No. of Data Transfer
    No. of ALU Instructions
    No. of Control Instructions
    Stall Count
    No. of data Hazards
    No. of control Hazards
    No. of branch mispredictions
    No. of data Hazard stall
    No. of control Hazard stall

