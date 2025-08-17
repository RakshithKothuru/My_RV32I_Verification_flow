module load_hazard_unit(
    input [1:0] ResultSrcE,      // 01 if EX-stage instruction is a load (Result from memory)
    input [4:0] RD_E,      // destination register in EX stage
    input [31:0] InstrD,   // IF/ID instruction word (to read rs1/rs2)
    output pc_write,
    output stallF_load_hazard,
    output flushD_load_hazard
);

    wire load_in_ex;
    assign load_in_ex = (ResultSrcE == 2'b01); // in this design ResultSrc==01 for loads

    wire [4:0] rs1_d = InstrD[19:15];
    wire [4:0] rs2_d = InstrD[24:20];

    wire hazard;
    assign hazard = load_in_ex & (RD_E != 5'h00) & ((RD_E == rs1_d) | (RD_E == rs2_d));

    assign pc_write = ~hazard;
    assign stallF_load_hazard = hazard;
    assign flushD_load_hazard = hazard; // turns ID/EX into NOP for one cycle

endmodule
