#!/usr/bin/env python

# Ukazka negaci v prechodech i v posunech
from ts import *
ts=TS()

s=ts.AddCmd([R("!x"), R("!y"), L("!y")])
n=ts.AddCmd([Note("test")])
ts.addCon(s,n, "!z")

ts.test("_xxxyyzzz_________")
print ts.tape
