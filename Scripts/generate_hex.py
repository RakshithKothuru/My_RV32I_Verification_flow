import sys

# ================= CONFIG =================
INPUT_ASM_FILE  = "program.asm"
OUTPUT_HEX_FILE = "risc_memfile.hex"
# ==========================================

# ================= OPCODES =================
OP_R_TYPE = '0110011'
OP_I_TYPE = '0010011'
OP_LOAD   = '0000011'
OP_STORE  = '0100011'
OP_BRANCH = '1100011'
OP_JAL    = '1101111'
# ==========================================

# ================= FUNCT TABLES =================
FUNCT3_R = {
    'add':'000','sub':'000','and':'111','or':'110','xor':'100'
}

FUNCT7_R = {
    'add':'0000000','sub':'0100000','and':'0000000','or':'0000000','xor':'0000000'
}

FUNCT3_I = {
    'addi':'000','andi':'111','ori':'110','xori':'100'
}

FUNCT3_LOAD  = {'lw':'010'}
FUNCT3_STORE = {'sw':'010'}

FUNCT3_BRANCH = {
    'beq':'000','bne':'001'
}
# ================================================

# ================= REGISTERS =================
REGISTERS = {f'x{i}': format(i, '05b') for i in range(32)}
# ==============================================

def get_reg(r):
    if r not in REGISTERS:
        raise ValueError(f"Invalid register {r}")
    return REGISTERS[r]

def imm_bin(val, bits):
    """Returns 2's complement signed binary string of length 'bits'."""
    return format(val & ((1 << bits) - 1), f'0{bits}b')

# ================= ASSEMBLERS =================

def assemble_r(parts):
    op = parts[0]
    return (
        FUNCT7_R[op] +
        get_reg(parts[3]) +
        get_reg(parts[2]) +
        FUNCT3_R[op] +
        get_reg(parts[1]) +
        OP_R_TYPE
    )

def assemble_i(parts, funct3, opcode):
    rd = get_reg(parts[1])
    if opcode == OP_LOAD:
        # lw format: lw rd, offset(rs1)
        offset_part = parts[2]
        imm_str, rs1_str = offset_part.replace(')','').split('(')
        rs1 = get_reg(rs1_str)
        imm = int(imm_str)
    else:
        # addi format: addi rd, rs1, imm
        rs1 = get_reg(parts[2])
        imm = int(parts[3])
    return (
        imm_bin(imm, 12) +
        rs1 +
        funct3 +
        rd +
        opcode
    )

def assemble_s(parts):
    # sw format: sw rs2, offset(rs1)
    rs2 = get_reg(parts[1])
    offset_part = parts[2]
    imm_str, rs1_str = offset_part.replace(')','').split('(')
    rs1 = get_reg(rs1_str)
    imm = int(imm_str)
    imm12 = imm_bin(imm, 12)
    # S-type: imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | opcode
    return (
        imm12[:7] +
        rs2 +
        rs1 +
        FUNCT3_STORE[parts[0]] +
        imm12[7:] +
        OP_STORE
    )

def assemble_b(parts):
    # bne/beq format: bne rs1, rs2, imm
    rs1 = get_reg(parts[1])
    rs2 = get_reg(parts[2])
    imm = int(parts[3])
    imm13 = imm_bin(imm, 13)
    # B-type: imm[12]|imm[10:5]|rs2|rs1|funct3|imm[4:1]|imm[11]|opcode
    return (
        imm13[0] +        # imm[12]
        imm13[2:8] +      # imm[10:5]
        rs2 +
        rs1 +
        FUNCT3_BRANCH[parts[0]] +
        imm13[8:12] +     # imm[4:1]
        imm13[1] +        # imm[11]
        OP_BRANCH
    )

def assemble_jal(parts):
    # jal rd, imm
    rd = get_reg(parts[1])
    imm = int(parts[2])
    imm21 = imm_bin(imm, 21)
    # J-type: imm[20]|imm[10:1]|imm[11]|imm[19:12]|rd|opcode
    return (
        imm21[0] +
        imm21[10:20] +
        imm21[9] +
        imm21[1:9] +
        rd +
        OP_JAL
    )

# ================= PARSER =================

def assemble_line(line):
    line = line.split('#')[0].strip()
    if not line:
        return None

    parts = line.replace(',', ' ').split()
    inst = parts[0].lower()

    if inst in FUNCT3_R:
        return assemble_r(parts)
    elif inst in FUNCT3_I:
        return assemble_i(parts, FUNCT3_I[inst], OP_I_TYPE)
    elif inst in FUNCT3_LOAD:
        return assemble_i(parts, FUNCT3_LOAD[inst], OP_LOAD)
    elif inst in FUNCT3_STORE:
        return assemble_s(parts)
    elif inst in FUNCT3_BRANCH:
        return assemble_b(parts)
    elif inst == 'jal':
        return assemble_jal(parts)
    else:
        raise NotImplementedError(f"{inst} not supported")

# ================= MAIN =================

def main():
    print("---- RV32I HEX GENERATOR ----")

    try:
        with open(INPUT_ASM_FILE) as f:
            lines = f.readlines()

        machine_codes = []
        for i, line in enumerate(lines):
            try:
                mc = assemble_line(line)
                if mc:
                    machine_codes.append(mc)
            except Exception as e:
                print(f"Error at line {i+1}: {line.strip()}")
                print(e)
                sys.exit(1)

        if not machine_codes:
            raise RuntimeError("No valid instructions found")

        with open(OUTPUT_HEX_FILE, 'w') as f:
            for mc in machine_codes:
                f.write(f"{int(mc,2):08x}\n")

        print(f"Generated {len(machine_codes)} instructions")
        print(f"Output: {OUTPUT_HEX_FILE}")

    except FileNotFoundError:
        print(f"File {INPUT_ASM_FILE} not found")

if __name__ == "__main__":
    main()
