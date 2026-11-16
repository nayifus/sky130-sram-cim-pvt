v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {sram8t_bitcell.sym} 80 30 0 0 {name=x1}
C {lab_wire.sym} -70 -50 0 0 {name=p1 sig_type=std_logic lab=CL}
C {lab_wire.sym} -70 -30 0 0 {name=p2 sig_type=std_logic lab=VDD}
C {lab_wire.sym} -70 -10 0 0 {name=p3 sig_type=std_logic lab=WWL}
C {lab_wire.sym} -70 10 0 0 {name=p4 sig_type=std_logic lab=RWL1}
C {lab_wire.sym} -70 30 0 0 {name=p5 sig_type=std_logic lab=WBL}
C {lab_wire.sym} -70 50 0 0 {name=p6 sig_type=std_logic lab=WBLB}
C {lab_wire.sym} -70 70 0 0 {name=p7 sig_type=std_logic lab=SHARE_B}
C {lab_wire.sym} -70 90 0 0 {name=p8 sig_type=std_logic lab=SHARE}
C {lab_wire.sym} -70 110 0 0 {name=p9 sig_type=std_logic lab=PRE_B}
C {code_shown.sym} -700 -890 0 0 {name=s1 only_toplevel=false value=".lib /usr/local/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice fs

.param vdd_v=1.8
.param td=9.6e-9
.param t_r=\{10.2e-9+2e-11\} t_f=\{10.2e-9+td\} t_e=\{10.2e-9+td+2e-11\}
.param kk=0
.param w1=\{kk>=1\} w2=\{kk>=2\} w3=\{kk>=3\} w4=\{kk>=4\} w5=\{kk>=5\} w6=\{kk>=6\} w7=\{kk>=7\} w8=\{kk>=8\}
.param in1=1 in2=1 in3=1 in4=1 in5=1 in6=1 in7=1 in8=1

x2 CL VDD WWL RWL2 WBL WBLB SHARE_B SHARE PRE_B sram8t_bitcell
x3 CL VDD WWL RWL3 WBL WBLB SHARE_B SHARE PRE_B sram8t_bitcell
x4 CL VDD WWL RWL4 WBL WBLB SHARE_B SHARE PRE_B sram8t_bitcell
x5 CL VDD WWL RWL5 WBL WBLB SHARE_B SHARE PRE_B sram8t_bitcell
x6 CL VDD WWL RWL6 WBL WBLB SHARE_B SHARE PRE_B sram8t_bitcell
x7 CL VDD WWL RWL7 WBL WBLB SHARE_B SHARE PRE_B sram8t_bitcell
x8 CL VDD WWL RWL8 WBL WBLB SHARE_B SHARE PRE_B sram8t_bitcell

.ic v(x1.q)=\{w1*vdd_v\} v(x1.qb)=\{(1-w1)*vdd_v\}
.ic v(x2.q)=\{w2*vdd_v\} v(x2.qb)=\{(1-w2)*vdd_v\}
.ic v(x3.q)=\{w3*vdd_v\} v(x3.qb)=\{(1-w3)*vdd_v\}
.ic v(x4.q)=\{w4*vdd_v\} v(x4.qb)=\{(1-w4)*vdd_v\}
.ic v(x5.q)=\{w5*vdd_v\} v(x5.qb)=\{(1-w5)*vdd_v\}
.ic v(x6.q)=\{w6*vdd_v\} v(x6.qb)=\{(1-w6)*vdd_v\}
.ic v(x7.q)=\{w7*vdd_v\} v(x7.qb)=\{(1-w7)*vdd_v\}
.ic v(x8.q)=\{w8*vdd_v\} v(x8.qb)=\{(1-w8)*vdd_v\}

Vsup  VDD   0 \{vdd_v\}
Vwwl  WWL   0 0
Vwbl  WBL   0 0
Vwblb WBLB  0 0
Vpre  PRE_B   0 PWL(0 0 9.9n 0 10n \{vdd_v\})
Vsh   SHARE   0 PWL(0 \{vdd_v\} 9.9n \{vdd_v\} 10n 0 19.9n 0 20n \{vdd_v\})
Vshb  SHARE_B 0 PWL(0 0 9.9n 0 10n \{vdd_v\} 19.9n \{vdd_v\} 20n 0)
Vr1 RWL1 0 PWL(0 0 10.2n 0 \{t_r\} \{in1*vdd_v\} \{t_f\} \{in1*vdd_v\} \{t_e\} 0)
Vr2 RWL2 0 PWL(0 0 10.2n 0 \{t_r\} \{in2*vdd_v\} \{t_f\} \{in2*vdd_v\} \{t_e\} 0)
Vr3 RWL3 0 PWL(0 0 10.2n 0 \{t_r\} \{in3*vdd_v\} \{t_f\} \{in3*vdd_v\} \{t_e\} 0)
Vr4 RWL4 0 PWL(0 0 10.2n 0 \{t_r\} \{in4*vdd_v\} \{t_f\} \{in4*vdd_v\} \{t_e\} 0)
Vr5 RWL5 0 PWL(0 0 10.2n 0 \{t_r\} \{in5*vdd_v\} \{t_f\} \{in5*vdd_v\} \{t_e\} 0)
Vr6 RWL6 0 PWL(0 0 10.2n 0 \{t_r\} \{in6*vdd_v\} \{t_f\} \{in6*vdd_v\} \{t_e\} 0)
Vr7 RWL7 0 PWL(0 0 10.2n 0 \{t_r\} \{in7*vdd_v\} \{t_f\} \{in7*vdd_v\} \{t_e\} 0)
Vr8 RWL8 0 PWL(0 0 10.2n 0 \{t_r\} \{in8*vdd_v\} \{t_f\} \{in8*vdd_v\} \{t_e\} 0)

.tran 0.01n 40n uic
.save v(CL)

.control
set cname = fs
foreach cc 1 2 3
  if $cc = 1
    set vv = 1.62
    set tv = 125
  end
  if $cc = 2
    set vv = 1.8
    set tv = 27
  end
  if $cc = 3
    set vv = 1.98
    set tv = -40
  end
  foreach tdv 9.6e-9 2e-9 1e-9 5e-10 3e-10 2e-10 1.5e-10 1e-10 7e-11
    foreach kv 0 8
      alterparam kk = $kv
      alterparam vdd_v = $vv
      alterparam td = $tdv
      set temp = $tv
      reset
      run
      meas tran vcl find v(cl) at=35n
      echo $cname $vv $tv $tdv $kv $&vcl >> td_results.csv
    end
  end
  echo finished $cname $vv $tv
end
.endc"}
