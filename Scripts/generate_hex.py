import sys
import os

# --- Configuration ---
# Name of the assembly file to read (your input)
INPUT_ASM_FILE = "program.asm"
# Name of the HEX file to write (your output for Verilog)
OUTPUT_HEX_FILE = "risc_memfile.hex"

# --- Opcode and Function Code Definitions (Simplified Set) ---
# NOTE: This is a highly simplified set for R-type and I-type instructions.
# A full RISC-V assembler is complex and requires full opcode/funct3/funct7 mappings.

# R-Type: ADD, SUB, AND (Opcode 0110011)
OP_R_TYPE = '0110011'

FUNCT3 = {
    'add': '000',
    'sub': '000',  # (Needs funct7 check)
    'and': '111',
    'or':  '110'
}

FUNCT7 = {
    'add': '0000000',
    'sub': '0100000',
    'and': '0000000',
    'or':  '0000000'
}

# I-Type: ADDI (Opcode 0010011)
OP_I_TYPE = '0010011'

FUNCT3_I = {
    'addi': '000'
}

# --- Register Mapping (x0 to x31) ---
# Maps assembly register names (e.g., x1) to their 5-bit binary code.
REGISTERS = {f'x{i}': format(i, '05b') for i in range(32)}
# -----------------------------------

def get_register_binary(reg_name):
    """Checks and returns the 5-bit binary code for a register."""
    if reg_name not in REGISTERS:
        raise ValueError(f"Invalid register name: {reg_name}")
    return REGISTERS[reg_name]

def assemble_r_type(parts):
    """
    Assembles R-Type instruction: OPERATION Rd, Rs1, Rs2
    Format: funct7 (7) | Rs2 (5) | Rs1 (5) | funct3 (3) | Rd (5) | opcode (7)
    """
    op_name = parts[0].lower()

    # Handle SUB: funct7 is different
    funct7_val = FUNCT7[op_name]
    if op_name == 'sub':
        funct7_val = '0100000'

    machine_code = (
        funct7_val +
        get_register_binary(parts[3]) +  # Rs2
        get_register_binary(parts[2]) +  # Rs1
        FUNCT3[op_name] +                # funct3
        get_register_binary(parts[1]) +  # Rd
        OP_R_TYPE                        # opcode
    )
    return machine_code

def assemble_i_type(parts):
    """
    Assembles I-Type instruction: ADDI Rd, Rs1, Imm
    Format: immediate (12) | Rs1 (5) | funct3 (3) | Rd (5) | opcode (7)
    """
    op_name = parts[0].lower()

    imm_val = int(parts[3])

    # The immediate is 12 bits. Check if it fits (or truncate)
    if imm_val < -2048 or imm_val > 2047:
        print(f"Warning: Immediate value {imm_val} for {op_name} is outside the 12-bit signed range.")

    # Format the immediate as 12-bit signed binary
    imm_binary = format(imm_val & 0xFFF, '012b')

    machine_code = (
        imm_binary +                     # Imm (12 bits)
        get_register_binary(parts[2]) +  # Rs1
        FUNCT3_I[op_name] +              # funct3
        get_register_binary(parts[1]) +  # Rd
        OP_I_TYPE                        # opcode
    )
    return machine_code

def assemble_line(line):
    """Parses a single line of assembly and returns its 32-bit machine code."""
    line = line.strip()
    if not line or line.startswith('#'):
        return None  # Ignore comments and empty lines

    # Normalize the instruction (e.g., "ADD x1, x2, x3" -> "ADD x1 x2 x3")
    parts = line.replace(',', ' ').split()
    if not parts:
        return None

    instruction = parts[0].lower()

    if instruction in FUNCT3 and instruction in FUNCT7:
        # R-Type: ADD, SUB, AND, OR
        if len(parts) != 4:
            raise ValueError(f"R-Type instruction '{instruction}' requires 3 operands. Found: {len(parts)-1}")
        return assemble_r_type(parts)

    elif instruction in FUNCT3_I:
        # I-Type: ADDI
        if len(parts) != 4:
            raise ValueError(f"I-Type instruction '{instruction}' requires 3 operands. Found: {len(parts)-1}")
        return assemble_i_type(parts)

    else:
        raise NotImplementedError(f"Instruction '{instruction}' is not implemented in this assembler script.")

def main():
    """Main function to read assembly, assemble, and write hex file."""
    print("--- RISC-V HEX File Generator ---")

    try:
        # 1. Read Assembly Input
        with open(INPUT_ASM_FILE, 'r') as f:
            assembly_lines = f.readlines()

        machine_codes = []
        for i, line in enumerate(assembly_lines):
            try:
                mc = assemble_line(line)
                if mc:
                    machine_codes.append(mc)
            except (ValueError, NotImplementedError) as e:
                print(f"Error on line {i+1} ('{line.strip()}'): {e}", file=sys.stderr)
                sys.exit(1)

        # 2. Write Hex Output
        if not machine_codes:
            print(f"Error: No valid instructions found in {INPUT_ASM_FILE}", file=sys.stderr)
            sys.exit(1)

        with open(OUTPUT_HEX_FILE, 'w') as f:
            for mc in machine_codes:
                hex_code = format(int(mc, 2), '08x')   # 32-bit hex
                f.write(f"{hex_code}\n")

        print(f" Success! Generated {len(machine_codes)} instructions.")
        print(f"Output written to: {OUTPUT_HEX_FILE}")

    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_ASM_FILE}' not found.", file=sys.stderr)
        print("Please create this file and add your assembly instructions.")
        sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
