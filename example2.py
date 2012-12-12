#!/usr/bin/env python

# data z https://www.fit.vutbr.cz/study/courses/TIN/public/Prednasky/tin-pr07-ts1.pdf
from ts import *
ts = TuringMachine()

# Kopirovaci stroj  _w_ transformuje na _w_w_
s1 = ts.add_command(R("_"), R(), "_", L("_"), L("_"))
s2 = ts.add_command(R())
s3 = ts.add_command(Mem("w"), "_", R("_"), R("_"), C(MemRead(ts, "w")), R(), "_", L("_"), L("_"), C(MemRead(ts, "w")))

ts.add_connection(s1, s2)
ts.add_connection(s2, s3, "x")
ts.add_connection(s2, s3, "y")
ts.add_connection(s3, s2)


ts.run("_xyyxx_______________")
#print ToGraph(ts)
