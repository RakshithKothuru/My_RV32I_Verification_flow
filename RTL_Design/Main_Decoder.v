module Main_Decoder(Op,RegWrite,ImmSrc,ALUSrc,MemWrite,ResultSrc,Branch,ALUOp, Jump);
    input [6:0]Op;
    output RegWrite,ALUSrc,MemWrite,Branch, Jump;
    output [1:0] ALUOp,ResultSrc;
    output [2:0] ImmSrc;

    assign RegWrite = (Op == 7'b0000011 | Op == 7'b0110011 | Op == 7'b0010011 | Op == 7'b1101111) ? 1'b1 : 1'b0 ;

    assign ImmSrc = (Op == 7'b0000011) ? 3'b000 :  // LW
                    (Op == 7'b0100011) ? 3'b001 :  // SW
                    (Op == 7'b1100011) ? 3'b010 :  // B-type
                    (Op == 7'b1101111) ? 3'b011 :  // J-type
                    (Op == 7'b0010011) ? 3'b100 : 3'b101; // I-type
                                            

    assign ALUSrc = (Op == 7'b0000011 | Op == 7'b0100011 | Op == 7'b0010011) ? 1'b1 : 1'b0 ;

    assign MemWrite = (Op == 7'b0100011) ? 1'b1 : 1'b0 ;

    assign ResultSrc = (Op == 7'b0000011) ? 2'b01 :  // LW
                       (Op == 7'b1101111) ? 2'b10 :  // J-type
                                            2'b00 ;

    assign Branch = (Op == 7'b1100011) ? 1'b1 : 1'b0 ;

    assign ALUOp = (Op == 7'b0110011) ? 2'b10 :
                   (Op == 7'b1100011) ? 2'b01 :
                                        2'b00 ;

    assign Jump = (Op == 7'b1101111) ? 1'b1 : 1'b0;                                

endmodule
