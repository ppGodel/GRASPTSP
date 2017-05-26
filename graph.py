import multiprocessing
import random
import math
from heapq import heappop, heappush

def flatten(L):
    while len(L) > 0:
        yield L[0]
        L = L[1]

class Vertex:
    def __init__(self, _id, _object):
        self._id = _id
        self._value = _object
        self._outneighbors = {}
        self._inneighbors = {}
        self._label = dict()
        self._label['id'] = _id
        self._label['value'] = _object

    @property
    def id(self):
        return self._id

    @property
    def value(self):
        return self._value

    @property
    def neighbors(self):
        return self._outneighbors
    
    @property
    def inneighbors(self):
        return self._inneighbors
    
    @property
    def label(self):
        return self._label
    
    def __str__(self):
        result = 'Vertex: ' + str(self.id) + '\n'
        result += 'Value: ' + str(self._value) + '\n'
        if len(self.neighbors)>0:
            result += 'Neighbors: OutDegree('+ str(len(self.neighbors)) + ')\n'
            for n in self.neighbors:
                result += 'Vertex: ' + str(n) + ' weight: ' + str(self.neighbors[n])
                result += '\n'
        else:
            result += 'No Neighbors \n'        
        if len(self.inneighbors)>0:
            result += 'In Neighbors: InDegree('+ str(len(self.inneighbors)) + ')\n'
            for n in self.inneighbors:
                result += 'Vertex: ' + str(n) + ' weight: ' + str(self.inneighbors[n])
                result += '\n'
        else:
            result += 'No in Neighbors \n'
        return result

    def add_neighbor(self, _neighbor, _weight=1):
        if _neighbor not in self.neighbors.keys():
            self.neighbors[_neighbor] = _weight

    def add_inneighbor(self, _inneighbor, _weight=1):
        if _inneighbor not in self.inneighbors.keys():
            self.inneighbors[_inneighbor] = _weight

class Graph:
    def __init__(self, name, directed = False):
        self._vertices = dict()
        self._id = name
        self._directed = directed
        self._complete = None
        self._tree = None
        self.cyclic = None
        self._connect = None
    @property
    def vertices(self):
        return self._vertices

    @property
    def cardinal(self):
        return len(self._vertices)

    @property
    def id(self):
        return self._id

    @property
    def complete(self):
        if self._complete is None:
            self._complete = self.iscomplete()
        return self._complete

    @property
    def connected(self):
        if self._connect is None:
            self._connect = self.isconnected()
        return self._connect
    @property
    def density(self):
        n = self.cardinal
        return self.degreesum / (n * (n - 1.0))
    @property
    def tree(self):
        if self._tree is None:
            self._tree = self.istree()
        return self._tree
    @property
    def degreesum(self):
        return sum([len(self.vertices[v].neighbors) for v in self.vertices]) 
    @property
    def directed(self):
        return self._directed

    def __getitem__(self, item):
        res = None
        if isinstance(item, str):
            res = self._vertices[item]
            if res == None:
                res = [j for i, j in enumerate(self._vertices) if j.id == item]
        if isinstance(item, int):
            res = self._vertices[item]
        if isinstance(item, Vertex):
            res = [j for i, j in enumerate(self._vertices) if j == item]
        return res

    def __iter__(self):
        res = iter(self._vertices.values())
        return res

    def __str__(self):
        result = 'Graph: ' + str(self.id) + '\n'
        result += 'Number of vertices: ' + str(self.cardinal) + '\n'
        result += 'Number of edges: ' + str(self.getNumberEdges()) + '\n'
        result += 'Directed: ' + str(self.directed) +'\n'
        result += 'Connected: ' + str(self.connected) +'\n'
        result += 'Complete: ' + str(self.complete) +'\n'
        result += 'Tree: ' + str(self.tree) +'\n'
        for v in (self._vertices):
            result += str(self._vertices[v]) + '\n'
        return result

    def add_vertex(self, _vertex_obj):
        if isinstance(_vertex_obj, Vertex):
            if _vertex_obj not in self._vertices and _vertex_obj.id not in self._vertices.keys():
                self._vertices[_vertex_obj.id] = _vertex_obj
        return _vertex_obj

    def add_edge(self, _begin, _end, _weight=1):
