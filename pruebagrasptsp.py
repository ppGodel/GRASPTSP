import grasptsp
import graph
import InstanciesGenerator

dd = InstanciesGenerator.Distribution(InstanciesGenerator.DistributionsTypes.uniform, 10, 2)
dw = InstanciesGenerator.Distribution(InstanciesGenerator.DistributionsTypes.uniform, 1, 10)
generador = InstanciesGenerator.GraphInstancesGenerator(graphtype = InstanciesGenerator.GraphTypes.complete,distribution_weight = dw,distribution_degree = dd, directed = False )
g = generador.generateInstance('Test', 5, 90)

s = grasptsp.graspTSP(g, 10, 0.3)

print(s[0], s[1])
