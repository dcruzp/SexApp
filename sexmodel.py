import global_Sex as gs
import numpy as np

from scipy.optimize import linprog

#Este problema se centra en encontrar que tiempo se
#debe estar en cada postura para que el tiempo del acto
#sexual sea el mayor posible.
def Model_1():
    restr = Res1(gs.Pij, gs.Aij, gs.Ei, gs.Ti, gs.PO_i, gs.Per, gs.Post)

    A_ub = restr[0]
    b_ub = restr[1]
    A_eq = restr[2]
    b_eq = restr[3]

    res = linprog(SumTime, A_ub = A_ub, b_ub = b_ub, A_eq = A_eq, b_eq = b_eq, bounds = (0,None))

    print(restr)

def SumTime(T):
    return np.sum(T)

def Res1(Pij, Aij, Ei, Ti, PO_i, Per, Post):
    A_ub = []
    b_ub = []
    
    A_eq = []
    b_eq = []
    
    for i in range(0,len(Per)-1):
        value = []
        for j in range(0,len(Post)-1):
            value.append(-Pij[j][i])
        A_ub.append(value)
        b_ub.append(-PO_i[i])
        
    for i in range(0,len(Per)-1):
        value = []
        for j in range(0,len(Post)-1):
            value.append(Aij[j][i])
        A_ub.append(value)
        b_ub.append(Ei[i])
        
    return [A_ub, b_ub, A_eq, b_eq]

def Model_2():
    restr = Res2(gs.Pij, gs.Aij, gs.Ei, gs.Ti, gs.PO_i, gs.Per, gs.Post)

    A_ub = restr[0]
    b_ub = restr[1]
    A_eq = restr[2]
    b_eq = restr[3]

    res = linprog(FunModel2, A_ub = A_ub, b_ub = b_ub, A_eq = A_eq, b_eq = b_eq, bounds = (0,None))

    print(restr)

def FunModel2(h):
    return h

def Res2(Pij, Aij, Ei, Ti, PO_i, Per, Post):
    A_ub = []
    b_ub = []
    
    A_eq = []
    b_eq = []
    
    for i in range(0,len(Per)-1):
        value = []
        for j in range(0,len(Post)-1):
            value.append(-Pij[j][i])
        A_ub.append(value)
        b_ub.append(-PO_i[i])
        
    for i in range(0,len(Per)-1):
        value = []
        for j in range(0,len(Post)-1):
            value.append(Aij[j][i])
        A_ub.append(value)
        b_ub.append(Ei[i])
        
    return [A_ub, b_ub, A_eq, b_eq]

def Model_3():
    return

def Model_4():
    return

def Model_5():
    return

def Model_6():
    return