import pulp as pl 

posturas = ["postura1", "postura2"]
personas = ["Pedro" , "Amanda"]


# placer de personas contra posturas 
# persona  X postura 
personaXplacer = [[4,5],[5,6]]

# enegia que consume persona contra postura 
# persona X energia 
personaXenergia = [[2,3],[1,4]]

# energia inicial de la personas
enegiaInicial = [10,15]  

# placer inicial de las persona 
placerInicial = [200, 300] 

# placer requerido para obtener el orgasmo 
placerRequerido = [150, 200]


problem = pl.LpProblem("Maximizar el tiempo",pl.LpMaximize) 

x_name = ['time1', 'time2']
x = [pl.LpVariable(x_name[i] , lowBound=0, upBound=200) for i in range(len(x_name))]
c = pl.LpAffineExpression([(x[i],1)  for i in range(len(x))])

# 
problem += pl.lpSum([1 * x[i] for i in range(len(x_name))])

for person in range (len(personas)):
  problem += pl.lpSum(personaXplacer[person][i] * x[i] for i in range(len(posturas))) >= placerRequerido[person] - placerInicial[person] , "placer para : " + str(personas[person])


for person in range(len(personas)):
  problem += pl.lpSum(-personaXenergia[person][i] * x[i] for i in range(len(posturas))) <= enegiaInicial[person] , " energia para la persona : " + str(personas[person]) 

print(problem)

problem.solve()

for name, c in list(problem.constraints.items()):
  print(name, ":", c, "\t", c.pi, "\t\t", c.slack)



#Resolviendo el Dual de Esto
x=[]
for i in range(2*len(personas)):
  x.append(pl.LpVariable('Lambda '+ str(i),cat = pl.LpInteger))
        
        
    
    
c = pl.LpAffineExpression([(x[i],enegiaInicial[i]) for i in range(len(x)//2)])
d =pl.LpAffineExpression([(x[(len(x)//2)+j],placerRequerido[j]-placerInicial[j]) for j in range(len(x)//2)])
    
    
DualProblem = pl.LpProblem("Problema Dual",sense=pl.const.LpMinimize)
DualProblem+= c + d

  #For para restricciones del dual
for position in range(len(posturas)):
        
  DualProblem+= pl.lpSum(x[person]*personaXenergia[person][position]+x[person+len(x)//2]*personaXplacer[person][position] for person in range(len(x)//2)) <=0
    
        
        
DualProblem.solve()
for name in DualProblem.variables():
  print(name, " : ", name.varValue)
        

