# 🚀 5-Stage Pipelined RISC-V Processor

## 📌 Project Overview
This repository contains the RTL design and simulation of a 5-stage pipelined 32-bit **RISC-V** processor.  
The processor implements a subset of the **RV32I** instruction set and follows the classic pipeline architecture:

> **IF → ID → EX → MEM → WB**

The processor handles **data and control hazards** effectively using dedicated **Forwarding** and **Hazard** units, ensuring correct execution and efficient performance.

---

## 🛠️ Technologies Used
- ✅ Verilog HDL  
- ✅ Icarus Verilog (simulation)  
- ✅ GTKWave (waveform visualization)  
- ✅ VS Code (development)  

---

## 🧮 Supported Instruction Types
- ✅ **R-Type** (includes ADD, SUB, AND, OR, SLT)
- ✅ **I-Type** (includes LW, ADDI, ANDI, ORI, SLTI)
- ✅ **S-Type** (includes SW)
- ✅ **B-Type** (includes BEQ)
- ✅ **J-Type** (includes JAL)

---

## 🧠 Arithmetic, Logical & Control Operations Supported
- ✅ **Addition** (`ADD`, `ADDI`)
- ✅ **Subtraction** (`SUB`)
- ✅ **Bitwise AND** (`AND`)
- ✅ **Bitwise OR** (`OR`)
- ✅ **Set Less Than** (`SLT`)
- ✅ **Branch if Equal** (`BEQ`)
- ✅ **Jump and Link** (`JAL`)

---

## 📦 Pipeline Stage Details

### 🟦 Instruction Fetch (IF)
- Fetches instructions using the Program Counter (PC).
- **PC source mux** selects among:
  - `PC+4`
  - **branch target (B-type)**
  - **jump target (JAL)**
- **Flush logic** injects a bubble into IF/ID when a branch or jump is taken.
- **Stall signal** freezes PC update during load-use hazards.

### 🟩 Instruction Decode (ID)
- Decodes opcode/fields, reads operands from the register file.
- **Immediate Generator** supports I-type, B-type, and J-type encodings.
- Generates control signals for EX/MEM/WB.
- **Hazard Detection Unit** checks for load-use hazards and triggers stall if needed.

### 🟨 Execute (EX)
- ALU performs arithmetic/logic and branch compare for `BEQ`.
- **Branch Unit** computes `target = PC + immB` and checks `(rs1 == rs2)`.
- **Jump Unit** computes `target = PC + immJ` for `JAL`.
- On **taken branch/jump**, asserts **flush** to squash IF/ID and redirect PC.
- **Forwarding logic** bypasses data from later pipeline stages.

### 🟧 Memory Access (MEM)
- Performs memory reads/writes for load/store (if implemented).
- Simple synchronous interface.

### 🟥 Write Back (WB)
- Writes ALU, memory result, or `PC+4` (for JAL) back to the destination register.

---

## ⚠️ Hazard Handling and Penalties

### 🔹 Data Hazards
- **RAW (with forwarding):** 0 cycles (no stall)  
- **Load–use hazard:** +1 cycle penalty (stall inserted)

### 🔹 Control Hazards
- **BEQ taken (resolved in EX):** +2 cycles penalty  
  - Wrong-path instructions in **ID** and **IF** must be flushed  
- **BEQ not taken:** 0 cycles   
- **JAL (if resolved in EX):** +2 cycles penalty
  - Wrong-path instructions in **ID** and **IF** must be flushed 

### 🔹 Structural Hazards
- **None** (Harvard architecture: separate instruction/data memories) → 0 cycles

---

## 📊 Hazard Penalty Summary

| Hazard Type           | Where Resolved | Penalty (Cycles) |
|-----------------------|----------------|------------------|
| RAW (with forwarding) | EX             | 0                |
| Load–use (forwarding) | MEM→WB timing  | +1               |
| BEQ taken             | EX             | +2               |
| BEQ not taken         | —              | 0                |
| JAL (EX target)       | EX             | +2               |
| Structural (Harvard)  | —              | 0                |

---


## 📊 Instruction Type Distribution

The benchmark program executed a total of **33 instructions**, categorized as follows:

| **Instruction Type** | **Count** | **Percentage** |
|-----------------------|:---------:|:--------------:|
| **R-type**            | 21        | 63.64%         |
| **Jump**              | 1         | 3.03%          |
| **Branch**            | 1         | 3.03%          |
| **Store**             | 2         | 6.06%          |
| **Load**              | 2         | 6.06%          |
| **I-type**            | 6         | 18.18%         |
| **Total**             | **33**    | **100%**       |

---

## 🔗 References
- Patterson, D. A., & Hennessy, J. L. (2017). *Computer Organization and Design RISC-V Edition: The Hardware Software Interface*. Morgan Kaufmann.  
- [RISC-V ISA Manual (Volume I: User-Level ISA)](https://riscv.org/technical/specifications/)  
- [RISC-V Wikipedia](https://en.wikipedia.org/wiki/RISC-V)  

