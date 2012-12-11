#!/usr/bin/env python

# Ukazka testovani (twtw)
from ts import *
 
# ukazka testovani
ts=TS()
 
# popis vasho TS
 
t=Tester(ts)
# t.add_test_case(vstup, ocekavany vystup (RE))
t.add_test_case("_01011#0000000000001______________________________________________________", r"_*_1010__*")
t.add_test_case("_01011#1000000000001______________________________________________________", r"_*_0__*")
 
t.run_test()
