#!/usr/bin/env python

# Ukazka ticheho rezimu
from ts import *
ts=TS(False)

s=ts.AddCmd([R("!x"), R("!y"), L("!y")])
n=ts.AddCmd([Note("test")])
ts.addCon(s,n, "!z")

ts.test("_xxxyyzzz_________")
print ts.tape
