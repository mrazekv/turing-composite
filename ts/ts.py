#!/usr/bin/env python

# Simulator Turingovych stroju definovanych kompozitnim diagramem
# Autor: Vojtech Mrazek
import sys

class R:
    """ Posun pasky doprava, bud o jeden symbol, nebo na dany symbol 
Pokud aktualni symbol je shodny s hledanym, nic se nedeje, hleda
se az v tin dalsim"""
    def __init__(self, char=None):
        if not char:
            self.type=0
            self.data="R"

        else:
            if len(char)==2 and char[0] == "!":
                self.type=2
                self.char=char[1]
            else:
                self.type=1
                self.char=char
            self.data="R(" + char + ")"

    def do(self, ts):
        if self.type==0:
            ts.head+=1
        else:
            while 1:
                ts.head+=1
                if (self.type==1 and ts.tape[ts.head]==self.char) or (self.type==2 and ts.tape[ts.head]!=self.char):
                    break

class L:
    """ Posun pasky doleva, bud o jeden symbol, nebo na dany symbol 
Pokud aktualni symbol je shodny s hledanym, nic se nedeje, hleda
se az v tin dalsim"""
    def __init__(self, char=None):
        if not char:
            self.type=0
            self.data="L"

        else:
            if len(char)==2 and char[0] == "!":
                self.type=2
                self.char=char[1]
            else:
                self.type=1
                self.char=char
            self.data="L(" + char + ")"

    def do(self, ts):
        if self.type==0:
            ts.head-=1
        else:
            while 1:
                ts.head-=1
                if (self.type==1 and ts.tape[ts.head]==self.char) or (self.type==2 and ts.tape[ts.head]!=self.char):
                    break
class C:
    """ Nahrazeni symbolu symbolem novym. Pokud se mu jako novy symbol
da MemRead, tak se vlozi symbol z pameti"""
    def __init__(self, new):
        self.new=new
        self.data=new

    def do(self, ts):
        s=list(ts.tape)
        self.data=str(self.data)
        s[ts.head]=str(self.new)
        ts.tape="".join(s)

class Mem:
    """ Slouzi k zapamatovani symbolu do pameti TS. Jmeno musi byt unikatni
TS totiz nema zadny zasobnik a podobne"""
    def __init__(self, memory):
        self.memory=memory
        self.data=" -- } " + memory + " --" 

    def do(self, ts):
        ts.saveMem(self.memory, ts.tape[ts.head])
        self.data="%s = %s" % (self.memory, ts.tape[ts.head])


class Sr:
    """Posune retezec neblankovych symbolu nachazejicich se vlevo od aktualni
pozice hlavy o 1 symbol doprava"""
    def __init__(self):
        self.data="Sr"
    def do(self, ts):
        s=list(ts.tape)
        pos=ts.head
        while 1:
            s[ts.head]=s[ts.head - 1]
            ts.head-=1
            if s[ts.head]=="_":
                ts.head=pos
                break    
        ts.tape="".join(s)

class Sl:
    """Posune retezec neblankovych symbolu nachazejicich se vpravo od aktualni
pozice hlavy o 1 symbol doleva"""
    def __init__(self):
        self.data="Sl"
    def do(self, ts):
        s=list(ts.tape)
        pos=ts.head
        while 1:
            s[ts.head]=s[ts.head + 1]
            ts.head+=1
            if s[ts.head]=="_":
                ts.head=pos
                break    
        ts.tape="".join(s)
        
class MemRead:
    """Slouzi pro cteni dat z pameti, neni to klasicky stroj! Vklada se az do symbolu
C"""
    def __init__(self, ts, memory):
        self.ts=ts
        self.memory=memory
        self.data=self.memory
    def __str__(self):
        mem = self.ts.getMem(self.memory)
        if mem == "":
            return self.memory
        return mem

    def do(self, ts):
        s=list(ts.tape)
        self.data="put " + self.memory + " (" + str(self) + ") "
        s[ts.head]=str(self)
        ts.tape="".join(s)

class Note:
    """Vytiskne poznamku a nemeni nic na pasce """
    def __init__(self, t):
        self.data=" [" + t + "] "
    def do(self, ts):
        pass

class TS:
    """ Vlastni turinguv stroj """
    def __init__(self, verbose=True):
        self.counter=0
        self.cmd=[]
        self.con=[]
        self.mem={}
        self.verbose=verbose

    def saveMem(self, name, value):
        self.mem[name]=value
    def getMem(self, name):
        try:
            return self.mem[name]
        except KeyError:
            return ""

    def AddCmd(self, cmd):
        self.cmd+=[cmd]
        self.counter+=1
        return self.counter - 1

    def printTape(self, desc):
        if not self.verbose:
            return
        i=0
        for c in self.tape:
            if i==self.head:
                sys.stdout.write("\033[91m" + c + "\033[0m")
            else:
                sys.stdout.write(c)
            i=i+1
        print "    " + desc
    def docmd(self, cmd):
        for c in cmd:
            c.do(self)
            self.printTape(c.data)

    def addCon(self, start, end, char=None):
        # Nalezeni nedeterminismu
        for s,e,c in self.con:
            if start!=s:
                continue
            if c==char:
                raise Exception("Nedeterminismus")
            if len(str(c)) == 2 and str(c)[0]=="!":
                raise Exception("Nedeterminismus - uz je definovany NOT")
            if len(str(char)) == 2 and str(char)[0]=="!":
                raise Exception("Nedeterminismus - uz je definovany NOT")

        self.con+=[(start, end, char)]
    def test(self,tape):
        self.head=0
        self.tape=tape
        self.command=0
        # nalezeni zacatku
        while self.tape[self.head]=="_":
            self.head+=1
        self.head-=1
        self.printTape("init")
        while 1:
            self.docmd(self.cmd[self.command])
            # nalezeni dalsiho prechodu
            find=-1
            for s,e,c in self.con:
                if s==self.command and (not c or str(c)==self.tape[self.head] or (len(str(c)) == 2 and str(c)[0]=="!" and str(c)[1] != self.tape[self.head])):
                    find=e
                    if self.verbose:
                        print "Prechod --> %s" % (c) 
                    break

            if find != -1:
                self.command=find
            else:
                if self.verbose:
                    print "Automat se uspesne zastavil"
                break
