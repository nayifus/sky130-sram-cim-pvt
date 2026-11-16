v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {column8t.sym} 10 -20 0 0 {name=xcol}
C {lab_pin.sym} -140 -220 0 0 {name=p1 sig_type=std_logic lab=WWL1
}
C {lab_pin.sym} -140 -200 0 0 {name=p2 sig_type=std_logic lab=RWL1}
C {lab_pin.sym} -140 -180 0 0 {name=p3 sig_type=std_logic lab=WBL}
C {lab_pin.sym} -140 -160 0 0 {name=p4 sig_type=std_logic lab=WBLB}
C {lab_pin.sym} -140 -140 0 0 {name=p5 sig_type=std_logic lab=SHARE_B}
C {lab_pin.sym} -140 -120 0 0 {name=p6 sig_type=std_logic lab=SHARE}
C {lab_pin.sym} -140 -100 0 0 {name=p7 sig_type=std_logic lab=PRE_B}
C {lab_pin.sym} -140 -80 0 0 {name=p8 sig_type=std_logic lab=WWL2}
C {lab_pin.sym} -140 -60 0 0 {name=p9 sig_type=std_logic lab=RWL2}
C {lab_pin.sym} -140 -40 0 0 {name=p10 sig_type=std_logic lab=WWL3}
C {lab_pin.sym} -140 -20 0 0 {name=p11 sig_type=std_logic lab=RWL3}
C {lab_pin.sym} -140 0 0 0 {name=p12 sig_type=std_logic lab=WWL4}
C {lab_pin.sym} -140 20 0 0 {name=p13 sig_type=std_logic lab=RWL4}
C {lab_pin.sym} -140 40 0 0 {name=p14 sig_type=std_logic lab=WWL5}
C {lab_pin.sym} -140 60 0 0 {name=p15 sig_type=std_logic lab=RWL5}
C {lab_pin.sym} -140 80 0 0 {name=p16 sig_type=std_logic lab=WWL6}
C {lab_pin.sym} -140 100 0 0 {name=p17 sig_type=std_logic lab=RWL6}
C {lab_pin.sym} -140 120 0 0 {name=p18 sig_type=std_logic lab=WWL7}
C {lab_pin.sym} -140 140 0 0 {name=p19 sig_type=std_logic lab=RWL7}
C {lab_pin.sym} -140 160 0 0 {name=p20 sig_type=std_logic lab=WWL8}
C {lab_pin.sym} -140 180 0 0 {name=p21 sig_type=std_logic lab=RWL8}
C {lab_pin.sym} 160 -220 2 0 {name=p22 sig_type=std_logic lab=CL}
C {lab_pin.sym} 160 -200 2 0 {name=p23 sig_type=std_logic lab=VDD}
C {code_shown.sym} 350 -370 0 0 {name=s1 only_toplevel=false value="
.lib /usr/local/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice fs

.param vdd_v=1.8
.param tmp=27
.temp \{tmp\}
.param td=0.5e-9
.param kk=3
.param in1=1 in2=1 in3=1 in4=1 in5=1 in6=1 in7=1 in8=1
.param w1=\{kk>=1\} w2=\{kk>=2\} w3=\{kk>=3\} w4=\{kk>=4\} w5=\{kk>=5\} w6=\{kk>=6\} w7=\{kk>=7\} w8=\{kk>=8\}

.ic v(xcol.x1.q)=\{w1*vdd_v\} v(xcol.x1.qb)=\{(1-w1)*vdd_v\}
.ic v(xcol.x2.q)=\{w2*vdd_v\} v(xcol.x2.qb)=\{(1-w2)*vdd_v\}
.ic v(xcol.x3.q)=\{w3*vdd_v\} v(xcol.x3.qb)=\{(1-w3)*vdd_v\}
.ic v(xcol.x4.q)=\{w4*vdd_v\} v(xcol.x4.qb)=\{(1-w4)*vdd_v\}
.ic v(xcol.x5.q)=\{w5*vdd_v\} v(xcol.x5.qb)=\{(1-w5)*vdd_v\}
.ic v(xcol.x6.q)=\{w6*vdd_v\} v(xcol.x6.qb)=\{(1-w6)*vdd_v\}
.ic v(xcol.x7.q)=\{w7*vdd_v\} v(xcol.x7.qb)=\{(1-w7)*vdd_v\}
.ic v(xcol.x8.q)=\{w8*vdd_v\} v(xcol.x8.qb)=\{(1-w8)*vdd_v\}

Vsup VDD 0 \{vdd_v\}
Vwbl WBL 0 0
Vwblb WBLB 0 0
Vww1 WWL1 0 0
Vww2 WWL2 0 0
Vww3 WWL3 0 0
Vww4 WWL4 0 0
Vww5 WWL5 0 0
Vww6 WWL6 0 0
Vww7 WWL7 0 0
Vww8 WWL8 0 0
Vpre PRE_B 0 PWL(0 0 9.9n 0 10n \{vdd_v\})
Vsh SHARE 0 PWL(0 \{vdd_v\} 9.9n \{vdd_v\} 10n 0 10.9n 0 11n \{vdd_v\})
Vshb SHARE_B 0 PWL(0 0 9.9n 0 10n \{vdd_v\} 10.9n \{vdd_v\} 11n 0)
Vr1 RWL1 0 PWL(0 0 10.1n 0 10.2n \{in1*vdd_v\} \{10.2e-9+td\} \{in1*vdd_v\} \{10.3e-9+td\} 0)
Vr2 RWL2 0 PWL(0 0 10.1n 0 10.2n \{in2*vdd_v\} \{10.2e-9+td\} \{in2*vdd_v\} \{10.3e-9+td\} 0)
Vr3 RWL3 0 PWL(0 0 10.1n 0 10.2n \{in3*vdd_v\} \{10.2e-9+td\} \{in3*vdd_v\} \{10.3e-9+td\} 0)
Vr4 RWL4 0 PWL(0 0 10.1n 0 10.2n \{in4*vdd_v\} \{10.2e-9+td\} \{in4*vdd_v\} \{10.3e-9+td\} 0)
Vr5 RWL5 0 PWL(0 0 10.1n 0 10.2n \{in5*vdd_v\} \{10.2e-9+td\} \{in5*vdd_v\} \{10.3e-9+td\} 0)
Vr6 RWL6 0 PWL(0 0 10.1n 0 10.2n \{in6*vdd_v\} \{10.2e-9+td\} \{in6*vdd_v\} \{10.3e-9+td\} 0)
Vr7 RWL7 0 PWL(0 0 10.1n 0 10.2n \{in7*vdd_v\} \{10.2e-9+td\} \{in7*vdd_v\} \{10.3e-9+td\} 0)
Vr8 RWL8 0 PWL(0 0 10.1n 0 10.2n \{in8*vdd_v\} \{10.2e-9+td\} \{in8*vdd_v\} \{10.3e-9+td\} 0)

.tran 0.05n 20n uic
.save v(CL)

.control
set cname = fs
foreach vv 1.62 1.8 1.98
  foreach tv -40 27 125
    foreach kv 0 1 2 3 4 5 6 7 8
      alterparam vdd_v=$vv
      alterparam tmp=$tv
      alterparam kk=$kv
      reset
      run
      meas tran vcl find v(cl) at=13n
      echo $cname $vv $tv $kv $&vcl >> pvt_results.csv
    end
  end
end
.endc"}
