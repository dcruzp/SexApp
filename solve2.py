import pulp as pl
#import sexapp as sap





def Solve2ndProblem():
   # ECUT = sap.ECUT
   # PGUT= sap.PGUT 
   # EIP = sap.EIP
   # PIP = sap.PIP
   # NPPOO = sap.NPPOO
    
    ECUT = [[2,3],[1,4]]
    PGUT= [[4,5],[5,6]] 
    EIP = [300,300]  
    PIP = [5, 5] 
    NPPOO = [1000, 1000]
    Postures= ["postura1", "postura2"]
    Persons= ["persons1", "persons2"]
    Optimizing(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Postures)

    



def Optimizing(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Positions):
    
    problem = pl.LpProblem("Maximizar el placer H",pl.LpMaximize) 
    
    h = pl.LpVariable("H",lowBound=0,cat=pl.LpInteger)
    problem+= h
    
    
    TimepositionVars=[]
    for position in range(len(Positions)):
        TimepositionVars.append(pl.LpVariable(Positions[position],lowBound=1,cat=pl.LpInteger))
        
    
    
    for person in range (len(Persons)):
        
        problem += pl.lpSum(TimepositionVars[position]*PGUT[person][position] for position in range(len(Positions)))  >=h- PIP[person], "placer para : " + str(Persons[person])
        
        problem += pl.lpSum(TimepositionVars[position]*PGUT[person][position] for position in range(len(Positions))) <=  NPPOO[person] - PIP[person], "placer máximo de : "+ str(Persons[person]) 
        
        problem += pl.lpSum( TimepositionVars[position]*ECUT[person][position] for position in range(len(Positions))) >= EIP[person], "Energía de : "+ str(Persons[person])
    
    
    print(problem)
    problem.solve()
    
    
    



Solve2ndProblem()