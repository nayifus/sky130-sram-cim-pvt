v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N -380 -450 -380 -360 {lab=qb}
N -140 -450 -140 -360 {lab=q}
N -380 -550 -140 -550 {lab=VDD}
N -140 -540 -140 -510 {lab=VDD}
N -600 -400 -380 -400 {lab=qb}
N -210 -480 -180 -480 {lab=qb}
N -210 -480 -210 -330 {lab=qb}
N -210 -330 -180 -330 {lab=qb}
N -340 -480 -320 -480 {lab=q}
N -320 -480 -320 -330 {lab=q}
N -340 -330 -320 -330 {lab=q}
N -380 -440 -210 -440 {lab=qb}
N -320 -420 -140 -420 {lab=q}
N -140 -410 20 -410 {lab=q}
N -140 -380 150 -380 {lab=q}
N 190 -450 190 -410 {lab=output}
N 190 -450 310 -450 {lab=output}
N -140 -300 -140 -240 {lab=0}
N -140 -240 190 -240 {lab=0}
N 190 -350 190 -240 {lab=0}
N -630 -580 -630 -440 {lab=WWL}
N -630 -580 50 -580 {lab=WWL}
N 50 -580 50 -450 {lab=WWL}
N -710 -400 -660 -400 {lab=WBLB}
N -710 -580 -710 -400 {lab=WBLB}
N -380 -300 -380 -240 {lab=0}
N -380 -240 -140 -240 {lab=0}
N -630 -400 -630 -240 {lab=0}
N -630 -240 -380 -240 {lab=0}
N 190 -380 260 -380 {lab=0}
N 260 -380 260 -300 {lab=0}
N 190 -300 260 -300 {lab=0}
N 370 -450 430 -450 {lab=#net1}
N 340 -600 340 -490 {lab=RWL}
N 190 -600 190 -450 {lab=output}
N -140 -550 -140 -540 {lab=VDD}
N -380 -550 -380 -510 {lab=VDD}
N -410 -480 -380 -480 {lab=VDD}
N -410 -530 -410 -480 {lab=VDD}
N -410 -530 -380 -530 {lab=VDD}
N -140 -480 -80 -480 {lab=VDD}
N -80 -530 -80 -480 {lab=VDD}
N -140 -530 -80 -530 {lab=VDD}
N -430 -330 -380 -330 {lab=0}
N -430 -330 -430 -280 {lab=0}
N -430 -280 -380 -280 {lab=0}
N -140 -330 -70 -330 {lab=0}
N -70 -330 -70 -280 {lab=0}
N -140 -280 -70 -280 {lab=0}
N 80 -410 110 -410 {lab=WBL}
N 110 -600 110 -410 {lab=WBL}
N -630 -620 -630 -580 {lab=WWL}
N -270 -630 -270 -550 {lab=VDD}
N 340 -450 340 -240 {lab=0}
N 190 -240 340 -240 {lab=0}
N 50 -410 50 -240 {lab=0}
N 480 -450 490 -450 {lab=#net1}
N 490 -450 500 -450 {lab=#net1}
N 730 -450 740 -450 {lab=#net1}
N 740 -450 750 -450 {lab=#net1}
N 750 -450 760 -450 {lab=#net1}
N 760 -450 770 -450 {lab=#net1}
N 770 -450 780 -450 {lab=#net1}
N 780 -450 790 -450 {lab=#net1}
N 790 -450 800 -450 {lab=#net1}
N 840 -420 870 -420 {lab=PRE_B}
N 800 -390 800 -330 {lab=VDD}
N 750 -420 800 -420 {lab=VDD}
N 750 -420 750 -370 {lab=VDD}
N 750 -370 800 -370 {lab=VDD}
N 430 -450 480 -450 {lab=#net1}
N 500 -450 570 -450 {lab=#net1}
N 570 -450 730 -450 {lab=#net1}
N 540 -540 540 -450 {lab=#net1}
N 540 -630 540 -600 {lab=CL}
N 480 -570 500 -570 {lab=SHARE}
N 540 -570 590 -570 {lab=0}
N 590 -570 590 -520 {lab=0}
N 690 -540 690 -450 {lab=#net1}
N 540 -700 540 -630 {lab=CL}
N 690 -670 690 -600 {lab=CL}
N 540 -670 690 -670 {lab=CL}
N 730 -570 740 -570 {lab=SHARE_B}
N 640 -570 690 -570 {lab=VDD}
N 640 -570 640 -510 {lab=VDD}
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -360 -330 2 0 {name=M1
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
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -360 -480 2 0 {name=M2
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
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} -160 -480 0 0 {name=M3
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
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -160 -330 0 0 {name=M4
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
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} -630 -420 1 0 {name=M5
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
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 50 -430 1 0 {name=M6
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
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 170 -380 0 0 {name=M7
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
C {/usr/local/share/pdk/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 340 -470 1 0 {name=M8
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
C {gnd.sym} -240 -240 0 0 {name=l1 lab=0}
C {ipin.sym} -710 -580 1 0 {name=p1 lab=WBLB}
C {ipin.sym} 110 -600 1 0 {name=p2 lab=WBL}
C {ipin.sym} 340 -600 1 0 {name=p3 lab=RWL}
C {ipin.sym} -630 -620 1 0 {name=p6 lab=WWL}
C {lab_wire.sym} -500 -400 0 0 {name=p14 sig_type=std_logic lab=qb}
C {lab_wire.sym} -60 -410 0 0 {name=p15 sig_type=std_logic lab=q}
C {ipin.sym} -270 -630 1 0 {name=p7 lab=VDD}
C {lab_wire.sym} 190 -600 0 0 {name=p5 sig_type=std_logic lab=output}
C {capa.sym} 430 -420 0 0 {name=C1
m=1
value=\{10f*(1+csig*agauss(0,1,1))\}
footprint=1206
device="ceramic capacitor"}
C {/home/blazeinkid/eda_sources/open_pdks/sky130/sky130A/libs.tech/xschem/sky130_fd_pr/nfet_01v8.sym} 520 -570 0 0 {name=M9
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
C {/home/blazeinkid/eda_sources/open_pdks/sky130/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 820 -420 2 0 {name=M10
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
C {/home/blazeinkid/eda_sources/open_pdks/sky130/sky130A/libs.tech/xschem/sky130_fd_pr/pfet_01v8.sym} 710 -570 2 0 {name=M11
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
C {ipin.sym} 870 -420 1 0 {name=p8 lab=PRE_B}
C {lab_wire.sym} 800 -330 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {gnd.sym} 430 -390 0 0 {name=l2 lab=0}
C {ipin.sym} 540 -700 1 0 {name=p4 lab=CL}
C {ipin.sym} 480 -570 0 0 {name=p10 lab=SHARE}
C {gnd.sym} 590 -520 0 0 {name=l3 lab=0}
C {ipin.sym} 740 -570 2 0 {name=p11 lab=SHARE_B}
C {lab_wire.sym} 640 -510 2 0 {name=p12 sig_type=std_logic lab=VDD}
