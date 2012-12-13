#!/usr/bin/env python

# Ukazka XORu a testovania vsetkych moznosti

from ts import *
ts = TuringMachine(False)

do = ts.add_command([R()])
do0 = ts.add_command([C('1')])
do1 = ts.add_command([C('0')])

ts.add_connection(do, do0, '0')
ts.add_connection(do0, do)

ts.add_connection(do, do1, '1')
ts.add_connection(do1, do)

# Otestuj to na 8 bitoch
bits = 8
for i in range(2 ** bits):
    # Preved na binarne cislo a zarovnaj na dany pocet bitov
    i_bin = bin(i)[2:]
    i_bin = '0' * (bits - len(i_bin)) + i_bin

    tape = "_%s__________" % i_bin
    ts.run(tape)

    # Preved vysledok na cislo
    res = ts.tape.strip('_')
    res = int(res, 2)

    # skontroluj vysledok
    mask = 2 ** bits - 1
    assert (~i & mask) == res, "Negacia nefunguje pre i=%d" % i
