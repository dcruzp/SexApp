import pulp as pl 

# posturas = ["postura1", "postura2"]
# personas = ["Pedro" , "Amanda"]


# placer de personas contra posturas 
# persona  X postura 
# personaXplacer = [[4,5],[5,6]]

# enegia que consume persona contra postura 
  # # persona X energia 
  # personaXenergia = [[2,3],[1,4]]
  
  # # energia inicial de la personas
  # enegiaInicial = [100,60]  
  
  # # placer inicial de las persona 
  # placerInicial = [20, 15] 
  
  # # placer requerido para obtener el orgasmo 
  # placerRequerido = [150, 200]
  
def Solve1stProblem(ECUT,PGUT,EIP,PIP,NPPOO,personas,posturas):
  problem = pl.LpProblem("Maximizar el tiempo",pl.LpMaximize) 
  
  x_name = posturas
  x = [pl.LpVariable(x_name[i] , lowBound=1) for i in range(len(x_name))]
  c = pl.LpAffineExpression([(x[i],1)  for i in range(len(x))])
  
  # 
  problem += pl.lpSum([1 * x[i] for i in range(len(x_name))])
  
  for person in range (len(personas)):
    problem += pl.lpSum(PGUT[person][i] * x[i] for i in range(len(posturas))) >= NPPOO[person] - PIP[person] , "placer para : " + str(personas[person])
  
  
  for person in range(len(personas)):
    problem += pl.lpSum(ECUT[person][i] * x[i] for i in range(len(posturas))) <= EIP[person] , " energia para la persona : " + str(personas[person]) 
  
  print(problem)
  
  problem.solve()
  
  
  for name in problem.variables():
    print(name, " : ", name.varValue)
  
  
  
  for name, c in list(problem.constraints.items()):
    print(name, ":", c, "\t", c.pi, "\t\t", c.slack)
  
  return problem
  
  
  #Resolviendo el Dual de Esto
  # x=[]
  # for i in range(2*len(Persons)):
  #   if i >= len(Persons):
  #     x.append(pl.LpVariable('Lambda '+ str(i),lowBound= 1 , cat = pl.LpInteger))
  #   else:
  #     x.append(pl.LpVariable('Lambda '+ str(i),upBound = 1 , cat = pl.LpInteger))
          
          
      
      
  # c = pl.LpAffineExpression([(x[i],EIP[i]) for i in range(len(x)//2)])
  # d =pl.LpAffineExpression([(x[(len(x)//2)+j],NPPOO[j]-PIP[j]) for j in range(len(x)//2)])
      
      
  # DualProblem = pl.LpProblem("Problema Dual",pl.LpMinimize)
  # DualProblem+= c + d
  
  #   #For para restricciones del dual
  # for position in range(len(posturas)):
          
  #   DualProblem+= pl.lpSum(x[person]*ECUT[person][position]+x[person+len(x)//2]*PGUT[person][position] for person in range(len(x)//2)) >=1
      
          
          
  # DualProblem.solve()
  # print(DualProblem)
  
  # for name, c in list(DualProblem.constraints.items()):
  #   print(name, ":", c, "\t", c.pi, "\t\t", c.slack)
  
  # for name in DualProblem.variables():
  #   print(name, " : ", name.varValue)
          
  
  