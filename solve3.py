import pulp as pl


def Solve3rdProblem(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Postures):
    # ECUT = ECUT
    # PGUT= PGUT 
    # EIP = EIP
    # PIP = PIP
    # NPPOO = NPPOO
    
    # ECUT = [[2,3],[1,4]]
    # PGUT= [[4,5],[5,6]] 
    # EIP = [300,300]  
    # PIP = [5, 5] 
    # NPPOO = [500, 500]
    # Postures= ["postura1", "postura2"]
    # Persons= ["persons1", "persons2"]
    return Optimizing(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Postures)
    
    
    
def Optimizing(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Positions):
    
    problem = pl.LpProblem("Maximizar la enrgía H",pl.LpMaximize) 
    
    h = pl.LpVariable("H",lowBound=0,cat=pl.LpInteger)
    problem+= h
    
    
    TimepositionVars=[]
    for position in range(len(Positions)):
        TimepositionVars.append(pl.LpVariable(Positions[position],lowBound=1,cat=pl.LpInteger))
        
    
    #por cada persona
    for person in range (len(Persons)):
        
        #Por cada tiempoXpostura x cansancioXpostura sumalos y revisa que sean menores que una variable h menos la enrgia inicial de la persona
        problem += pl.lpSum(TimepositionVars[position]*ECUT[person][position] for position in range(len(Positions))) <= - h + EIP[person], "cansancio de : " + str(Persons[person])
        #Por cada tiempoXpostura x placerXpostura sumalos y revisa que sean mayores que el placer necesario para el orgasmo
        problem += pl.lpSum(TimepositionVars[position]*PGUT[person][position] for position in range(len(Positions))) >= NPPOO[person] - PIP[person], "placer máximo de : "+ str(Persons[person]) 
        #por cada tiempoXpostura x cansancioXpostura sumalos y revisa que sean menores que la energia inicial de la persona
        problem += pl.lpSum( TimepositionVars[position]*ECUT[person][position] for position in range(len(Positions))) <= EIP[person], "Energía de : "+ str(Persons[person])
        
        
    
    print(problem)
    problem.solve()
    return problem
    print("a")

    
    
