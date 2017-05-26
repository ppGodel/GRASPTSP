import graph
import random
import TSPproblem

def graspTSP(probgraph, iters, alpha):
    sa = (None, 0)
    bs, bv = sa
    tspp = TSPproblem.TSPProblem(graph = probgraph)
    sl = []
    print(tspp.graph)
    for i in range(iters):
        so = greedyconstructive(tspp, alpha)
        ls = localsearch(tspp,so)
        av = tspp.evaluate(ls)
        if bv < av:
            bs = ls
            bv = av
            fi = i
        sl.append((i, ls,av))
        #print(so, ae, ls,be)
    return bs, bv, fi, sl

def greedyconstructive(prob, alpha):
    path = []
    vl = list(prob.graph.vertices.keys())
    elem = random.choice(vl)
    si = elem
    #pendiente
    pl ={elem}
    vl.remove(elem)
    while len(vl)>0:
        #print(prob.graph[elem].neighbors.keys(), pl)
        nl = list(set(prob.graph[elem].neighbors.keys()) - pl)
        if len(nl) == 0:
            break
        wnl = [(x, prob.graph[elem].neighbors[x]) for x in nl ]
        onl = sorted(wnl, key=lambda x:x[1])
        lim = round(alpha*len(onl)) if round(alpha*len(onl)) > 1 else 1
        rcl = onl[0:lim]
        ce = random.choice(rcl)
        #print (nl, elem, ce[0], ce[1])
        tup = (elem, ce[0], ce[1])
        path.append(tup)
        elem = ce[0]
        pl.add(ce[0])
        vl.remove(ce[0])
    if len(path) == (prob.graph.cardinal)-1:
        path.append((elem, si, prob.graph[elem].neighbors[si]))
    return path
    
def localsearch(prob, so):
    
    return so

