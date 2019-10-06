from tools import *
from parameters import *
from time import sleep

# Se carga la informacion de los camiones, cajeros y cassetes
camiones = carga_camiones()
cajeros = carga_cajeros()
cassetes = carga_cassetes()

# Parte el lunes en la mañana y se piden cuantos dias se quieren simular
numero_de_días = int(input('Ingrese el numero de dias: '))
cantidad_de_turnos = numero_de_días*3
turnos_completados = 0
turno = 'Manana'
dia = 'Lunes'

# Se recargan todos los cajeros con esa cantidad de plata
plata_inicial = plata_a_recargar = float(input('Ingrese la plata con que parten todos los cajeros: '))
for llave in cajeros:
    if llave != 'Bodega':
        cajeros[llave]['Plata actual'] += plata_a_recargar

# Se definen las listas donde estaran los cajeros
cajeros_en_stock_out = []
cajeros_a_stock_out = [] # Sirve de referencia, no se recorre
cajeros_a_visitar = []
cajeros_con_plata = [llave for llave in cajeros.keys() if llave != 'Bodega']

# Se definen las listas donde estaran los camiones
camiones_en_bodega = [llave_camion for llave_camion in camiones.keys()]
camiones_en_camino = []
camiones_recargando = []
camiones_en_decision = []

