#!/usr/bin/env python

# Ukazka negaci v prechodech i v posunech
from ts import *
ts = TuringMachine()

s = ts.add_command(R("!x"), R("!y"), L("!y"))
n = ts.add_command(Note("test"))
o = ts.add_command(Note("next"))
ts.add_connection(n, o, "x", "y", "z")
ts.add_connection(s, n, "!z")

ts.run("_xxxyyzzz_________")
