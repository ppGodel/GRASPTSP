import graph
import math
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

class TSPProblem:
    def __init__(self, path = None, p_graph = None):
        if path is not None:
            l = open(path,'r').readlines()
            #print(l)
            cl = l[0].split(' ')
            name = path.split('/')[-1].split('.')[0]
            if cl[0].lower == 'name':
                name = cl[2]
            i=1
            #print(name)
            self._graph = graph.Graph(name, directed=False)
            while l[i][0].isalpha():                    
                i+=1
            print('i',i)    
            for vl in l[i:]:
                il = vl.split(' ')
                #and il[1].isdigit() and il[2].isdigit()
                if len(il)>=3 and isfloat(il[1].replace('\n','')) and isfloat(il[2].replace('\n','')):
                    v = graph.Vertex(il[0], coord=( float(il[1].replace('\n','')), float(il[2].replace('\n','')) ) )
                    self._graph.add_vertex(v)

            for v in self._graph.vertices:
                #print(self._graph[v])
                for n in self._graph.vertices:
                    if v != n:
                         x1, y1 = self._graph[v].label['coord']
                         x2, y2 = self._graph[n].label['coord']
                         #print(x1,y1,x2,y2)                         
                         self._graph[v].add_neighbor(n, distance = math.sqrt( (x2-x1)**2 + (y2-y1)**2 ))
        elif graph is not None:
            self._graph = p_graph

    @property
    def graph(self):
        return self._graph
                
    def evaluate(self, path, key ='weight'):
        valid = 0
        result = 0
        for edge in path:
            u,v = edge[0], edge[1]
            if u in self.graph.vertices.keys():
                if v in self.graph[u].neighbors:
                    result += self.graph[u].neighbors[v][key]
                else:
                    result = None
                    break
            else:                
                result = None
                break            
        return result 
    
    def costFunction(self, visitedlist, u, v, key='weight'):
        result = None
        if v not in visitedlist and u in self.graph.keys() and v in self.graph[u].neighbors:
            result  = self.graph[u].neighbors[v][key]
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
