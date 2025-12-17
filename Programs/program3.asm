# ------------------------------------
# Register initialization
# ------------------------------------
addi x1, x0, 0        # i = 0
addi x2, x0, 10       # loop limit = 10
addi x3, x0, 0        # sum = 0
addi x4, x0, 0        # memory base pointer
addi x5, x0, 1        # increment value
addi x9, x0, 1        # temp register for unconditional branch

# ------------------------------------
# Initialize memory
# mem[0]=5, mem[1]=7, mem[2]=9
# ------------------------------------
addi x6, x0, 5
sw   x6, 0(x4)

addi x6, x0, 7
sw   x6, 4(x4)

addi x6, x0, 9
sw   x6, 8(x4)

# ------------------------------------
# LOOP START (absolute offsets)
# ------------------------------------
lw   x7, 0(x4)        # load mem[i]
add  x3, x3, x7       # sum += mem[i]
addi x4, x4, 4        # next memory word
addi x1, x1, 1        # i++
addi x8, x0, 10       # loop limit in temp register
beq  x1, x8, 20       # if i == 10, skip next 5 instructions (exit loop)
beq  x0, x0, -20      # unconditional jump back 5 instructions (loop)

# ------------------------------------
# Store final result
# ------------------------------------
sw   x3, 40(x0)       # store sum in mem[10]

# ------------------------------------
# Skip dummy instructions using beq
# ------------------------------------
beq  x0, x0, 8        # skip next 2 instructions

# ------------------------------------
# Dummy instructions (should be skipped)
# ------------------------------------
addi x10, x0, 99
addi x11, x0, 88

# ------------------------------------
# End marker
# ------------------------------------
addi x12, x0, 0
