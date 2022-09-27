.data
arr: .word 5, 4, 3, 2, 1
size: .word 5

.text
lw x10, arr
lw x11, size
jal x1, sort
beq x0, x0, exit

swap:
addi x4, x0, 2
sll x6, x11, x4		#x6 = k*4
add x6, x10, x6		#x6 = v + (k*4)
lw x5, 0(x6)		#x5 = v[k]
lw x7, 4(x6)		#x7 = v[k+1]
sw x7, 0(x6)		#v[k] = x7
sw x5, 4(x6)		#x[k+1] = x5
jalr x0, x1, 0

sort: addi sp, sp, -20		#space for 5 registers
sw x1, 16(sp)
sw x22, 12(sp)
sw x21, 8(sp)
sw x20, 4(sp)
sw x19, 0(sp)
addi x21, x10, 0
addi x22, x11, 0
addi x19, x0, 0

for1tst: bge x19, x22, exit1
addi x20, x19, -1

for2tst: blt x20, x0, exit2
addi x4, x0, 2
sll x5, x20, x4
add x5, x21, x5
lw x6, 0(x5)
lw x7, 4(x5)
ble x6, x7, exit2

addi x10, x21, 0
addi x11, x20, 0
jal x1, swap

addi x20, x20, -1
jal, x0 for2tst

exit2: addi x19, x19, 1
jal, x0 for1tst

exit1: lw x19, 0(sp)
lw x20, 4(sp)
lw x21, 8(sp)
lw x22, 12(sp)
lw x1, 16(sp)
addi sp, sp, 20
jalr x0, x1, 0

exit: