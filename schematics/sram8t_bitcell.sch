v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 10 140 10 230 {lab=qb}
N 250 140 250 230 {lab=q}
N 10 40 250 40 {lab=VDD}
N 250 50 250 80 {lab=VDD}
N -210 190 10 190 {lab=qb}
N 180 110 210 110 {lab=qb}
N 180 110 180 260 {lab=qb}
N 180 260 210 260 {lab=qb}
N 50 110 70 110 {lab=q}
N 70 110 70 260 {lab=q}
N 50 260 70 260 {lab=q}
N 10 150 180 150 {lab=qb}
N 70 170 250 170 {lab=q}
N 250 180 410 180 {lab=q}
N 250 210 540 210 {lab=q}
N 580 140 580 180 {lab=output}
N 580 140 700 140 {lab=output}
N 250 290 250 350 {lab=0}
N 250 350 580 350 {lab=0}
N 580 240 580 350 {lab=0}
N -240 10 -240 150 {lab=WWL}
N -240 10 440 10 {lab=WWL}
N 440 10 440 140 {lab=WWL}
N -320 190 -270 190 {lab=WBLB}
N -320 10 -320 190 {lab=WBLB}
N 10 290 10 350 {lab=0}
N 10 350 250 350 {lab=0}
N -240 190 -240 350 {lab=0}
N -240 350 10 350 {lab=0}
N 580 210 650 210 {lab=0}
N 650 210 650 290 {lab=0}
N 580 290 650 290 {lab=0}
N 760 140 820 140 {lab=#net1}
N 730 -10 730 100 {lab=RWL}
N 580 -10 580 140 {lab=output}
N 250 40 250 50 {lab=VDD}
N 10 40 10 80 {lab=VDD}
N -20 110 10 110 {lab=VDD}
N -20 60 -20 110 {lab=VDD}
N -20 60 10 60 {lab=VDD}
N 250 110 310 110 {lab=VDD}
N 310 60 310 110 {lab=VDD}
N 250 60 310 60 {lab=VDD}
N -40 260 10 260 {lab=0}
N -40 260 -40 310 {lab=0}
N -40 310 10 310 {lab=0}
N 250 260 320 260 {lab=0}
N 320 260 320 310 {lab=0}
N 250 310 320 310 {lab=0}
N 470 180 500 180 {lab=WBLB}
N 500 -10 500 180 {lab=WBLB}
N -240 -30 -240 10 {lab=WWL}
N 120 -40 120 40 {lab=VDD}
N 730 140 730 350 {lab=0}
N 580 350 730 350 {lab=0}
N 440 180 440 350 {lab=0}
N 870 140 880 140 {lab=#net1}
N 880 140 890 140 {lab=#net1}
N 1120 140 1130 140 {lab=#net1}
N 1130 140 1140 140 {lab=#net1}
N 1140 140 1150 140 {lab=#net1}
N 1150 140 1160 140 {lab=#net1}
N 1160 140 1170 140 {lab=#net1}
N 1170 140 1180 140 {lab=#net1}
N 1180 140 1190 140 {lab=#net1}
N 1230 170 1260 170 {lab=PRE_B}
N 1190 200 1190 260 {lab=VDD}
N 1140 170 1190 170 {lab=VDD}
N 1140 170 1140 220 {lab=VDD}
N 1140 220 1190 220 {lab=VDD}
N 820 140 870 140 {lab=#net1}
N 890 140 960 140 {lab=#net1}
N 960 140 1120 140 {lab=#net1}
N 930 50 930 140 {lab=#net1}
N 930 -40 930 -10 {lab=CL}
N 870 20 890 20 {lab=SHARE}
N 930 20 980 20 {lab=0}
N 980 20 980 70 {lab=0}
N 1080 50 1080 140 {lab=#net1}
N 930 -110 930 -40 {lab=CL}
N 1080 -80 1080 -10 {lab=CL}
N 930 -80 1080 -80 {lab=CL}
N 1120 20 1130 20 {lab=SHARE_B}
N 1030 20 1080 20 {lab=VDD}
N 1030 20 1030 80 {lab=VDD}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 30 260 2 0 {name=M1
W=1
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 30 110 2 0 {name=M2
W=1
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 230 110 0 0 {name=M3
W=1
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 230 260 0 0 {name=M4
W=1
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -240 170 1 0 {name=M5
W=1
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 440 160 1 0 {name=M6
W=1
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 560 210 0 0 {name=M7
W=1
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 730 120 1 0 {name=M8
W=1
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {gnd.sym} 150 350 0 0 {name=l1 lab=0}
C {ipin.sym} -320 10 1 0 {name=p1 lab=WBLB}
C {ipin.sym} 500 -10 1 0 {name=p2 lab=WBL}
C {ipin.sym} 730 -10 1 0 {name=p3 lab=RWL}
C {ipin.sym} -240 -30 1 0 {name=p6 lab=WWL}
C {lab_wire.sym} -110 190 0 0 {name=p14 sig_type=std_logic lab=qb}
C {lab_wire.sym} 330 180 0 0 {name=p15 sig_type=std_logic lab=q}
C {ipin.sym} 120 -40 1 0 {name=p7 lab=VDD}
C {lab_wire.sym} 580 -10 0 0 {name=p5 sig_type=std_logic lab=output}
C {capa.sym} 820 170 0 0 {name=C1
m=1
value=10f
footprint=1206
device="ceramic capacitor"}
C {/home/blazeinkid/eda_sources/open_pdks/sky130/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 910 20 0 0 {name=M9
W=1
L=0.15
nf=1 
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=nfet_01v8
spiceprefix=X
}
C {/home/blazeinkid/eda_sources/open_pdks/sky130/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1210 170 2 0 {name=M10
W=1
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {/home/blazeinkid/eda_sources/open_pdks/sky130/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 1100 20 2 0 {name=M11
W=1
L=0.15
nf=1
mult=1
ad="expr('int((@nf + 1)/2) * @W / @nf * 0.29')"
pd="expr('2*int((@nf + 1)/2) * (@W / @nf + 0.29)')"
as="expr('int((@nf + 2)/2) * @W / @nf * 0.29')"
ps="expr('2*int((@nf + 2)/2) * (@W / @nf + 0.29)')"
nrd="expr('0.29 / @W ')" nrs="expr('0.29 / @W ')"
sa=0 sb=0 sd=0
model=pfet_01v8
spiceprefix=X
}
C {ipin.sym} 1260 170 1 0 {name=p8 lab=PRE_B}
C {lab_wire.sym} 1190 260 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {gnd.sym} 820 200 0 0 {name=l2 lab=0}
C {ipin.sym} 930 -110 1 0 {name=p4 lab=CL}
C {ipin.sym} 870 20 0 0 {name=p10 lab=SHARE}
C {gnd.sym} 980 70 0 0 {name=l3 lab=0}
C {ipin.sym} 1130 20 2 0 {name=p11 lab=SHARE_B}
C {lab_wire.sym} 1030 80 2 0 {name=p12 sig_type=std_logic lab=VDD}
