import pulp as pl


def Solve4thProblem(ECUT,PGUT,PIP,NPPOO,Persons,Postures):
    ECUT = ECUT
    PGUT= PGUT 
    PIP = PIP
    NPPOO = NPPOO
    
    
    # ECUT = [[3,4],[1,4]]
    # PGUT= [[1,2],[5,6]] 
    # EIP = [250,300]  
    # PIP = [100, 5] 
    # NPPOO = [400, 500]
    # Postures= ["postura1", "postura2"]
    # Persons= ["persons1", "persons2"]
    return Optimizing(ECUT,PGUT,PIP,NPPOO,Persons,Postures)
    
def Optimizing(ECUT,PGUT,PIP,NPPOO,Persons,Positions):
        
    problem = pl.LpProblem("Minimizar la energia inicial H",pl.LpMinimize) 
    
    h = pl.LpVariable("H",lowBound=1,cat=pl.LpInteger)
    
   
    EnergyInitialVars=[]
   
    TimepositionVars = []
    for position in range(len(Positions)):
        TimepositionVars.append(pl.LpVariable(Positions[position],lowBound=1,cat=pl.LpInteger))
        
    for person in range(len(Persons)):
        EnergyInitialVars.append(pl.LpVariable(Persons[person],lowBound=0,cat=pl.LpInteger))
    
    problem+= pl.LpAffineExpression([(EnergyInitialVars[i],1)  for i in range(len(EnergyInitialVars))])
    
    for person in range (len(Persons)):
        
        #Por cada tiempoXpostura x cansancioXpostura sumalos y revisa que sean iguales a la energia inicial de la persona menos un valor h
        problem += pl.lpSum(TimepositionVars[position]*ECUT[person][position] for position in range(len(Positions))) == EnergyInitialVars[person] - h, "cansancio de : "+ str(Persons[person])
        
        #Por cada tiempoXpostura x cansancioXpostura sumalos y revisa que sean mayores que cero
        problem += pl.lpSum(TimepositionVars[position]*ECUT[person][position] for position in range(len(Positions))) <= EnergyInitialVars[person], "cansancio de :"+ str(Persons[person])
        
        #Por cada tiempoXpostura x placerXpostura sumalos y revisa que sean mayores que el placer necesario para el orgasmo
        problem += pl.lpSum(TimepositionVars[position]*PGUT[person][position] for position in range(len(Positions))) >= NPPOO[person] - PIP[person], "placer máximo de : "+ str(Persons[person]) 
        
        
        
        
    
    print(problem)
    problem.solve()
    return problem
    print("a")