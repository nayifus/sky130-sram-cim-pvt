v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
C {sram_array.sym} -560 -590 0 0 {name=xarr}
C {lab_pin.sym} -710 -850 0 0 {name=p1 sig_type=std_logic lab=WWL1}
C {lab_pin.sym} -710 -830 0 0 {name=p2 sig_type=std_logic lab=RWL1}
C {lab_pin.sym} -710 -810 0 0 {name=p3 sig_type=std_logic lab=WBL3}
C {lab_pin.sym} -710 -790 0 0 {name=p4 sig_type=std_logic lab=WBL0}
C {lab_pin.sym} -710 -770 0 0 {name=p5 sig_type=std_logic lab=WBL2}
C {lab_pin.sym} -710 -750 0 0 {name=p6 sig_type=std_logic lab=WBL1}
C {lab_pin.sym} -710 -730 0 0 {name=p7 sig_type=std_logic lab=WBLB0}
C {lab_pin.sym} -710 -710 0 0 {name=p8 sig_type=std_logic lab=SHARE_B}
C {lab_pin.sym} -710 -690 0 0 {name=p9 sig_type=std_logic lab=WBLB2}
C {lab_pin.sym} -710 -670 0 0 {name=p10 sig_type=std_logic lab=WBLB1}
C {lab_pin.sym} -710 -650 0 0 {name=p11 sig_type=std_logic lab=WBLB3}
C {lab_pin.sym} -710 -630 0 0 {name=p12 sig_type=std_logic lab=SHARE}
C {lab_pin.sym} -710 -610 0 0 {name=p13 sig_type=std_logic lab=PRE_B}
C {lab_pin.sym} -710 -590 0 0 {name=p14 sig_type=std_logic lab=WWL2}
C {lab_pin.sym} -710 -570 0 0 {name=p15 sig_type=std_logic lab=RWL2}
C {lab_pin.sym} -710 -550 0 0 {name=p16 sig_type=std_logic lab=WWL3}
C {lab_pin.sym} -710 -530 0 0 {name=p17 sig_type=std_logic lab=RWL3}
C {lab_pin.sym} -710 -510 0 0 {name=p18 sig_type=std_logic lab=WWL4}
C {lab_pin.sym} -710 -490 0 0 {name=p19 sig_type=std_logic lab=RWL4}
C {lab_pin.sym} -710 -470 0 0 {name=p20 sig_type=std_logic lab=WWL5}
C {lab_pin.sym} -710 -450 0 0 {name=p21 sig_type=std_logic lab=RWL5}
C {lab_pin.sym} -710 -430 0 0 {name=p22 sig_type=std_logic lab=WWL6}
C {lab_pin.sym} -710 -410 0 0 {name=p23 sig_type=std_logic lab=RWL6}
C {lab_pin.sym} -710 -390 0 0 {name=p24 sig_type=std_logic lab=WWL7}
C {lab_pin.sym} -710 -370 0 0 {name=p25 sig_type=std_logic lab=RWL7}
C {lab_pin.sym} -710 -350 0 0 {name=p26 sig_type=std_logic lab=WWL8}
C {lab_pin.sym} -710 -330 0 0 {name=p27 sig_type=std_logic lab=RWL8}
C {lab_pin.sym} -410 -850 2 0 {name=p28 sig_type=std_logic lab=CL1}
C {lab_pin.sym} -410 -830 2 0 {name=p29 sig_type=std_logic lab=CL2}
C {lab_pin.sym} -410 -810 2 0 {name=p30 sig_type=std_logic lab=CL3}
C {lab_pin.sym} -410 -790 2 0 {name=p31 sig_type=std_logic lab=CL0}
C {lab_pin.sym} -410 -770 2 0 {name=p32 sig_type=std_logic lab=VDD}
C {code_shown.sym} -220 -880 0 0 {name=s1 only_toplevel=false value="
.lib /usr/local/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice ss

.param vdd_v=1.8
.param tmp=27
.temp \{tmp\}
.param csig=0
.param td=0.5e-9
.param ts=\{10.5e-9+td\}
.param pat=255
.param in1=\{floor(pat/1)-2*floor(pat/2)\} in2=\{floor(pat/2)-2*floor(pat/4)\}
.param in3=\{floor(pat/4)-2*floor(pat/8)\} in4=\{floor(pat/8)-2*floor(pat/16)\}
.param in5=\{floor(pat/16)-2*floor(pat/32)\} in6=\{floor(pat/32)-2*floor(pat/64)\}
.param in7=\{floor(pat/64)-2*floor(pat/128)\} in8=\{floor(pat/128)-2*floor(pat/256)\}

* weights w<row><col>, rows 1-8, cols 0-3
.param w10=1 w20=1 w30=1 w40=1 w50=1 w60=1 w70=1 w80=1
.param w11=1 w21=1 w31=1 w41=1 w51=0 w61=0 w71=0 w81=0
.param w12=1 w22=0 w32=1 w42=0 w52=1 w62=0 w72=1 w82=0
.param w13=0 w23=1 w33=1 w43=1 w53=1 w63=1 w73=0 w83=0

.ic v(xarr.xc0.x1.q)=\{w10*vdd_v\} v(xarr.xc0.x1.qb)=\{(1-w10)*vdd_v\}
.ic v(xarr.xc0.x2.q)=\{w20*vdd_v\} v(xarr.xc0.x2.qb)=\{(1-w20)*vdd_v\}
.ic v(xarr.xc0.x3.q)=\{w30*vdd_v\} v(xarr.xc0.x3.qb)=\{(1-w30)*vdd_v\}
.ic v(xarr.xc0.x4.q)=\{w40*vdd_v\} v(xarr.xc0.x4.qb)=\{(1-w40)*vdd_v\}
.ic v(xarr.xc0.x5.q)=\{w50*vdd_v\} v(xarr.xc0.x5.qb)=\{(1-w50)*vdd_v\}
.ic v(xarr.xc0.x6.q)=\{w60*vdd_v\} v(xarr.xc0.x6.qb)=\{(1-w60)*vdd_v\}
.ic v(xarr.xc0.x7.q)=\{w70*vdd_v\} v(xarr.xc0.x7.qb)=\{(1-w70)*vdd_v\}
.ic v(xarr.xc0.x8.q)=\{w80*vdd_v\} v(xarr.xc0.x8.qb)=\{(1-w80)*vdd_v\}
.ic v(xarr.xc1.x1.q)=\{w11*vdd_v\} v(xarr.xc1.x1.qb)=\{(1-w11)*vdd_v\}
.ic v(xarr.xc1.x2.q)=\{w21*vdd_v\} v(xarr.xc1.x2.qb)=\{(1-w21)*vdd_v\}
.ic v(xarr.xc1.x3.q)=\{w31*vdd_v\} v(xarr.xc1.x3.qb)=\{(1-w31)*vdd_v\}
.ic v(xarr.xc1.x4.q)=\{w41*vdd_v\} v(xarr.xc1.x4.qb)=\{(1-w41)*vdd_v\}
.ic v(xarr.xc1.x5.q)=\{w51*vdd_v\} v(xarr.xc1.x5.qb)=\{(1-w51)*vdd_v\}
.ic v(xarr.xc1.x6.q)=\{w61*vdd_v\} v(xarr.xc1.x6.qb)=\{(1-w61)*vdd_v\}
.ic v(xarr.xc1.x7.q)=\{w71*vdd_v\} v(xarr.xc1.x7.qb)=\{(1-w71)*vdd_v\}
.ic v(xarr.xc1.x8.q)=\{w81*vdd_v\} v(xarr.xc1.x8.qb)=\{(1-w81)*vdd_v\}
.ic v(xarr.xc2.x1.q)=\{w12*vdd_v\} v(xarr.xc2.x1.qb)=\{(1-w12)*vdd_v\}
.ic v(xarr.xc2.x2.q)=\{w22*vdd_v\} v(xarr.xc2.x2.qb)=\{(1-w22)*vdd_v\}
.ic v(xarr.xc2.x3.q)=\{w32*vdd_v\} v(xarr.xc2.x3.qb)=\{(1-w32)*vdd_v\}
.ic v(xarr.xc2.x4.q)=\{w42*vdd_v\} v(xarr.xc2.x4.qb)=\{(1-w42)*vdd_v\}
.ic v(xarr.xc2.x5.q)=\{w52*vdd_v\} v(xarr.xc2.x5.qb)=\{(1-w52)*vdd_v\}
.ic v(xarr.xc2.x6.q)=\{w62*vdd_v\} v(xarr.xc2.x6.qb)=\{(1-w62)*vdd_v\}
.ic v(xarr.xc2.x7.q)=\{w72*vdd_v\} v(xarr.xc2.x7.qb)=\{(1-w72)*vdd_v\}
.ic v(xarr.xc2.x8.q)=\{w82*vdd_v\} v(xarr.xc2.x8.qb)=\{(1-w82)*vdd_v\}
.ic v(xarr.xc3.x1.q)=\{w13*vdd_v\} v(xarr.xc3.x1.qb)=\{(1-w13)*vdd_v\}
.ic v(xarr.xc3.x2.q)=\{w23*vdd_v\} v(xarr.xc3.x2.qb)=\{(1-w23)*vdd_v\}
.ic v(xarr.xc3.x3.q)=\{w33*vdd_v\} v(xarr.xc3.x3.qb)=\{(1-w33)*vdd_v\}
.ic v(xarr.xc3.x4.q)=\{w43*vdd_v\} v(xarr.xc3.x4.qb)=\{(1-w43)*vdd_v\}
.ic v(xarr.xc3.x5.q)=\{w53*vdd_v\} v(xarr.xc3.x5.qb)=\{(1-w53)*vdd_v\}
.ic v(xarr.xc3.x6.q)=\{w63*vdd_v\} v(xarr.xc3.x6.qb)=\{(1-w63)*vdd_v\}
.ic v(xarr.xc3.x7.q)=\{w73*vdd_v\} v(xarr.xc3.x7.qb)=\{(1-w73)*vdd_v\}
.ic v(xarr.xc3.x8.q)=\{w83*vdd_v\} v(xarr.xc3.x8.qb)=\{(1-w83)*vdd_v\}

Vsup VDD 0 \{vdd_v\}
Vwbl0 WBL0 0 0
Vwblb0 WBLB0 0 0
Vwbl1 WBL1 0 0
Vwblb1 WBLB1 0 0
Vwbl2 WBL2 0 0
Vwblb2 WBLB2 0 0
Vwbl3 WBL3 0 0
Vwblb3 WBLB3 0 0
Vww1 WWL1 0 0
Vww2 WWL2 0 0
Vww3 WWL3 0 0
Vww4 WWL4 0 0
Vww5 WWL5 0 0
Vww6 WWL6 0 0
Vww7 WWL7 0 0
Vww8 WWL8 0 0

Vpre PRE_B 0 PWL(0 0 9.9n 0 10n \{vdd_v\})
Vsh SHARE 0 PWL(0 \{vdd_v\} 9.9n \{vdd_v\} 10n 0 \{ts-0.1e-9\} 0 \{ts\} \{vdd_v\})
Vshb SHARE_B 0 PWL(0 0 9.9n 0 10n \{vdd_v\} \{ts-0.1e-9\} \{vdd_v\} \{ts\} 0)

Vr1 RWL1 0 PWL(0 0 10.1n 0 10.2n \{in1*vdd_v\} \{10.2e-9+td\} \{in1*vdd_v\} \{10.3e-9+td\} 0)
Vr2 RWL2 0 PWL(0 0 10.1n 0 10.2n \{in2*vdd_v\} \{10.2e-9+td\} \{in2*vdd_v\} \{10.3e-9+td\} 0)
Vr3 RWL3 0 PWL(0 0 10.1n 0 10.2n \{in3*vdd_v\} \{10.2e-9+td\} \{in3*vdd_v\} \{10.3e-9+td\} 0)
Vr4 RWL4 0 PWL(0 0 10.1n 0 10.2n \{in4*vdd_v\} \{10.2e-9+td\} \{in4*vdd_v\} \{10.3e-9+td\} 0)
Vr5 RWL5 0 PWL(0 0 10.1n 0 10.2n \{in5*vdd_v\} \{10.2e-9+td\} \{in5*vdd_v\} \{10.3e-9+td\} 0)
Vr6 RWL6 0 PWL(0 0 10.1n 0 10.2n \{in6*vdd_v\} \{10.2e-9+td\} \{in6*vdd_v\} \{10.3e-9+td\} 0)
Vr7 RWL7 0 PWL(0 0 10.1n 0 10.2n \{in7*vdd_v\} \{10.2e-9+td\} \{in7*vdd_v\} \{10.3e-9+td\} 0)
Vr8 RWL8 0 PWL(0 0 10.1n 0 10.2n \{in8*vdd_v\} \{10.2e-9+td\} \{in8*vdd_v\} \{10.3e-9+td\} 0)

.tran 0.02n 45n uic
.save v(CL0) v(CL1) v(CL2) v(CL3)

.control
alterparam vdd_v=1.62
alterparam tmp=-40
foreach pv 85 255
  alterparam pat=$pv
  reset
  run
  meas tran a find v(cl0) at=13n
  meas tran b find v(cl0) at=15n
  meas tran c find v(cl0) at=20n
  meas tran d find v(cl0) at=25n
  meas tran e find v(cl0) at=30n
  meas tran f find v(cl0) at=40n
  echo $pv $&a $&b $&c $&d $&e $&f >> settle_test.csv
end
.endc"}
