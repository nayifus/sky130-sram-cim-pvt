v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 20 -140 30 -20 {lab=#net1}
N -80 -80 -0 -80 {lab=#net2}
N -0 -80 0 -0 {lab=#net2}
N 0 -0 30 -0 {lab=#net2}
N -80 -30 -20 -30 {lab=#net3}
N -20 -30 -20 20 {lab=#net3}
N -20 20 30 20 {lab=#net3}
N -80 20 -80 50 {lab=#net4}
N -80 50 20 50 {lab=#net4}
N 20 50 20 60 {lab=#net4}
N 20 60 30 60 {lab=#net4}
N -80 80 30 80 {lab=#net5}
N -260 -80 -140 -80 {lab=0}
N -260 -80 -260 100 {lab=0}
N -260 -140 -40 -140 {lab=0}
N -260 -140 -260 -80 {lab=0}
N -260 -30 -140 -30 {lab=0}
N -260 20 -140 20 {lab=0}
N -260 80 -140 80 {lab=0}
N -190 130 -140 130 {lab=0}
N -190 50 -190 130 {lab=0}
N -260 50 -190 50 {lab=0}
N 330 -20 370 -20 {lab=out}
N -80 130 -30 130 {lab=#net6}
N -30 40 -30 130 {lab=#net6}
N -30 40 30 40 {lab=#net6}
C {sram8t.sym} 180 30 0 0 {name=x1}
C {code_shown.sym} 390 90 0 0 {name=s1 only_toplevel=false value=".lib /usr/local/share/pdk/sky130A/libs.tech/ngspice/sky130.lib.spice tt
.tran 100p 80n"}
C {vsource.sym} -10 -140 1 0 {name=V1 value=1.8 savecurrent=false}
C {vsource.sym} -110 -80 1 0 {name=V2 value="PULSE(0 1.8 15n 100p 100p 5n 40n)" savecurrent=false}
C {vsource.sym} -110 -30 1 0 {name=V3 value="PULSE(0 1.8 30n 100p 100p 10n 60n)" savecurrent=false}
C {vsource.sym} -110 20 1 0 {name=V4 value="PULSE(1.8 0 10n 100p 100p 10n 40n)" savecurrent=false}
C {vsource.sym} -110 80 1 0 {name=V5 value="PULSE(0 1.8 10n 100p 100p 10n 40n)" savecurrent=false}
C {gnd.sym} -260 100 0 0 {name=l1 lab=0}
C {vsource.sym} -110 130 1 0 {name=V6 value=1.8 savecurrent=false}
C {lab_wire.sym} 370 -20 0 0 {name=p1 sig_type=std_logic lab=out}
