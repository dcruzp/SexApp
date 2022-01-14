from pulp import *
import sexapp as sap





def ExecutePulp():

    ECUT = sap.ECUT
    PGUT= sap.PGUT 
    EIP = sap.EIP
    PIP = sap.PIP
    NPPOO = sap.NPPOO
    



def Optimizing():
    
    
    vector = [55,48,39,72]
    
    prob = LpProblem("TimeOptimizing Problem", LpMaximize)
    for i in vector:
        prob += LpVariable("Var" + str(i), i)
        
    print(prob)
    



Optimizing()