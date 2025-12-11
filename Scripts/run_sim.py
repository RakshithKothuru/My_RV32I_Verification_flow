import subprocess
import sys
import os
import argparse
import shutil

# --- GLOBAL CONFIGURATION (Should be the only global definitions outside the class) ---
GTKWAVE_COMMAND = 'gtkwave'
HEX_GENERATOR_SCRIPT = "generate_hex.py"
# ----------------------------------------------------------------------------------

class RiscvSimFlow:
    """
    Manages the entire RISC-V verification flow, holding configuration
    and execution logic for each step (Compile, Sim, GTKWave, Clean).
    """
    def __init__(self, verilog_dir="."):
        # --- Project File Configuration (Class Attributes) ---
        self.VERILOG_DIR = verilog_dir
        self.DESIGN_FILE = "risc.v"
        self.TESTBENCH_FILE = "risc_tb.v"
        self.OUTPUT_SIM_NAME = "riscv_sim_executable"
        self.VCD_FILE_NAME = "risc.vcd"
        self.GTKW_CONFIG_FILE = "risc.gtkw"
        self.HEX_FILE_NAME = "risc_memfile.hex"
        self.LOG_FILE_NAME = "risc_sim.log"

        # Construct all necessary paths once
        self.DESIGN_PATH = os.path.join(self.VERILOG_DIR, self.DESIGN_FILE)
        self.TESTBENCH_PATH = os.path.join(self.VERILOG_DIR, self.TESTBENCH_FILE)
        self.VCD_FILE_PATH = os.path.join(self.VERILOG_DIR, self.VCD_FILE_NAME)
        self.HEX_FILE_PATH = os.path.join(self.VERILOG_DIR, self.HEX_FILE_NAME)
        self.LOG_FILE_PATH = os.path.join(self.VERILOG_DIR, self.LOG_FILE_NAME)
        # ---------------------------------------------------

    # --- UTILITY FUNCTION: Runs an external process ---
    def _run_process(self, command, step_name, output_file=None):
        """Utility function to run a command and handle errors, now an internal method."""
        print(f"\n--- {step_name.upper()} ---")
        print(f"Running command: {' '.join(command)}")

        try:
            # Popen for logging simulation output to a file
            if output_file:
                with open(output_file, 'w') as f:
                    process = subprocess.Popen(
                        command,
                        stdout=f,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    stdout, stderr = process.communicate()
                    return_code = process.returncode
            # subprocess.run for simple steps like compilation
            else:
                result = subprocess.run(command, capture_output=True, text=True, check=True)
                stdout = result.stdout
                stderr = result.stderr
                return_code = result.returncode
                # Returning the result here allows the caller to inspect stdout/stderr if needed
                return result 

            if return_code != 0:
                # Re-raise as CalledProcessError for consistent error handling
                raise subprocess.CalledProcessError(return_code, command, stdout, stderr)

            if stderr:
                print(f"[{step_name} Warnings/Notes]:\n{stderr}")

            return True # Success indicator for Popen case

        except subprocess.CalledProcessError as e:
            print(f"\n {step_name} FAILED with exit code: {e.returncode}", file=sys.stderr)
            if e.stderr:
                print(f"Stderr: {e.stderr}", file=sys.stderr)
            elif os.path.exists(output_file):
                print(f"Check simulation log for details: {output_file}", file=sys.stderr)
            sys.exit(1)

        except FileNotFoundError:
            print(f"\n CRITICAL ERROR: The tool '{command[0]}' was not found...", file=sys.stderr)
            sys.exit(1)

    # --------- FLOW STEP: Check Tool Availability ------------------------------------------

    def check_tool_availability(self):
        """Checks if iverilog, vvp, and gtkwave are installed and in PATH."""
        CRITICAL_TOOLS = {
            'iverilog': "Verilog Compiler",
            'vvp': "Verilog Simulator",
            GTKWAVE_COMMAND: "Waveform Viewer (GTKWave)"
        }
        missing_tools = []

        print("\n--- ENVIRONMENT CHECK ---")
        for tool, description in CRITICAL_TOOLS.items():
            if shutil.which(tool) is None:
                print(f"  [MISSING] {description}: '{tool}' not found in system PATH.")
                missing_tools.append(tool)
            else:
                print(f"  [OK] {description}: '{tool}' found.")

        if missing_tools:
            print("\n CRITICAL ERROR: The following required tools are missing or inaccessible.")
            print(" Please ensure they are installed and configured in your system's PATH.")
            sys.exit(1)
        print("Environment check successful!")

    # --------- FLOW STEP: Instruction Hex Generation ---------------------------------------

    def generate_hex(self):
        """Runs the assembly-to-hex generator script."""
        hex_gen_command = [sys.executable, HEX_GENERATOR_SCRIPT]
        self._run_process(hex_gen_command, "Hex File Generation")

        if not os.path.exists(self.HEX_FILE_PATH):
            print(f"\n ERROR: Hex file '{self.HEX_FILE_NAME}' was not created by '{HEX_GENERATOR_SCRIPT}'. Check generator script output.", file=sys.stderr)
            sys.exit(1)
        print(f"Hex file check successful: {self.HEX_FILE_NAME} is ready.")

    # --------- FLOW STEP: Compilation -----------------------------------------------------

    def compile_design(self):
        """Compiles the Verilog design and testbench using iverilog."""
        sim_command = ['iverilog', '-o', self.OUTPUT_SIM_NAME, self.DESIGN_PATH, self.TESTBENCH_PATH]
        self._run_process(sim_command, "Compilation (iverilog)")
        print("Compilation successful! Executable created.")

    # --------- FLOW STEP: Simulation ------------------------------------------------------

    def run_simulation(self):
        """Runs the compiled VVP simulation and analyzes the log."""
        run_command = ['vvp', f"./{self.OUTPUT_SIM_NAME}"]
        
        # Output simulation stdout to the log file
        self._run_process(run_command, "Simulation (vvp)", output_file=self.LOG_FILE_PATH)

        # Automated Log Analysis
        print("\n--- ANALYZING SIMULATION LOG ---")
        try:
            with open(self.LOG_FILE_PATH, 'r') as f:
                log_content = f.read()
        except FileNotFoundError:
            print(f"Error: Log file {self.LOG_FILE_NAME} not found.", file=sys.stderr)
            return

        if "TEST PASSED" in log_content:
            print(f" TEST SUITE RESULT: PASSED")
        else:
            print(f" TEST SUITE RESULT: FAILED (See {self.LOG_FILE_NAME} for details)")

    # --------- FLOW STEP: GTKWave Launch -------------------------------------------------

    def launch_gtkwave(self):
        """Launches the GTKWave viewer with the generated VCD file."""
        print(f"\n--- LAUNCHING GTKWAVE ---")

        if not os.path.exists(self.VCD_FILE_PATH):
            print(f"Warning: VCD file '{self.VCD_FILE_NAME}' not found. Cannot launch GTKWave.", file=sys.stderr)
            return

        gtkwave_base_cmd = [GTKWAVE_COMMAND, self.VCD_FILE_PATH]

        # Check for GTKW config file
        if os.path.exists(self.GTKW_CONFIG_FILE):
            gtkwave_base_cmd.extend(['-a', self.GTKW_CONFIG_FILE])
            print(f"Loading waveform configuration from {self.GTKW_CONFIG_FILE}.")
        else:
            print(f"Warning: Configuration file '{self.GTKW_CONFIG_FILE}' not found. Loading raw VCD.")

        # Platform-specific launch logic to detach the GUI
        if sys.platform.startswith('win'):
            gtkwave_cmd = ['start'] + gtkwave_base_cmd
            subprocess.Popen(gtkwave_cmd, shell=True)
        else:
            subprocess.Popen(gtkwave_base_cmd)
        print(f"Opened {self.VCD_FILE_NAME} in GTKWave.")

    # --------- FLOW STEP: Clean up generated files --------------------------------------

    def clean(self):
        """Removes all generated simulation and temporary files."""
        print("\n--- CLEANING PROJECT FILES ---")
        files_to_remove = [
            self.OUTPUT_SIM_NAME,
            self.VCD_FILE_PATH,
            self.HEX_FILE_PATH,
            self.LOG_FILE_PATH
        ]
        
        cleaned_count = 0
        for file_path in files_to_remove:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"  [DELETED] {file_path}")
                    cleaned_count += 1
                except OSError as e:
                    print(f"  [ERROR] Could not delete {file_path}: {e}", file=sys.stderr)

        if cleaned_count == 0:
            print("No simulation files found to clean.")
        else:
            print(f"Cleaning complete. Removed {cleaned_count} file(s).")


