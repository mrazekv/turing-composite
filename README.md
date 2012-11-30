turing-composite
================

Deterministic turing machine simulator in composite format


Umoznuje simulaci TS v kompozitnim modelu. Obsahuje:
 - model TS
 - prechod R
 - prechod L
 - prechod L_x
 - prechod R_x
 - ukladani do pameti
 - cteni z pameti
 - Shift left (Sl)
 - Shift right (Sr)

Blank symboly jsou definovany pomoci symbolu podtrzitka "_"


Vice informaci a ukazka moznosti v prikladech.

Nekonecna paska neni implementovana, na zacatek je nutne vlozit na pasku okolo dostatecne mnozstvi blank symbolu


Vystup je barevny pro unixove konzole, kdy se cervenou barvou ukazuje pozice cteci hlavy


Generovani obrazku
==========================
Kdyz nagenerujeme TS, tak misto funkce "test" importujeme kreslici knihovnu
  
from tograph import ToGraph
.....


print ToGraph(ts)


Tento stroj transformujeme na obrazek pres
  python test.py | dot -Tpng -o output.png

Pripadne muzeme transformovat data do jineho formatu (napr svg) a ten pak upravit
