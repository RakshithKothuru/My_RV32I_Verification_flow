# Program to test basic arithmetic and logic

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
