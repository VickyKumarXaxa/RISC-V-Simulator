.data
num: .word 10

.text
# x1 = n
# x2 = final result
lw x1, num
bne x1, x0, start # branch if n!=0
add x2, x0, x0
beq x0, x0, end # end

start:
addi x1, x1, -1 # n = n - 1
add x3, x0, x0 # x = 0
addi x2, x0, 1 # y = 1
loop:
bge x0, x1, end # if 0 >= n
add x5, x3, x2 # tmp = x + y
add x3, x2, x0 # x = y
add x2, x5, x0 # y = tmp
addi x1, x1, -1 # n = n - 1
beq x0, x0, loop # continue loop
end: