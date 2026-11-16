v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {sram8t_bitcell.sym} 70 0 0 0 {name=x1}
C {code_shown.sym} -710 -520 0 0 {name=s1 only_toplevel=false value="
.lib /usr/local/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt


* case select: stored w=1 -> w_bl=1.8 w_blb=0 ; w=0 -> w_bl=0 w_blb=1.8 ; x = xin
.param w_bl=1.8 w_blb=0 xin=1.8

Vsup  VDD   0 1.8
* write the weight in 0-5 ns, then turn the write port off
Vwwl  WWL   0 PWL(0 1.8 4.9n 1.8 5n 0)
Vwbl  WBL   0 PWL(0 \{w_bl\}  4.9n \{w_bl\}  5n 0)
Vwblb WBLB  0 PWL(0 \{w_blb\} 4.9n \{w_blb\} 5n 0)
* reset 0-10 ns | compute 10-20 | share 20-30 | read 30-40
Vpre  PRE_B   0 PWL(0 0 9.9n 0 10n 1.8)
Vsh   SHARE   0 PWL(0 1.8 9.9n 1.8 10n 0 19.9n 0 20n 1.8)
Vshb  SHARE_B 0 PWL(0 0 9.9n 0 10n 1.8 19.9n 1.8 20n 0)
Vrwl  RWL     0 PWL(0 0 10.1n 0 10.2n \{xin\} 19.8n \{xin\} 19.9n 0)
* 7 other cells' worth of capacitance on the column, so one cell behaves like a column of 8
Ccl   CL 0 70f

.tran 0.05n 40n uic
.save v(x1.q) v(x1.qb) v(x1.net1) v(CL)
"}
C {lab_wire.sym} -80 -80 0 0 {name=p1 sig_type=std_logic lab=CL}
C {lab_wire.sym} -80 -60 0 0 {name=p2 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -80 -40 0 0 {name=p3 sig_type=std_logic lab=WWL}
C {lab_wire.sym} -80 -20 0 0 {name=p4 sig_type=std_logic lab=RWL}
C {lab_wire.sym} -80 0 0 0 {name=p5 sig_type=std_logic lab=WBL}
C {lab_wire.sym} -80 20 0 0 {name=p6 sig_type=std_logic lab=WBLB}
C {lab_wire.sym} -80 40 0 0 {name=p7 sig_type=std_logic lab=SHARE_B}
C {lab_wire.sym} -80 60 0 0 {name=p8 sig_type=std_logic lab=SHARE}
C {lab_wire.sym} -80 80 0 0 {name=p9 sig_type=std_logic lab=PRE_B}