# Se recorre turno a turno
while turnos_completados < cantidad_de_turnos:

    tiempo_actual = 0
    tiempo_final = 8*3600 # 8 horas en segundos

    # Ve la disponibilidad de todos los cajeros
    cajeros_disponibles = disponibilidad(cajeros, dia, turno)

    # Agrega los cajeros en stock out disponible a los cajeros a visitar ese dia
    for llave_cajero in cajeros.keys():
        if llave_cajero != 'Bodega':
            if cajeros[llave_cajero]['Estado'] == 'Stock Out':
                if llave_cajero in cajeros_disponibles:
                    cajeros_a_visitar.append(llave_cajero)


    # Agrega los cajeros que quedaran en stock out disponible a los cajeros a visitar ese dia
    for llave_cajero in cajeros:
        if llave_cajero != 'Bodega':
            if (cajeros[llave_cajero]['Promedio diario de retiro'] / 3 > cajeros[llave_cajero]['Plata actual']):
                # cajeros_a_stock_out.append(llave_cajero) 
                if llave_cajero in cajeros_disponibles:
                    cajeros_a_visitar.append(llave_cajero)
    
    print(f'''======= Turno {turnos_completados + 1} [{dia}, {turno}] =======''')

    # Se recorre segundo a segundo el turno
    while tiempo_actual < tiempo_final: 

        # Se recorren los camiones en las bodegas para ver si es que alguno puede ir a recargar un cajero
        for llave_camion in camiones_en_bodega:
            for llave_cajero in cajeros_a_visitar:
                if camiones[llave_camion]['Tiempo maximo'] >= (2*distancia(cajeros['Bodega'], cajeros[llave_cajero])*3.6/velocidad_camion + cajeros[llave_cajero]['Duracion de la recarga']*3600):
                    cajeros_a_visitar.remove(llave_cajero)
                    camiones_en_bodega.remove(llave_camion)
                    camiones_en_camino.append(llave_camion)
                    camiones[llave_camion]['Plata en camion'] = camiones[llave_camion]['Carga maxima plata']
                    camiones[llave_camion]['Objetivo'] = llave_cajero
                    camiones[llave_camion]['Tiempo en llegar a objetivo'] = round(distancia(cajeros['Bodega'], cajeros[llave_cajero])*3.6/velocidad_camion, 0)
                    break

        #  Se recorren los camiones recien listos y se decide a donde mandarlos
        for llave_camion in camiones_en_decision:
            volver_bodega = 'Si'
            for llave_cajero in cajeros_a_visitar:
                if (camiones[llave_camion]['Tiempo maximo'] - camiones[llave_camion]['Tiempo en movimiento'])>= (distancia(cajeros[camiones[llave_camion]['Objetivo']], cajeros[llave_cajero])*3.6/velocidad_camion  + cajeros[llave_cajero]['Duracion de la recarga']*3600 + distancia(cajeros['Bodega'], cajeros[llave_cajero])*3.6/velocidad_camion ):
                    if camiones[llave_camion]['Plata en camion'] >= 35:
                        cajeros_a_visitar.remove(llave_cajero)
                        camiones_en_decision.remove(llave_camion)
                        camiones_en_camino.append(llave_camion)
                        camiones[llave_camion]['Plata en camion'] = camiones[llave_camion]['Carga maxima plata']
                        camiones[llave_camion]['Tiempo en llegar a objetivo'] = round(distancia(cajeros[camiones[llave_camion]['Objetivo']], cajeros[llave_cajero])*3.6/velocidad_camion, 0)
                        camiones[llave_camion]['Objetivo'] = llave_cajero
                        volver_bodega = 'No'
                        break
            if volver_bodega == 'Si':
                camiones_en_decision.remove(llave_camion)
                camiones_en_camino.append(llave_camion)
                camiones[llave_camion]['Tiempo en llegar a objetivo'] = round(distancia(cajeros[camiones[llave_camion]['Objetivo']], cajeros['Bodega'])*3.6/velocidad_camion, 0)
                camiones[llave_camion]['Objetivo'] = 'Bodega'

        # Se recorren los camiones en camino
        for llave_camion in camiones_en_camino:
            if camiones[llave_camion]['Tiempo en llegar a objetivo'] == 0:
                if camiones[llave_camion]['Objetivo'] == 'Bodega':
                    camiones[llave_camion]['Tiempo en movimiento'] = 0
                    camiones_en_bodega.append(llave_camion)
                    camiones[llave_camion]['Plata en camion'] = 0
                else:
                    camiones[llave_camion]['Tiempo en llegar a objetivo'] = round(cajeros[camiones[llave_camion]['Objetivo']]['Duracion de la recarga']*3600, 0)
                    camiones_recargando.append(llave_camion)
                    cajeros[camiones[llave_camion]['Objetivo']]['Estado'] = 'Recarga'
                camiones_en_camino.remove(llave_camion)
            else:
                camiones[llave_camion]['Tiempo en llegar a objetivo'] -= 1
            camiones[llave_camion]['Tiempo en movimiento'] += 1
            camiones[llave_camion]['Costo traslado acumulado'] += (55 / 3600) * costo_traslado

        # Se recorren los camiones cargando
        for llave_camion in camiones_recargando:
            if camiones[llave_camion]['Tiempo en llegar a objetivo'] == 0:
                cajeros[camiones[llave_camion]['Objetivo']]['Plata actual'] = 35
                cajeros[camiones[llave_camion]['Objetivo']]['Estado'] = 'Normal'
                camiones_recargando.remove(llave_camion)
                camiones_en_decision.append(llave_camion)
            else:
                camiones[llave_camion]['Tiempo en llegar a objetivo'] -= 1
            camiones[llave_camion]['Tiempo en movimiento'] += 1

        # Se recorren los cajeros:
        for llave_cajero in cajeros.keys():
            if llave_cajero != 'Bodega':
                if cajeros[llave_cajero]['Estado'] == 'Normal':
                    if cajeros[llave_cajero]['Plata actual'] <= 0:
                        cajeros[llave_cajero]['Plata actual'] = 0
                        cajeros[llave_cajero]['Estado'] = 'Stock Out'
                        cajeros[llave_cajero]["Costo fijo acumulado stock out"] += cajeros[llave_cajero]['Costo fijo por Stock Out']
                    else:
                        cajeros[llave_cajero]['Plata actual'] -= cajeros[llave_cajero]['Promedio diario de retiro'] / (24*3600)
                    pass
                elif cajeros[llave_cajero]['Estado'] == 'Recarga':
                    pass
                elif cajeros[llave_cajero]['Estado'] == 'Stock Out':
                    cajeros[llave_cajero]["Costo variable acumulado stock out"] += cajeros[llave_cajero]['Costo variable por Stock Out']/60
            
        # Se avanza el tiempo
        tiempo_actual += 1

    # Se avanza de turno
    turnos_completados += 1
    if turno == 'Noche':
        dia = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'][(['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'].index(dia) + 1)%7]
    turno = ['Manana', 'Tarde', 'Noche'][(['Manana', 'Tarde', 'Noche'].index(turno) + 1)%3]

    # Se limpia los cajeros a visitar para el proximo turno
    cajeros_a_visitar = []

# Se obtienen los resultados
suma_fijo = 0
suma_variable = 0
suma_traslado = 0
for llave_cajero in cajeros:
    if llave_cajero != 'Bodega':
        suma_fijo += cajeros[llave_cajero]['Costo fijo por Stock Out']
        suma_variable += cajeros[llave_cajero]["Costo variable acumulado stock out"]
for llave_camion in camiones:
    suma_traslado += camiones[llave_camion]['Costo traslado acumulado']
print(f"""


----------------------------------------------------

> Total costo variable Stock Out: MM${suma_variable}.
> Total costo fijo Stock Out: MM${suma_fijo}
> Total en traslado: MM${suma_traslado}

TOTAL> MM${suma_variable + suma_fijo + suma_traslado}
""" )





