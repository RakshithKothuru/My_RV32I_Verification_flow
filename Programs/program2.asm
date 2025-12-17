# x1 = 5
addi x1, x0, 5

# x2 = 10
addi x2, x0, 10

# x3 = x1 + x2 = 15
add  x3, x1, x2

# Logical ops
and  x4, x1, x2
or   x5, x1, x2

# Set less than (signed)
slt  x6, x1, x2    # x6 = 1

# Immediate ops
addi x7, x0, -3
andi x8, x2, 3
ori  x9, x1, 4
slti x10, x1, 8    # x10 = 1

# Store x3 -> MEM[0]
sw   x3, x0, 0

# Load MEM[0] -> x11
lw   x11, x0, 0

# Branch NOT taken (x3 == x11)
beq  x3, x11, 8

# This executes
addi x12, x0, 111

# Jump over next instruction
jal  x0, 8

# Skipped
addi x13, x0, 222

# Final instruction
addi x14, x0, 99
