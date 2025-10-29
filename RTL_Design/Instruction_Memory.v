module Instruction_Memory(rst,A,RD);

  input rst;
  input [31:0]A;
  output [31:0]RD;

  reg [31:0] mem [1023:0];
  
  assign RD = (rst == 1'b0) ? {32{1'b0}} : mem[A[31:2]]; 
  
// testcase for branch instruction (flushing) and load data hazard (stalling)
 /*initial begin
    mem[0] = 32'h000002B3; // ADD x5, x0, x0
    mem[1] = 32'h00000333; // ADD x6, x0, x0
    mem[2] = 32'h00628863; // BEQ x5, x6, +16
    mem[3] = 32'h002083B3; // ADD x7, x1, x4 (flush)
    mem[4] = 32'h00000433; // ADD x8, x0, x0 (flush)
    mem[5] = 32'h006284B3; // ADD x9, x5, x6
    mem[6] = 32'h0052A303; // lw x6, x5, 05 
    mem[7] = 32'h000305B3; // ADD x11, x6, x0
    mem[8] = 32'h00000433; // ADD x8, x0, x0
end*/

// testcase for branch instruction (flushing) and jump (flushing)
 /*initial begin
    mem[0] = 32'h000002B3; // ADD x5, x0, x0
    mem[1] = 32'h00000333; // ADD x6, x0, x0
    mem[2] = 32'h00628863; // BEQ x5, x6, +16
    mem[3] = 32'h002083B3; // ADD x7, x1, x4 (flush)
    mem[4] = 32'h00000433; // ADD x8, x0, x0 (flush)
    mem[5] = 32'h006284B3; // ADD x9, x5, x6
    mem[6] = 32'h01000FEF; // JAL x31,16  
    mem[7] = 32'h000305B3; // ADD x11, x6, x0
    mem[8] = 32'h00000433; // ADD x8, x0, x0
    mem[9] = 32'h000002B3; // ADD x5, x0, x0
    mem[10] = 32'h00000333; // ADD x6, x0, x0
    mem[11] = 32'h000002B3; // ADD x5, x0, x0
    mem[12] = 32'h00000333; // ADD x6, x0, x0
end*/

// Original testcase

initial begin
    // ---------- Block 1 ( 1 branch and 1 jump) ----------
    mem[0]  = 32'h000002B3; // ADD x5, x0, x0
    mem[1]  = 32'h00000333; // ADD x6, x0, x0
    mem[2]  = 32'h00628863; // BEQ x5, x6, +16
    mem[3]  = 32'h002083B3; // ADD x7, x1, x4 (flush)
    mem[4]  = 32'h00000433; // ADD x8, x0, x0 (flush)
    mem[5]  = 32'h006284B3; // ADD x9, x5, x6
    mem[6]  = 32'h01000FEF; // JAL x31, 16  
    mem[7]  = 32'h000305B3; // ADD x11, x6, x0
    mem[8]  = 32'h00000433; // ADD x8, x0, x0
    mem[9]  = 32'h000002B3; // ADD x5, x0, x0
    mem[10] = 32'h00000333; // ADD x6, x0, x0
    mem[11] = 32'h000002B3; // ADD x5, x0, x0
    mem[12] = 32'h00000333; // ADD x6, x0, x0

    // ---------- Block 2 (1 data dependent load + 1 normal load) ----------
    mem[13] = 32'h000002B3; // ADD x5, x0, x0
    mem[14] = 32'h00000333; // ADD x6, x0, x0
    mem[15] = 32'h006284B3; // ADD x7, x1, x4
    mem[16] = 32'h0052A303; // lw x6, x5, 05   (data dependent load)
    mem[17] = 32'h006284B3; // ADD x9, x5, x6
    mem[18] = 32'h000305B3; // ADD x11, x6, x0
    mem[19] = 32'h00000433; // ADD x8, x0, x0
    mem[20] = 32'h000002B3; // ADD x5, x0, x0
    mem[21] = 32'h00000333; // ADD x6, x0, x0
    mem[22] = 32'h000002B3; // ADD x5, x0, x0
    mem[23] = 32'h00000333; // ADD x6, x0, x0
    mem[24] = 32'h0052A303; // lw x6, x5, 05   (data independent load)
    mem[25] = 32'h00000333; // ADD x6, x0, x0

    // ---------- Block 3 (2 stores) ----------
    mem[26] = 32'h000002B3; // ADD x5, x0, x0
    mem[27] = 32'h00000333; // ADD x6, x0, x0
    mem[28] = 32'h002083B3; // ADD x7, x1, x4
    mem[29] = 32'h00552023; // SW x5, 0(x10)
    mem[30] = 32'h006284B3; // ADD x9, x5, x6
    mem[31] = 32'h000305B3; // ADD x11, x6, x0
    mem[32] = 32'h00000433; // ADD x8, x0, x0
    mem[33] = 32'h000002B3; // ADD x5, x0, x0
    mem[34] = 32'h00000333; // ADD x6, x0, x0
    mem[35] = 32'h000002B3; // ADD x5, x0, x0
    mem[36] = 32'h00000333; // ADD x6, x0, x0
    mem[37] = 32'h00552023; // SW x5, 0(x10)
    mem[38] = 32'h00000333; // ADD x6, x0, x0
end
  
endmodule
