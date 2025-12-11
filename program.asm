# Program to test basic arithmetic and logic
# R-Type: ADD Rd, Rs1, Rs2
# I-Type: ADDI Rd, Rs1, Imm

# 1. Initialize register x1 with 10 (decimal)
addi x1, x0, 10

# 2. Initialize register x2 with 2 (decimal)
addi x2, x0, 2

# 3. Perform addition: x3 = x1 + x2 (Result: 12)
add x3, x1, x2

# 4. Perform subtraction: x4 = x3 - x2 (Result: 10)
sub x4, x3, x2

# 5. Perform logical AND: x5 = x3 & x2 (Result: 12 & 2 -> 0000..1100 & 0000..0010 -> 0000..0000 -> 0)
and x5, x3, x2

# 6. Halt or Loop (essential to stop the simulation)
# A simple way to stop is to jump to the current address infinitely
# (JALR x0, x0, 0 is often used, but not implemented in this simple script).
# We'll rely on the testbench to halt after a certain number of cycles for now.
