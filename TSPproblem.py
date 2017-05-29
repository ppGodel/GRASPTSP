class TSPProblem:
    def __init__(self, path = None, graph = None):
        if path is not None:
            l = open(path,'r').readlines()
            print(l)
            p = l[0][-1]
            self._problem = [(x.replace("\n", "").split(' ')) for x in l[1:]]
        else:
            self._graph = graph

    @property
    def graph(self):
        return self._graph
                
    def evaluate(self, path):
        valid = 0
        result = 0
        for edge in path:
            u,v = edge[0], edge[1]
            if u in self.graph.vertices.keys():
                if v in self.graph[u].neighbors:
                    result += self.graph[u].neighbors[v]
                else:
                    result = None
                    break
            else:                
                result = None
                break            
        return result 
    
    def costFunction(self, visitedlist, u, v):
        result = None
        if v not in visitedlist and u in self.graph.keys() and v in self.graph[u].neighbors:
            result  = self.graph[u].neighbors[v]
        return result

    def vertexpath(self, path):
        vl = set()
        for edge in path:
            if len(edge) == 2:
                u,v = edge
                vl.add(u)
                vl.add(v)
            if len(edge) == 3:
                u,v,w = edge
                vl.add(u)
                vl.add(v)
        return vl
