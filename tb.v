module tb();

    reg clk=0, rst;
    wire [31:0] cycle_count, instr_retired;
    
    always begin
        clk = ~clk;
        #50;
    end

    initial begin
        rst <= 1'b0;
        #100;
        rst <= 1'b1;
        #2000;

        $display("\n---------------------------------------------");
        $display("   Simulation Finished || Performance Report  ");
        $display("---------------------------------------------");
        $display("Total Cycles      : %0d", dut.cycle_count);
        $display("Instructions Ret. : %0d", dut.instr_retired);
        if (dut.instr_retired != 0)
            $display("Average CPI       : %f",
                     $itor(dut.cycle_count) / $itor(dut.instr_retired));
        else
            $display("Average CPI       : N/A (no instructions retired)");
        $display("---------------------------------------------\n");


        $finish;    
    end

    initial begin
        $dumpfile("risc.vcd");
        $dumpvars(0);
    end

    Pipeline_top dut (.clk(clk), .rst(rst), .instr_retired(instr_retired), .cycle_count(cycle_count));

endmodule
