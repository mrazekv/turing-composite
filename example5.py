#!/usr/bin/env python

# data z https://www.fit.vutbr.cz/study/courses/TIN/public/Prednasky/tin-pr07-ts1.pdf, pr. 7.8
from ts import *
ts = TuringMachine()

_R = ts.add_command(R('_'))
_L = ts.add_command(L())
_I = ts.add_command('1')
_OLR = ts.add_command('0', L('_'), R())
_SL = ts.add_command(Sl())
_O = ts.add_command('0')
_L2 = ts.add_command(L())

ts.add_connection(_R, _L)
ts.add_connection(_L, _I, '0')
ts.add_connection(_I, _L)
ts.add_connection(_L, _OLR, '1')
ts.add_connection(_OLR, _SL, '0')
ts.add_connection(_OLR, _L2, '1')

ts.add_connection(_O, _L2)

ts.add_connection(_SL, _SL, '0')
ts.add_connection(_SL, _L2, '1')
ts.add_connection(_SL, _O, '_')

ts.run("_111001_____")
