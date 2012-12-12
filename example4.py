#!/usr/bin/env python

# Ukazka ticheho rezimu
from ts import *
ts = TuringMachine(False)

s = ts.add_command([R("!x"), R("!y"), L("!y")])
n = ts.add_command([Note("test")])
ts.add_connection(s, n, "!z")

ts.run("_xxxyyzzz_________")
print ts.tape
