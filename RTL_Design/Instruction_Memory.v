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
/*  initial begin
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
  
endmodule