# ---------- Argument Parsing (Remains outside the class) --------------------------------

def parse_arguments():
    """Sets up the argument parser for the verification flow."""
    parser = argparse.ArgumentParser(
        description="Automated RISC-V Verification and Simulation Flow.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # Arguments remain the same
    parser.add_argument('--clean', action='store_true', help='Remove all generated files and exit.')
    parser.add_argument('--no-sim', action='store_true', help='Compile the design but skip the VVP simulation and GTKWave launch.')
    parser.add_argument('--no-gui', action='store_true', help='Run the full simulation but skip launching GTKWave.')
    return parser.parse_args()


#------------------ MAIN EXECUTION FLOW (Simplified) -------------------------------------

def main():
    """Main entry point: sets up the flow manager and executes steps."""
    args = parse_arguments()
    flow = RiscvSimFlow() # Initialize the flow manager

    if args.clean:
        flow.clean()
        sys.exit(0)

    print(f"--- RISC-V Verification Flow Start ---")
    
    # Pre-check tools (Essential step)
    flow.check_tool_availability()
    
    # 1. Generate Hex
    flow.generate_hex()

    # 2. Compile
    flow.compile_design()

    # 3. Simulate & Launch GUI
    if not args.no_sim:
        flow.run_simulation()
        if not args.no_gui:
            flow.launch_gtkwave()
        else:
            print("\nSkipping GTKWave launch per --no-gui flag.")
    else:
        print("\nSkipping simulation and GUI launch per --no-sim flag. Compilation successful.")

    print("\n--- Flow Complete ---")

if __name__ == "__main__":
    main()