#        beg, end = None, None
        if isinstance(_begin, Vertex):
            if _begin.id in self.vertices.keys():
                beg = self.vertices[_begin.id]
            else:
                beg = _beg
            self.add_vertex(beg)                
        else:
            if _begin in self._vertices.keys():
                beg = self._vertices[_begin]
            else:
                beg = Vertex(_begin, None)
                self.add_vertex(beg)
        if isinstance(_end, Vertex):
            if _end.id in self.vertices.keys():
                end = self.vertices[_end.id]
            else:
                end = _end
            self.add_vertex(end)
        else:
            if _end in self._vertices.keys():
                end = self._vertices[_end]
            else:
                end = Vertex(_end, None)
                self.add_vertex(end)

        # print(beg.id, end.id, _weight)
        if not self.directed:
            self.vertices[end.id].add_neighbor(beg.id, _weight)
            self.vertices[beg.id].add_inneighbor(end.id, _weight)
        self.vertices[beg.id].add_neighbor(end.id, _weight)
        self.vertices[end.id].add_inneighbor(beg.id, _weight)
#        print(beg.id, beg.inneighbors,end.id, end.inneighbors)

    def remove_vertex(self, v):
        if isinstance(v, Vertex):
            rem = v
        else:
            if v in self._vertices.keys():
                rem = self._vertices[v]
            else:
                return None
        result = Graph(self.id + ' -' + rem.id)
        for n in self._vertices:
            if rem .id != self._vertices[n]:
                a = Vertex(self._vertices[n].id, self._vertices[n].value)
                for nn in self._vertices[n].neighbors:
                    if nn != rem.id:
                        a.add_neighbor(nn, self._vertices[n].neighbors[nn])
                result.add_vertex(a)
        return result

    def have_leafs(self):
        result = False
        for v in self._vertices:
            if len(self._vertices[v].neighbors) == 0:
                result = True
                break
        else:
            result = False
        return result

    def adjacent_matrix(self):
        result = {}
        for v in self._vertices:
            result[v] = {}
            for n in self._vertices:
                if n in self._vertices[v].neighbors:
                    result[v][n] = self._vertices[v].neighbors[n]
                else:
                    result[v][n] = 0
        return result

    def getedges(self):
        result = dict()
        for v in self.vertices:
            for n in self.vertices[v].neighbors:
                result[(v,n)] = self.vertices[v].neighbors[n]
        return result

    def vertexcomplete(self, v):
        result = False
        for n in self._vertices:
            if v != n and n not in self._vertices[v].neighbors:
                break
        else:
            result = True
        return result

    def iscomplete(self):
        result = True
