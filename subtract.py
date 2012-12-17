#!/usr/bin/env python

# Binarni odcitani v TS
# Autor: Vojtech Mrazek
from ts import *
ts=TuringMachine()
start=ts.add_command([R("_"), C("#"), L("#")])  # pridani # na konec

pre_0=ts.add_command([Note("pre_0"), L()])
pre_1=ts.add_command([Note("pre_1"), L()])

s_01x=ts.add_command([Note("s_01x"), Sr(), R("#"), R("#"), L()]) # nalezeni 2 strany (odcitatele)
s_00x=ts.add_command([Note("s_00x"), Sr(), R("#"), R("#"), L()]) # nalezeni 2 strany (odcitatele)

s_11x=ts.add_command([Note("s_11x"), Sr(), R("#"), R("#"), L()]) # nalezeni 2 strany (odcitatele)
s_10x=ts.add_command([Note("s_10x"), Sr(), R("#"), R("#"), L()]) # nalezeni 2 strany (odcitatele)

# write 1 predict 0
w1_p0=ts.add_command([Note("w1_p0"), Sr(), R("_")])
w1p0s=ts.add_command([Note("w1p0s"), R("_")])
aw1p0=ts.add_command([Note("aw1p0"), L(), Mem("w"), R(), C(MemRead(ts, "w")), L()])
bw1p0=ts.add_command([Note("bw1p0"), R(), C("1"), L("#"), L("#")])

# write 0 predict 0
w0_p0=ts.add_command([Note("w0_p0"), Sr(), R("_")])
w0p0s=ts.add_command([Note("w0p0s"), R("_")])
aw0p0=ts.add_command([Note("aw0p0"), L(), Mem("w"), R(), C(MemRead(ts, "w")), L()])
bw0p0=ts.add_command([Note("bw0p0"), R(), C("0"), L("#"), L("#")])

# write 1 predict 1
w1_p1=ts.add_command([Note("w1_p1"), Sr(), R("_")])
w1p1s=ts.add_command([Note("w1p1s"), R("_")])
aw1p1=ts.add_command([Note("aw1p1"), L(), Mem("w"), R(), C(MemRead(ts, "w")), L()])
bw1p1=ts.add_command([Note("bw1p1"), R(), C("1"), L("#"), L("#")])

# write 0 predict 1
w0_p1=ts.add_command([Note("w0_p1"), Sr(), R("_")])
w0p1s=ts.add_command([Note("w0p1s"), R("_")])
aw0p1=ts.add_command([Note("aw0p1"), L(), Mem("w"), R(), C(MemRead(ts, "w")), L()])
bw0p1=ts.add_command([Note("bw0p1"), R(), C("0"), L("#"), L("#")])

# ukoncovaci
vtest=ts.add_command([Note("vtest"), R(), C("_"), R()])
vtcyc=ts.add_command([Note("vtcyc"), C("_"), R()])
vteok=ts.add_command([Note("vteok"), C("_")])
error=ts.add_command([Note("error"), L("_"), C("0"), R()])
erclr=ts.add_command([Note("erclr"), C("_"), R()])
erfin=ts.add_command([Note("erfin"), L("0"), L()])
prerr=ts.add_command([Note("prerr"), R()])

# Start
ts.add_connection(start, pre_0)
ts.add_connection(pre_0, s_01x, "1")
ts.add_connection(pre_0, s_00x, "0")
ts.add_connection(pre_0, vtest, "_")

ts.add_connection(pre_1, s_11x, "1")
ts.add_connection(pre_1, s_10x, "0")
ts.add_connection(pre_1, prerr, "_")
ts.add_connection(prerr, error)

# ukoncovaci
ts.add_connection(vtest, vtcyc, "0")
ts.add_connection(vtest, error, "1")
ts.add_connection(vtest, vteok, "#")
ts.add_connection(vtcyc, vtcyc, "0")
ts.add_connection(vtcyc, error, "1")
ts.add_connection(vtcyc, vteok, "#")

# chyba
ts.add_connection(error, erclr, "0")
ts.add_connection(error, erclr, "1")
ts.add_connection(error, erclr, "#")
ts.add_connection(error, erfin, "_")

ts.add_connection(erclr, erclr, "0")
ts.add_connection(erclr, erclr, "1")
ts.add_connection(erclr, erclr, "#")
ts.add_connection(erclr, erfin, "_")

# write
# write 1 predict 0
ts.add_connection(w1_p0, aw1p0)
ts.add_connection(w1p0s, aw1p0)
ts.add_connection(aw1p0, aw1p0, "0")
ts.add_connection(aw1p0, aw1p0, "1")
ts.add_connection(aw1p0, bw1p0, "#")
ts.add_connection(bw1p0, pre_0)

# write 0 predict 0
ts.add_connection(w0_p0, aw0p0)
ts.add_connection(w0p0s, aw0p0)
ts.add_connection(aw0p0, aw0p0, "0")
ts.add_connection(aw0p0, aw0p0, "1")
ts.add_connection(aw0p0, bw0p0, "#")
ts.add_connection(bw0p0, pre_0)

# write 1 predict 1
ts.add_connection(w1_p1, aw1p1)
ts.add_connection(w1p1s, aw1p1)
ts.add_connection(aw1p1, aw1p1, "0")
ts.add_connection(aw1p1, aw1p1, "1")
ts.add_connection(aw1p1, bw1p1, "#")
ts.add_connection(bw1p1, pre_1)

# write 0 predict 1
ts.add_connection(w0_p1, aw0p1)
ts.add_connection(w0p1s, aw0p1)
ts.add_connection(aw0p1, aw0p1, "0")
ts.add_connection(aw0p1, aw0p1, "1")
ts.add_connection(aw0p1, bw0p1, "#")
ts.add_connection(bw0p1, pre_1)


# Predict = 0
ts.add_connection(s_01x, w1_p0, "0")
ts.add_connection(s_01x, w0_p0, "1")
ts.add_connection(s_01x, w1p0s, "#")

ts.add_connection(s_00x, w0_p0, "0")
ts.add_connection(s_00x, w1_p1, "1")
ts.add_connection(s_00x, w0p0s, "#")

# Predict = 1
ts.add_connection(s_11x, w0_p0, "0")
ts.add_connection(s_11x, w1_p1, "1")
ts.add_connection(s_11x, w0p0s, "#")

ts.add_connection(s_10x, w1_p1, "0")
ts.add_connection(s_10x, w0_p1, "1")
ts.add_connection(s_10x, w1p1s, "#")

ts.run("_110#111____________________________")

t=Tester(ts)
t.add_test_case("_01011#0000000000001______________________________________________________", r"_*_0*1010__*")
t.add_test_case("_01011#1000000000001______________________________________________________", r"_*_0*0__*")
t.add_test_case("_00000000000000000000001011#1000000000001______________________________________________________", r"_*_0*0__*")
t.add_test_case("_01011#01011______________________________________________________", r"_*_0*0__*")
t.add_test_case("_1#1______________________________________________________", r"_*_0*0__*")
t.add_test_case("_1000000000000#1000000000000______________________________________________________", r"_*_0*0__*")
t.add_test_case("_1000000000001#1000000000000______________________________________________________", r"_*_0*1__*")
t.add_test_case("_1100000000001#1000000000000______________________________________________________", r"_*_0*100000000001__*")
t.add_test_case("_00000000000000000100001011#00000000010001______________________________________________________", r"_*_0*11111010__*")
 
t.run_test()
#print ToGraph(ts)
