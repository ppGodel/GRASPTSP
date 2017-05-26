import graph
import random
import math
from enum import Enum

class GraphTypes(Enum):
    complete = 0
    connected = 1
    tree = 2

    
class DistributionsTypes(Enum):
    uniform = 1
    normal = 2
    binomial = 3
    exponential = 4
    geometric = 5
    random = 10

class Distribution():
    def __init__(self, Distribution_type = DistributionsTypes.uniform, p1 = None, p2 = None):
        self.type = Distribution_type
        self._parameter1 = p1
        self._parameter2 = p2

    @property
    def parameter1(self):
        return self._parameter1
    
    @property
    def parameter2(self):
        return self._parameter2

class GraphInstancesGenerator():
    def __init__(self, graphtype, distribution_weight, distribution_degree, continuous_weight = False, directed = True):
        self.directed = directed
        self.type = graphtype
        if self.type is GraphTypes.complete:
            self.distributiondegree = Distribution(DistributionsTypes.uniform, 10)
        else:
            self.distributiondegree = distribution_degree
        self.distributionweight = distribution_weight
        self.continuousweight = continuous_weight

    def getweightvalue(self, novertex = None):
        weight = 1
        if self.distributionweight.type is DistributionsTypes.uniform:
            if self.distributionweight.parameter2 is not None:
                if  self.continuousweight:
                    weight = random.uniform(self.distributionweight.parameter1, self.distributionweight.parameter2)
                else:
                    weight = random.randint(max(self.distributionweight.parameter1,0), self.distributionweight.parameter2)
            else:
                    weight = self.distributionweight.parameter1                    
        if self.distributionweight.type is DistributionsTypes.normal:
            weight = random.normalvariate(self.distributionweight.parameter1,self.distributionweight.parameter2)
        if self.distributionweight.type is DistributionsTypes.exponential:
            weight = random.expvariate(1/(self.distributionweight.parameter1))    
        if self.distributiondegree.type is DistributionsTypes.geometric:
            degree = round(math.log(random.random())/math.log(self.distributiondegree.parameter1/novertex))    
        if  self.continuousweight:
            weight = round(random.uniform(0, novertex))
        return weight

    
    def getdegreevalue(self, noedges, novertex):
        degree = 1
        if self.distributionweight.type is DistributionsTypes.uniform:
            if  self.distributionweight.parameter2 is not None:
                degree = random.randint(max(self.distributionweight.parameter1,1), min(self.distributionweight.parameter2, novertex))
            else:
                degree = min(self.distributionweight.parameter1, novertex)
        if self.distributiondegree.type is DistributionsTypes.normal:
            degree = round(random.normalvariate(self.distributiondegree.parameter1,self.distributiondegree.parameter2))
            degree = min(degree, novertex)
        if self.distributiondegree.type is DistributionsTypes.exponential:
            degree = round(random.expvariate(1/(self.distributiondegree.parameter1)))
            degree = min(degree, novertex)
        if self.distributiondegree.type is DistributionsTypes.geometric:
            degree = round(math.log(random.random())/math.log(self.distributiondegree.parameter1/novertex))
        if self.distributiondegree.type is DistributionsTypes.random:
            degree = random.randint(1, novertex)

        return degree

    def generateComplete(self, name, novertex):
        g = graph.Graph(name, self.directed)
        #Generador de grafos completos
        #vl = list(g.vertices)
        for i in range(novertex):
            #nl = vl
            #nl.remove(i)
            #self.distributiondegree = DistributionsTypes.uniform                
            for j in range(novertex):
                if i!=j:                        
                    weight = self.getweightvalue()
                    g.add_edge(i,j,weight)
        return g
   
    def generateTree(self, name, novertex, degree = None):
        g = graph.Graph(name, self.directed)
        #Generador de arboles
        noedges = novertex-1
        for i in range(novertex):
            nv = graph.Vertex(i, None)
            g.add_vertex(nv)          
        available = list(g.vertices)
        random.shuffle(available)      
        ne = 0
        leaf = []
        iav = available.pop()
        av = g[iav]
        while ne < noedges:
            if degree is None:
                degree = self.getdegreevalue(noedges, novertex)                
            for i in range(degree):
                # if connected 
                if len(available) < 1 or ne >= noedges:
                    break                        
                inv =  available.pop()
                nv = g[inv]
                weight = self.getweightvalue()
                g.add_edge(av,nv,weight)
                leaf.append(inv)
                ne+=1
            if len(leaf) > 0 :
                iav = random.choice(leaf)
                av = g[iav]
                leaf.remove(iav)
            else:
                av = None
                break
        return g

    
    def generateConnected(self,name, novertex, noedges):
        if noedges > novertex -1:
            g = self.generateTree(name, novertex, random.randint(1,novertex))
            ne = novertex-1
            vl = list(g.vertices)
            dv = dict()
            for v in g.vertices:
                dv[v] = self.getdegreevalue(noedges, novertex)
            sd = sum(dv.values)
            ld = noedges - sd 
            if ld > 0:
                rt = ld//novertex
                if rt >0:
                    for v in dv:
                        if dv[v]<novertex:
                            dv[v]+=rt
                
            random.shuffle(vl)           
            #rate = noedges//novertex 
            av = vl.pop()
            used = []
            while ne < noedges:
                #degree = self.getdegreevalue(noedges, novertex)
                #if degree/novertex > 0.5 :
                avl = list(g.vertices)
                avl.remove(av)
                for n in g[av].neighbors:
                    avl.remove(n)
                if len(avl) < degree-len(g[av].neighbors):
                    degree = len(avl)
                random.shuffle(avl)
                
                for i in range(degree-1):
                    print('i',i, degree)
                    nv = avl.pop()                        
                    weight = self.getweightvalue()
                    #print(av,nv)
                    print(ne, noedges, '|', len(avl), degree, '|', av,nv)
                    g.add_edge(av,nv,weight)                    
                    ne+=1
                if len(vl)>0:
                    av = vl.pop()
                else:
                    vl = list(g.vertices)
                    av = vl.pop()
            return g
             
    def generateInstance(self, name, novertex, noedges):
        g = graph.Graph(name, self.directed)
        if self.type is GraphTypes.complete:
            #Generador de grafos completos
            g = self.generateComplete(name, novertex)
        if self.type is GraphTypes.tree:
            #Generador de arboles
            g = self.generateTree(name, novertex)
        if self.type is GraphTypes.connected:
            #Generador de grafos connectados
            g = self.generateConnected(name, novertex, noedges)
        return g
               
