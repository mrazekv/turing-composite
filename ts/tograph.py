# -*- coding: utf-8 -*-


class ToGraph:
    """Use `dot -Tpng -o o.png` on string output`"""

    def __init__(self, tm):
        self.connections = tm.connections
        self.commands = tm.commands

    def __str__(self):
        res = ["digraph ethane {", "node [shape=box];", "rankdir=LR;"]

        c2s = {}
        i = -1
        ci = 0
        for cmd in self.commands:
            i += 1
            sname = "struct_%d" % i
            s = "%s [label=\"" % sname

            l = []
            for c in cmd:
                ci += 1
                #cname = "<f%d> %s" % (ci, c.__class__.__name__)
                cname = str(c.data)  # __class__.__name__
                l.append(cname)
                #c2s[c] = (sname, cname)

            c2s[i] = sname
            s += "".join(l)
            s += "\"];"

            res.append(s)

        # group by chars
        cons = {}
        for con in self.connections:
            start, end, char = con
            s_e = (start, end)
            if s_e in cons:
                cons[s_e].append(char)
            else:
                cons[s_e] = [char]

        for k, v in cons.iteritems():
            start, end = k
            chars = v
            # no None types
            char = ", ".join(filter(lambda x: x, chars))

            start_node = c2s[start]
            end_node = c2s[end]
            #st = "%s:%s -> %s:%s;" % (start_node[0], start_node[1],
            #    end_node[0], end_node[1])
            label = ""
            if char:
                label = '[label="%s"]' % char
            st = '%s -> %s %s;' % (start_node, end_node, label)

            res.append(st)

        res.append("}\n")
        return "\n".join(res)


if __name__ == '__main__':
    from ts import *
    ts = TS()

    # Kopirovaci stroj  _w_ transformuje na _w_w_
    s1 = ts.add_command(R("_"), R(), "_", L("_"), L("_"))
    s2 = ts.add_command(R())
    s3 = ts.add_command(Mem("w"), "_", R("_"), R("_"), C(MemRead(ts, "w")), R(), "_", L("_"), L("_"), C(MemRead(ts, "w")))

    ts.add_connection(s1, s2)
    ts.add_connection(s2, s3, "x")
    ts.add_connection(s2, s3, "z")
    ts.add_connection(s2, s3, "y")
    ts.add_connection(s3, s2)

    #ts.test("______________xyyxx_________")
    tg = ToGraph(ts)
    print tg
