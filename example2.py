#!/usr/bin/env python

# data z https://www.fit.vutbr.cz/study/courses/TIN/public/Prednasky/tin-pr07-ts1.pdf
from ts import *
ts=TS()

# Kopirovaci stroj  _w_ transformuje na _w_w_
s1=ts.AddCmd([R("_"), R(), C("_"), L("_"), L("_")])
s2=ts.AddCmd([R()])
s3=ts.AddCmd([Mem("w"), C("_"), R("_"), R("_"), C(MemRead(ts, "w")), R(), C("_"), L("_"), L("_"), C(MemRead(ts, "w"))])

ts.addCon(s1, s2)
ts.addCon(s2, s3, "x")
ts.addCon(s2, s3, "y")
ts.addCon(s3, s2)


ts.test("_xyyxx_______________")
