from gurobipy import *

# conjuntos
tamanos = ["grande", "mediano", "chico"]
sectores = [1, 2, 3, 4]
periodos = [i for i in range(28800 - 1)]
subindices_x = [(sector, tamano) for sector in sectores for tamano in tamanos]
subindices_x = tuplelist(subindices_x)  # para dar subinmdices a variable x
subindices_v = [(sector, t) for sector in sectores for t in periodos]
subindices_v = tuplelist(subindices_v)  # para dar subinmdices a variable v

# parametros
p = {"grande": 280, "mediano": 140, "chico": 70}
q = {"grande": 2, "mediano": 4, "chico": 6}
M = 10 ** 8
cf = {1:1.11,2:2.31,3:2.88,4:3.31} #datos en foto nico wsp
cv = {1:9.98,2:20.85,3:24.21,4:27.33} #datos en foto nico wsp
d = {1:573.1, 2:983.3, 3:1082.4, 4:1275.9} #se usaron datos de IMS con la enumeracion que salía

# Modelo
m = Model("Asignación de Camiones")

#variables
x = m.addVars(subindices_x, vtype=GRB.INTEGER, name="x")
v = m.addVars(subindices_v, vtype=GRB.BINARY, name="v")
f = m.addVars(sectores, vtype=GRB.BINARY, name="f")

m.setObjective(sum(
    cf[i] * f[i] + sum(v[i, t] * cv[i] for t in periodos) for i in sectores),
    GRB.MINIMIZE)

m.addConstrs((x.sum('*', c) <= q[c] for c in tamanos),
             "Cantidad Máxima Camiones")  # 3 primeras restricciones

m.addConstrs((1 - v[i, t] <= sum(
    (sum(x[i, c] * p[c] for c in tamanos)) / (28800 * d[i]) for u in
    periodos) for i in sectores for t in periodos), "Activacion v-1")

m.addConstrs((sum(
    sum(x[i, c] * p[c] for c in tamanos) for u in range(t)) / 28800 - d[
                  i] <= M * (1 - v[i, t]) for i in sectores for t in
              periodos), "Activacion v-2")

m.addConstrs(
    (1 - f[i] <= sum(x[i, c] * p[c] for c in tamanos) / d[i] for i in
     sectores for t in periodos), "Activacion f-1")

m.addConstrs(
    (sum(x[i, c] * p[c] for c in tamanos) <= M * (1 - f[i]) for i in
     sectores for t in periodos), "Activacion f-2")

#revisar esta ultima parte
m.optimize()
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))
print(f'\nValor Objetivo: {abs(m.objVal)}')
