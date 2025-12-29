# 🚀 RV32I Verification Flow

## 📌 Project Overview
This repository contains the RTL design and simulation environment for a 5-stage pipelined 32-bit **RISC-V** processor.

The processor implements a subset of the **RV32I** instruction set and follows the classic pipeline architecture:

> **IF → ID → EX → MEM → WB** 

The core focuses on efficient execution by handling **data and control hazards** using dedicated **Forwarding** and **Hazard** units.

---

## ⚙️ Key Features

### 🧮 Supported Instruction Types
- ✅ **R-Type** (includes ADD, SUB, AND, OR, SLT)
- ✅ **I-Type** (includes LW, ADDI, ANDI, ORI, SLTI)
- ✅ **S-Type** (includes SW)
- ✅ **B-Type** (includes BEQ)
- ✅ **J-Type** (includes JAL)

### 🔁 Hazard Handling
- **Forwarding Unit:**
    Resolves **Read-After-Write (RAW)** data hazards from **MEM** and **WB** stages. 
- **Hazard Unit:**
    Handles **load-use stalls** (1-cycle bubble) and **branch flushes** (2-cycles via NOP).

### ⚡ Performance
- Achieves an **average CPI $\approx 1.3378$** on the comprehensive test suite.
- Demonstrates **high throughput and efficiency** compared to the single-cycle version.

---

## 🧠 Processor Architecture

![RV32I Architecture](Images/My_RV32I_Architecture.png)


---

# 💻 Development and Simulation Flow (Automated Scripts)

The entire verification process is managed by a modular Python flow control script (`run_sim.py`), which handles the assembly-to-hex conversion, compilation, simulation, and analysis.

### 1. `generate_hex.py` (Instruction Converter)

This script is crucial for setting up the simulation:

* **Function:** Converts the human-readable assembly program file (`program.asm`) into a machine-readable format.
* **Output:** The **`risc_memfile.hex`** file, which is loaded into the Instruction Memory module (`risc.v`) at initialization.

### 2. `run_sim.py` (Verification Flow Manager)

This is the main entry point for running the verification flow. It orchestrates the entire process using **Icarus Verilog (`iverilog`/`vvp`)** and **GTKWave**.

* **Simulation Output:** During execution, the VVP simulation results (messages, register writes, final status) are redirected to the **`risc_sim.log`** file for easy analysis.

### ⚙️ Main Command

The default command executes the full flow: Hex generation, Compilation, Simulation, and GTKWave launch.

| Command | Description |
| :--- | :--- |
| `python run_sim.py` | Runs the full verification flow. |

### 🔬 Simulation Control Commands

The `run_sim.py` script accepts optional flags to skip specific steps, useful for debugging or quick re-runs.

| Command | Effect | Use Case |
| :--- | :--- | :--- |
| `python run_sim.py --no-sim` | **Skips** the VVP simulation and GTKWave. | Used for quick syntax check and **compilation-only** runs. |
| `python run_sim.py --no-gui` | **Skips** launching GTKWave. | Used when you only need to check the **log file output** (`risc_sim.log`) without viewing waveforms. |

### 🧹 Cleaning Command

This command removes all generated files to reset the environment.

| Command | Files Removed |
| :--- | :--- |
| `python run_sim.py --clean` | `riscv_sim_executable`, `risc.vcd`, `risc_memfile.hex`, **`risc_sim.log`** |

---

# 📊 RISC-V Custom Performance Testbench

This report summarizes the performance of our **RISC-V ASM benchmark program** executed on the pipelined RTL design.

---

## 📝 Instruction Distribution

The benchmark program (program3) executed a total of **74 instructions**, categorized as follows:

| **Instruction Type** | **Count** | **Percentage** |
| :--- | :--- | :--- |
| **R-type** (add) | 11 | 14.85% |
| **I-type** (addi) | 40 | 54.05% |
| **Load** (lw) | 1 | 1.35% |
| **Store** (sw) | 3 | 4.05% |
| **Branch** (beq) | 19 | 25.65% |
| **Total** | **74** | **100%** |

> **Note:** Counts reflect **instructions actually retired** in the RTL design. Branch flushes and load-use stalls affect the totals.

---

## ⚡ Summary Table

| Core / Design | Cycles | Instructions Retired | CPI |
|---------------|--------|--------------------|-----|
| Ideal Single-Cycle | 74 | 74 | 1.00 |
| **Pipelined RV32I (with stalls)** | **99** | **74** | **1.3378** |

**Observations:**

- The pipelined CPI > 1 due to **load-use and branch stalls**.  
- Skipped dummy instructions and branch flushes explain why not all instructions in the HEX are counted as retired.  
- Despite higher CPI, the pipelined design is faster in **real time**, as each pipeline stage has a shorter clock period than a single-cycle core.

---

## 🛠️ Technologies Used
- ✅ Verilog HDL
- ✅ Python (Flow Control and Instruction Generation)
- ✅ Icarus Verilog (Compiler & Simulator)
- ✅ GTKWave (Waveform Visualization)
- ✅ VS Code (Development)