#        for v in self.vertices:
#            result = result and self.vertexcomplete(v)
        with multiprocessing.Pool() as pool:
            workers = []
            results = []
            for v in self._vertices:
                workers.append(pool.apply_async(func=Graph.vertexcomplete, args=(self, v,)))
            for w in workers:
                result = result and w.get()
                
        return result

    def istree(self):
        result = False
        if self.connected and (((self.cardinal if self.directed else self.cardinal*2) -1) == self.getNumberEdges()):
            result = True
        return result

    def isconnected(self):
        result = False
        bfs = self.deepfirstsearch(None)
        if len(bfs) == self.cardinal:
            result = True
        return result

    def iscyclic(self):
        return False

    def getNumberEdges(self):
        edges = 0
        for v in self.vertices:
                edges+= len(self._vertices[v].neighbors)
        return edges
    
    def deepfirstsearch(self, v=None):
        if v is None: 
            lv = [x for x in self.vertices if len(self[x].inneighbors) == 0 and len(self[x].neighbors) > 0]
            if len(lv)> 0:
                v = self[lv[-1]]
            else:
                v = self[random.choice(list(self.vertices))]
        else:
            if v is not Vertex:
                v = self[v]
            else:
                v= self[v.id]                
        g = []
        p = [v]
        while len(p)>0:
            av = p.pop()
            if av.id not in g:
                g.append(av.id)
            # print(av.id)
               # print(av.neighbors.keys())
                if len(av.neighbors) > 0:
                    ne = list(av.neighbors.keys())
                    random.shuffle(ne)
                    for n in ne:
                        #print('v', av.id, 'n', n, 'p', p)
                        ne = self[n]
                        if ne.id not in g:
                            if ne not in p:
                                p.append(ne)
        return g

    def breadthfirstsearch(self, v=None):
        if v is None:
            lv = [x for x in self.vertices if len(self[x].inneighbors) == 0 and len(self[x].neighbors) > 0]
            if len(lv)> 0:
                v = self[lv[-1]]
            else:
                v = self[random.choice(list(self.vertices))]
        else:
            if v is not Vertex:
                v =self[v]
            else:
                v= self[v.id]
        levels = {}
        levels[v.id] = 0
        sig = [v]
        #print(v.id, levels[v.id])
        while len(sig) > 0:
            mark = []
            for l in sig:
                for n in l.neighbors:   
                    if n not in levels:
                        levels[n]= levels[l.id]+1
                        mark.append(self[n])
            sig = mark            
        return levels

    def closenesscentrality(self, av):        
        lvl = {}
        bg = self.breadthfirstsearch(av)
        #print(lvl)
        #print(bg)
        s = 0
        for c in bg:
            if bg[c] > 0:
                s += 1/bg[c]
            else:
                s += 0
        m = self.cardinal
        #print(m,s)
        if s <= 0:
            r = math.inf
        else:
            r = m/s        
        return r

        
    def shortest(self, v, w): # Dijkstra's algorithm
        if v is Vertex:
            v = v.id
        if w is Vertex:
            w = w.id
        q = [(0, v, ())]
        visited = set() 
        while len(q) > 0:
            (l, u, p) = heappop(q)
            if u not in visited:
                visited.add(u)
                if u == w:
                    return list(flatten(p))[::-1] + [u]
            p = (u, p) 
            for n in self[u].neighbors:
                if n not in visited:
                    heappush(q, (l + 1, n, p))
        return None
    
    def allshortedpaths(self):
        p = list()
        visited = []
        for v in self:
            visited.append(v)
            for u in self:
                if u not in visited:
                    res = self.shortest(v, u)
                    if res is not None:
                        p.append(res)
        return p

    def betweennesscentrality(self, v=None):
        p = self.allshortedpaths()
        if element is None: # all vertex betweennesses
            b = defaultdict(int) # zero if no paths
            for v in self:
                b[v] = sum([v in s for s in p])
            return b
        elif element in self: # vertex betweenness
            return sum([element in s for s in p])
        elif len(element) == 2: # edge betweenness
            (v, u) = element
            c = 0
            for s in p:
                if v in s and u in s:
                    if fabs(s.index(v) - s.index(u)) == 1:
                        c += 1
            return c

    def kruskal(self):
        e = self.getedges()
        #for v in self.vertices:
        #    for n in self[v].neighbors:
        #        e[(v,n)] = self[v].neighbors[n]
        arbol = Graph(self.id + ' MST from kuskal')
        peso = 0
        comp = dict()
        #print(e)
        t = sorted(e.keys(), key = (lambda k: e[k]))        
        #print(t)
        comp = dict()
        nuevo = set()
        while len(t) > 0 and len(nuevo) < len(self.vertices):
            #print(len(t)) 
            arista = t.pop()
            w = e[arista]    
            del e[arista]
            (u,v) = arista
            c = comp.get(v, {v})
            if u not in c:
                #print('u ',u, 'v ',v ,'c ', c)
                arbol.add_edge(u,v,w)
                peso += w
                nuevo = c.union(comp.get(u,{u}))
                for i in nuevo:
                    comp[i]= nuevo
        print('MST con peso', peso, ':', nuevo)
        return arbol
        
