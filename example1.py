#!/usr/bin/env python

# data z https://www.fit.vutbr.cz/study/courses/TIN/public/Prednasky/tin-pr07-ts1.pdf
from ts import *
ts = TuringMachine()

ts.add_command(R(), R(), R(), R(), Sr())

ts.run("_xyyxx_________")
