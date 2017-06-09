import grasptsp
import graph
import InstanciesGenerator
import TSPproblem

#dd = InstanciesGenerator.Distribution(InstanciesGenerator.DistributionsTypes.uniform, 10, 2)
#dw = InstanciesGenerator.Distribution(InstanciesGenerator.DistributionsTypes.uniform, 1, 10)
#generador = InstanciesGenerator.GraphInstancesGenerator(graphtype = InstanciesGenerator.GraphTypes.complete,distribution_weight = dw,distribution_degree = dd, directed = False )
#g = generador.generateInstance('Test', 5, 20)

#prob = TSPproblem.TSPProblem()
#print(prob.graph.to_string())
path='instancies/att48.txt'
s = grasptsp.graspTSP( 10, 0.3, path=path, key='distance')

print(s[0], s[1])
