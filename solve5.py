import pulp as pl


def Solve4thProblem(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Postures,SpecificPersonIndex):
    ECUT = ECUT
    PGUT= PGUT 
    EIP = EIP
    PIP = PIP
    NPPOO = NPPOO
    
    
    hECUT= ECUT[SpecificPersonIndex]
    ECUT.Pop(SpecificPersonIndex)
    
    PersonName = Persons[SpecificPersonIndex]
    Persons.Pop(SpecificPersonIndex)

    hPGUT = PGUT[SpecificPersonIndex]
    PGUT.Pop(SpecificPersonIndex)
    
    hEIP = EIP[SpecificPersonIndex]
    EIP.Pop(SpecificPersonIndex)
    
    hPIP = PIP[SpecificPersonIndex] 
    PIP.Pop(SpecificPersonIndex) 
    
    hNPOO = NPPOO[SpecificPersonIndex]
    NPPOO.Pop(SpecificPersonIndex)
    
    # hPGUT=[4,5]
    # hEIP=300
    # hNPOO=500
    
    # ECUT = [[2,3],[1,4]]
    # PGUT= [[4,5],[5,6]] 
    # EIP = [300,300]  
    # PIP = [5, 5] 
    # NPPOO = [500, 500]
    # Postures= ["postura1", "postura2"]
    # Persons= ["persons1", "persons2"]
    Optimizing(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Postures,hECUT,hPGUT,hEIP,hNPOO)
    
def Optimizing(ECUT,PGUT,EIP,PIP,NPPOO,Persons,Positions,hECUT,hPGUT,hEIP,hNPOO):
        
    problem = pl.LpProblem("Maximizar el placer H",pl.LpMaximize) 
    
    h = pl.LpVariable("H",lowBound=0,cat=pl.LpInteger)
    problem+= h
    
    
    TimepositionVars=[]
    for position in range(len(Positions)):
        TimepositionVars.append(pl.LpVariable(Positions[position],lowBound=1,cat=pl.LpInteger))
        
    
    
    for person in range (len(Persons)):
        
        
        #Por cada tiempoXpostura x cansancioXpostura sumalos y revisa que sean mayores que cero
        problem+= pl.lpSum(TimepositionVars[position]*ECUT[person][position] for position in range(len(Positions))) <= EIP[person], "cansancio de :"+ str(Persons[person])
        
        #Por cada tiempoXpostura x placerXpostura sumalos y revisa que sean mayores que el placer necesario para el orgasmo
        problem += pl.lpSum(TimepositionVars[position]*PGUT[person][position] for position in range(len(Positions))) >= NPPOO[person] - PIP[person], "placer máximo de : "+ str(Persons[person]) 
    
    #participante marginado
    
    #por cada tiempoXpostura x placerXpostura sumalos y revisa que sean menores que el placer para el orgasmo menos h
    problem+= pl.lpSum(TimepositionVars[position]*hPGUT[position] for position in range(len(Positions))) <= hNPOO-1-h ,"placer máximo de : marginado" 
    
    #h es menor que el placer necesario para el orgasmo (quizas es innecesaria)
    problem+= hNPOO-1>=h    
    
    #por cada tiempoXpostura x placerXpostura sumalos y revisa que sean menores qu la energia inicial
    problem+= pl.lpSum(TimepositionVars[position]*hECUT[position] for position in range(len(Positions))) <=hEIP ,"cansancio de : marginado"
    
    print(problem)
    problem.solve()
    print("a")
    
    
    
Solve5thProblem()

print("")
    
   