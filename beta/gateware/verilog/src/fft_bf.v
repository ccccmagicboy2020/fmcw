`ifndef _FFT_BF_V_
`define _FFT_BF_V_

`default_nettype none
`timescale 1ns/1ps

`include "fft_bfi.v"
`include "fft_bfii.v"

module fft_bf #(
   parameter WIDTH  = 25,
   parameter N      = 1024,
   parameter STAGE  = 0
) (
   input wire                     clk,
   input wire                     srst_n,
   input wire                     carry_in,
   output wire                    carry_out,
   input wire [$clog2(N)-1:0]     ctr_i,
   output reg [$clog2(N)-1:0]     ctr_o = {$clog2(N){1'b0}},
   input wire signed [WIDTH-1:0]  x_re_i,
   input wire signed [WIDTH-1:0]  x_im_i,
   output wire signed [WIDTH-1:0] z_re_o,
   output wire signed [WIDTH-1:0] z_im_o
);

   localparam STAGES = $clog2(N) / 2;

   wire                           sel1;
   wire                           sel2;
   reg [$clog2(N)-1:0]            ctrii = {$clog2(N){1'b0}};
   reg                            start_ctrii = 1'b0;
   reg                            start_ctr_o = 1'b0;

   wire signed [WIDTH-1:0]        z_re;
   wire signed [WIDTH-1:0]        z_im;

   assign sel1 = ctr_i[$clog2(N)-1-2*STAGE];
   assign sel2 = ctrii[$clog2(N)-2-2*STAGE];

   wire                          carry_int;

   fft_bfi #(
      .WIDTH         (WIDTH                   ),
      .SHIFT_REG_LEN (2**(2*(STAGES-STAGE)-1) )
   ) bfi (
      .clk       (clk       ),
      .srst_n    (srst_n    ),
      .carry_in  (carry_in  ),
      .carry_out (carry_int ),
      .sel_i     (sel1      ),
      .x_re_i    (x_re_i    ),
      .x_im_i    (x_im_i    ),
      .z_re_o    (z_re      ),
      .z_im_o    (z_im      )
   );

   fft_bfii #(
      .WIDTH         (WIDTH                   ),
      .SHIFT_REG_LEN (2**(2*(STAGES-STAGE)-2) )
   ) bfii (
      .clk       (clk       ),
      .srst_n    (srst_n    ),
      .carry_in  (carry_int ),
      .carry_out (carry_out ),
      .sel_i     (sel2      ),
      .tsel_i    (sel1      ),
      .x_re_i    (z_re      ),
      .x_im_i    (z_im      ),
      .z_re_o    (z_re_o    ),
      .z_im_o    (z_im_o    )
   );

   always @(posedge clk) begin
      if (sel1)                start_ctrii <= 1'b1;
      if (sel1 || start_ctrii) ctrii       <= ctrii + 1'b1;
      if (sel2)                start_ctr_o <= 1'b1;
      if (sel2 || start_ctr_o) ctr_o       <= ctr_o + 1'b1;
   end

endmodule
`endif