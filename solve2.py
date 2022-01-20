import pulp as pl
#import sexapp as sap
# ECUT = [[2,3],[1,4]]
# PGUT= [[3,500],[5,6]] 
# EIP = [300,300]  
# PIP = [1000, 5] 
# NPPOO = [1000, 1000]
# Postures= ["postura1", "postura2"]
# Persons= ["persons1", "persons2"]




def Solve2ndProblem(ECUT,PGUT,EIP,NPPOO,PIP,Persons,Postures):
    # ECUT = ECUT
    # PGUT= PGUT 
    # EIP = EIP
    # PIP = PIP
    # NPPOO = NPPOO

    # ECUT = [[2,3],[1,4]]
    # PGUT= [[4,5],[5,6]] 
    # EIP = [300,300]  
    # PIP = [5, 5] 
    # NPPOO = [1000, 1000]
    # Postures= ["postura1", "postura2"]
    # Persons= ["persons1", "persons2"]
    return Optimizing(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Postures)





def Optimizing(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Positions):
    
    problem = pl.LpProblem("Maximizar el placer H",pl.LpMaximize) 
    
    h = pl.LpVariable("H",lowBound=0,cat=pl.LpInteger)
    problem+= h
    
    
    TimepositionVars=[]
    for position in range(len(Positions)):
        TimepositionVars.append(pl.LpVariable(Positions[position],lowBound=1,cat=pl.LpInteger))
        
    
    #por cada persona
    for person in range (len(Persons)):
        #Por cada tiempoXpostura x placerXpostura sumalos y revisa que sean mayores que una variable de decision h menos el placer inicial
        problem += pl.lpSum(TimepositionVars[position]*PGUT[person][position] for position in range(len(Positions)))  >=h- PIP[person], "placer para : " + str(Persons[person])
        #Por cada tiempoXpostura x placerXpostura sumalos y revisa que sean mayores que el placer necesario para el orgasmo
        problem += pl.lpSum(TimepositionVars[position]*PGUT[person][position] for position in range(len(Positions))) >=  NPPOO[person] - PIP[person], "placer máximo de : "+ str(Persons[person]) 
        #Por cada tiempoXpostura x cansancioXpostura sumalos y revisa que sean menores que la energia inicial de la persona
        problem += pl.lpSum( TimepositionVars[position]*ECUT[person][position] for position in range(len(Positions))) <= EIP[person], "Energía de : "+ str(Persons[person])
    
    print(problem)
    problem.solve()
        
    
    
    for name in problem.variables():
        print(name, " : ", name.varValue)
    
    

    for name, c in list(problem.constraints.items()):
        print(name, ":", c, "\t", c.pi, "\t\t", c.slack)
        

        
    
    
    return problem



# Solve2ndProblem(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Postures)
    
    



# Solve2ndProblem()