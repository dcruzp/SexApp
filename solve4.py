import pulp as pl

def Solve4thProblem():
   # ECUT = sap.ECUT
   # PGUT= sap.PGUT 
   # EIP = sap.EIP
   # PIP = sap.PIP
   # NPPOO = sap.NPPOO
    
    ECUT = [[2,3],[1,4]]
    PGUT= [[4,5],[5,6]] 
    EIP = [300,300]  
    PIP = [5, 5] 
    NPPOO = [500, 500]
    Postures= ["postura1", "postura2"]
    Persons= ["persons1", "persons2"]
    Optimizing(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Postures)
    
def Optimizing(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Positions):
        
    problem = pl.LpProblem("Minimizar la energia H",pl.LpMinimize) 
    
    h = pl.LpVariable("H",lowBound=0,cat=pl.LpInteger)
    problem+= h
    
    
    TimepositionVars=[]
    EnergyInitialVars=[]
    for position in range(len(Positions)):
        TimepositionVars.append(pl.LpVariable(Positions[position],lowBound=1,cat=pl.LpInteger))
        
    for person in range(len(Persons)):
        EnergyInitialVars.append(pl.LpVariable(Persons[person],lowBound=1,cat=pl.LpInteger))
    
    
    for person in range (len(Persons)):
        
        #Por cada tiempoXpostura x cansancioXpostura sumalos y revisa que sean iguales a la energia inicial de la persona menos un valor h
        problem += pl.lpSum(TimepositionVars[position]*ECUT[person][position] for position in range(len(Positions))) == EnergyInitialVars[person]- h, "cansancio de : "+ str(Persons[person])
        
        #Por cada tiempoXpostura x cansancioXpostura sumalos y revisa que sean mayores que cero
        problem += pl.lpSum(TimepositionVars[position]*ECUT[person][position] for position in range(len(Positions))) <= EnergyInitialVars[person], "cansancio de :"+ str(Persons[person])
        
        #Por cada tiempoXpostura x placerXpostura sumalos y revisa que sean mayores que el placer necesario para el orgasmo
        problem += pl.lpSum(TimepositionVars[position]*PGUT[person][position] for position in range(len(Positions))) >= NPPOO[person] - PIP[person], "placer máximo de : "+ str(Persons[person]) 
        
        
        
        
    
    print(problem)
    problem.solve()
    print("a")
    
    
    
Solve4thProblem()

print("")
    
   