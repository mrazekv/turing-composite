#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Simulator Turingovych stroju definovanych kompozitnim diagramem
# Autor: Vojtech Mrazek
import sys


class R:
    """ Posun pasky doprava, bud o jeden symbol, nebo na dany symbol
Pokud aktualni symbol je shodny s hledanym, nic se nedeje, hleda
se az v tin dalsim"""
    def __init__(self, char=None):
        if not char:
            self.type = 0
            self.data = "R"

        else:
            if len(char) == 2 and char[0] == "!":
                self.type = 2
                self.char = char[1]
            else:
                self.type = 1
                self.char = char
            self.data = "R(" + char + ")"

    def do(self, ts):
        if self.type == 0:
            ts.head += 1
        else:
            while 1:
                ts.head += 1
                if ((self.type == 1 and ts.tape[ts.head] == self.char) or
                    (self.type == 2 and ts.tape[ts.head] != self.char)):
                    break


class L:
    """ Posun pasky doleva, bud o jeden symbol, nebo na dany symbol
Pokud aktualni symbol je shodny s hledanym, nic se nedeje, hleda
se az v tin dalsim"""
    def __init__(self, char=None):
        if not char:
            self.type = 0
            self.data = "L"

        else:
            if len(char) == 2 and char[0] == "!":
                self.type = 2
                self.char = char[1]
            else:
                self.type = 1
                self.char = char
            self.data = "L(" + char + ")"

    def do(self, ts):
        if self.type == 0:
            ts.head -= 1
        else:
            while 1:
                ts.head -= 1
                if ((self.type == 1 and ts.tape[ts.head] == self.char) or
                    (self.type == 2 and ts.tape[ts.head] != self.char)):
                    break


class C:
    """ Nahrazeni symbolu symbolem novym. Pokud se mu jako novy symbol
da MemRead, tak se vlozi symbol z pameti"""
    def __init__(self, new):
        self.new = new
        self.data = new

    def do(self, ts):
        s = list(ts.tape)
        self.data = str(self.data)
        s[ts.head] = str(self.new)
        ts.tape = "".join(s)


class Mem:
    """ Slouzi k zapamatovani symbolu do pameti TS. Jmeno musi byt unikatni
TS totiz nema zadny zasobnik a podobne"""
    def __init__(self, memory):
        self.memory = memory
        self.data = " -- } " + memory + " --"

    def do(self, ts):
        ts.set_memory(self.memory, ts.tape[ts.head])
        self.data = "%s = %s" % (self.memory, ts.tape[ts.head])


class Sr:
    """Posune retezec neblankovych symbolu nachazejicich se vlevo od aktualni
pozice hlavy o 1 symbol doprava"""
    def __init__(self):
        self.data = "Sr"

    def do(self, ts):
        s = list(ts.tape)
        pos = ts.head
        while 1:
            s[ts.head] = s[ts.head - 1]
            ts.head -= 1
            if s[ts.head] == "_":
                ts.head = pos
                break
        ts.tape = "".join(s)


class Sl:
    """Posune retezec neblankovych symbolu nachazejicich se vpravo od aktualni
pozice hlavy o 1 symbol doleva"""
    def __init__(self):
        self.data = "Sl"

    def do(self, ts):
        s = list(ts.tape)
        pos = ts.head
        while 1:
            s[ts.head] = s[ts.head + 1]
            ts.head += 1
            if s[ts.head] == "_":
                ts.head = pos
                break
        ts.tape = "".join(s)


class MemRead:
    """Slouzi pro cteni dat z pameti, neni to klasicky stroj! Vklada se az
do symbolu C"""
    def __init__(self, ts, memory):
        self.ts = ts
        self.memory = memory
        self.data = self.memory

    def __str__(self):
        mem = self.ts.get_memory(self.memory)
        if mem == "":
            return self.memory
        return mem

    def do(self, ts):
        s = list(ts.tape)
        self.data = "put " + self.memory + " (" + str(self) + ") "
        s[ts.head] = str(self)
        ts.tape = "".join(s)


class Note:
    """Vytiskne poznamku a nemeni nic na pasce """
    def __init__(self, t):
        self.data = " [" + t + "] "

    def do(self, ts):
        pass


class TuringMachine:
    """ Vlastni turinguv stroj """
    def __init__(self, verbose=True):
        self.counter = 0
        self.commands = []
        self.connections = []
        self.memory = {}
        self.verbose = verbose

    def add_command(self, *cmd):
        if hasattr(cmd[0], '__iter__'):
            self.commands += [self._replace_strings_with_c(cmd[0])]
        else:
            self.commands += [self._replace_strings_with_c(cmd)]
        self.counter += 1
        return self.counter - 1

    def add_connection(self, start, end, *chars):
        # Vice retezcu
        if len(chars) > 1:
            for a in chars:
                self.add_connection(start, end, a)
            return
        elif len(chars) == 1:
            char = chars[0]
        else:
            char = None

        # Nalezeni nedeterminismu
        for s, e, c in self.connections:
            if start != s:
                continue

            if c == char:
                raise Exception("Nedeterminismus")

            if len(str(c)) == 2 and str(c)[0] == "!" and c[1] != char:
                raise Exception("Nedeterminismus - uz je definovany NOT")

            if (len(str(char)) == 2 and str(char)[0] == "!"
                and (str(char)[1]) != c):
                raise Exception("Nedeterminismus - uz je definovany NOT")

        self.connections += [(start, end, char)]

    def set_memory(self, name, value):
        self.memory[name] = value

    def get_memory(self, name):
        try:
            return self.memory[name]
        except KeyError:
            return ""

    def _replace_strings_with_c(self, cmd):
        return [c if hasattr(c, 'do') else C(c) for c in cmd]

    def do_command(self, cmd):
        for c in cmd:
            c.do(self)
            self.print_tape(c.data)

    def print_tape(self, desc):
        if not self.verbose:
            return
        i = 0
        for c in self.tape:
            if i == self.head:
                sys.stdout.write("\033[1m\033[31m" + c + "\033[0m")
            else:
                sys.stdout.write(c)
            i += 1
        print "    " + desc

    def run(self, tape):
        self.head = 0
        self.tape = tape + '_' * 10
        self.command = 0

        # nalezeni zacatku
        while self.tape[self.head] == "_":
            self.head += 1
        self.head -= 1
        self.print_tape("init")

        while 1:
            self.do_command(self.commands[self.command])
            # nalezeni dalsiho prechodu
            find = -1
            for s, e, c in self.connections:
                if s == self.command:
                    neg_matched = (len(str(c)) == 2 and str(c)[0] == "!" and
                                   str(c)[1] != self.tape[self.head])
                    if not c or str(c) == self.tape[self.head] or neg_matched:
                        find = e
                        if self.verbose:
                            print "Prechod --> %s" % (c)
                        break

            if find != -1:
                self.command = find
            else:
                if self.verbose:
                    print "Automat se uspesne zastavil"
                break
