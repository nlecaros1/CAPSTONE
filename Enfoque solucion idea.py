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

# Se crean listas donde se guarda la información para luego mostrar
historial_general = ['+-------------+ \n', '| Simbologia: | \n', '| - Camiones  | \n', '| * Cajeros   | \n', '+-------------+ \n', '\n', f'Simulacion de {numero_de_días} con plata inicial de MM$ {plata_inicial}.\n', '\n']
historial_por_turno = []


# Se definen las listas donde estaran los cajeros
cajeros_a_visitar = []

# Se definen las listas donde estaran los camiones
camiones_en_bodega = [llave_camion for llave_camion in camiones.keys()]
camiones_en_camino = []
camiones_recargando = []
camiones_en_decision = []
semana = 0

# Se recorre turno a turno
while turnos_completados < cantidad_de_turnos:


    # Se setean als variables iniciales
    tiempo_actual = 0
    tiempo_final = 8*3600 # 8 horas en segundos
    historial_por_turno = [f'''{dia}-{turno} \n''']

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
    cajeros_a_visitar = ponderador(cajeros, cajeros_disponibles, dia, turno)

    
    print(f'''======= Turno {turnos_completados + 1} [{dia}, {turno}] =======''')

    # Se agrega nueva semana si corresponde
    if dia =='Lunes' and turno == 'Manana':
        semana += 1
        historial_general.append('Semana '+ str(semana) + '\n')
    draw_by_turn_initial(cajeros, cajeros_a_visitar, semana, dia, turno)








    for llave_cajero in cajeros_a_visitar:
        tiempo_actual = 10000000000000000
        for llave_camion in camiones:
            alguno = 'no'
            if camiones[llave_camion]["Tiempo simulacion"] < tiempo_actual:
                tiempo_actual = camiones[llave_camion]["Tiempo simulacion"]



        for llave_camion in camiones:

            if (camiones[llave_camion]['Tiempo maximo'] - camiones[llave_camion]['Tiempo en simulacion']) <= distancia_minima_cajero_bodega:
                opcion = (distancia(cajeros[camiones[llave_camion]['Cajero simulacion']], cajeros['Bodega']) + distancia(cajeros['Bodega'], cajeros[llave_cajero]))*3.6/velocidad_camion + (camiones[llave_camion]["Tiempo simulacion"] - tiempo_actual)
                camiones[llave_camion]['Tiempo en simulacion'] = 0
                camiones[llave_camion]["Tiempo simulacion"] += distancia(cajeros[camiones[llave_camion]['Cajero simulacion']], cajeros['Bodega'])*3.6/velocidad_camion
                camiones[llave_camion]['Pre historial'].append('Bodega')
            else:
                opcion = distancia(cajeros[camiones[llave_camion]['Cajero simulacion']], cajeros[llave_cajero])*3.6/velocidad_camion + (camiones[llave_camion]["Tiempo simulacion"] - tiempo_actual)
            if (camiones[llave_camion]['Tiempo maximo'] - camiones[llave_camion]['Tiempo en simulacion']) >= ((distancia(cajeros[llave_cajero], cajeros[camiones[llave_camion]['Cajero simulacion']]) + distancia(cajeros['Bodega'], cajeros[llave_cajero]))*3.6/velocidad_camion  + cajeros[llave_cajero]['Duracion de la recarga']*3600):
                alguno = "si"
                if cajeros[llave_cajero]['Camion simulacion'] == "ninguno":
                    cajeros[llave_cajero]['Camion simulacion'] = llave_camion
                    cajeros[llave_cajero]['Opcion'] = opcion
                    cajeros[llave_cajero]['Tiempo_a_agregar'] =  distancia(cajeros['Bodega'], cajeros[llave_cajero])*3.6/velocidad_camion + cajeros[llave_cajero]['Duracion de la recarga']*3600
                if opcion <= cajeros[llave_cajero]['Opcion']:
                    cajeros[llave_cajero]['Camion simulacion'] = llave_camion
                    cajeros[llave_cajero]['Opcion'] = opcion
                    cajeros[llave_cajero]['Tiempo_a_agregar'] =  distancia(cajeros['Bodega'], cajeros[llave_cajero])*3.6/velocidad_camion + cajeros[llave_cajero]['Duracion de la recarga']*3600







        if alguno == 'no':
            print("================================================================")
            print('ERROR')
            print(f'''{llave_cajero}: ''')
            for llave_camion in camiones_en_bodega:
                print(f'''  {llave_camion}: tiempo: {camiones[llave_camion]['Tiempo maximo'] - camiones[llave_camion]['Tiempo en simulacion']}. Llega a cajero: {distancia(cajeros[llave_cajero], cajeros[camiones[llave_camion]['Cajero simulacion']])*3.6/velocidad_camion}  Llega a bodega: { distancia(cajeros['Bodega'], cajeros[llave_cajero])*3.6/velocidad_camion }  Recarga: {cajeros[llave_cajero]['Duracion de la recarga']*3600}   Final: {((distancia(cajeros[llave_cajero], cajeros[camiones[llave_camion]['Cajero simulacion']]) + distancia(cajeros['Bodega'], cajeros[llave_cajero]))*3.6/velocidad_camion  + cajeros[llave_cajero]['Duracion de la recarga']*3600)}''')
            print("================================================================")

        camion_a_ocupar = cajeros[llave_cajero]['Camion simulacion'] 
        camiones[camion_a_ocupar]['Cajero simulacion'] = llave_cajero
        camiones[camion_a_ocupar]["Tiempo simulacion"] += cajeros[llave_cajero]['Tiempo_a_agregar']
        camiones[camion_a_ocupar]['Tiempo en simulacion'] += cajeros[llave_cajero]['Tiempo_a_agregar']
        camiones[camion_a_ocupar]['Pre historial'].append(llave_cajero)
        
    for llave_camion in camiones:
        camiones[llave_camion]["Tiempo simulacion"] = 0
        camiones[llave_camion]["Tiempo en simulacion"] = 0
        camiones[llave_camion]['Cajero simulacion'] = 'Bodega'



    # Se recorre segundo a segundo el turno
    while tiempo_actual < tiempo_final: 

        # Se recorren los camiones en las bodegas para ver si es que alguno puede ir a recargar un cajero
        for llave_camion in camiones_en_bodega:
            for llave_cajero in cajeros_a_visitar:
                if camiones[llave_camion]['Tiempo maximo'] >= (2*distancia(cajeros['Bodega'], cajeros[llave_cajero])*3.6/velocidad_camion + cajeros[llave_cajero]['Duracion de la recarga']*3600) and cajeros[llave_cajero]['Camion simulacion'] == llave_camion:
                    cajeros_a_visitar.remove(llave_cajero)
                    camiones_en_bodega.remove(llave_camion)
                    camiones_en_camino.append(llave_camion)
                    camiones[llave_camion]['Plata en camion'] = camiones[llave_camion]['Carga maxima plata']
                    camiones[llave_camion]['Objetivo'] = llave_cajero
                    camiones[llave_camion]['Tiempo en llegar a objetivo'] = round(distancia(cajeros['Bodega'], cajeros[llave_cajero])*3.6/velocidad_camion, 0)
                    historial_por_turno.append(f'''[{hora(tiempo_actual)[0]}] - {llave_camion} va al {llave_cajero}. \n''')
                    # camiones[llave_camion]['Tiempo en simulacion'] += (camiones[llave_camion]['Tiempo en llegar a objetivo'] + cajeros[llave_cajero]['Duracion de la recarga']*3600)
                    break

        #  Se recorren los camiones recien listos y se decide a donde mandarlos
        for llave_camion in camiones_en_decision:
            volver_bodega = 'Si'
            caso = 'No hay cajeros que recargar.'
            for llave_cajero in cajeros_a_visitar:
                if (camiones[llave_camion]['Tiempo maximo'] - camiones[llave_camion]['Tiempo en movimiento'])>= (distancia(cajeros[camiones[llave_camion]['Objetivo']], cajeros[llave_cajero])*3.6/velocidad_camion  + cajeros[llave_cajero]['Duracion de la recarga']*3600 + distancia(cajeros['Bodega'], cajeros[llave_cajero])*3.6/velocidad_camion ) and cajeros[llave_cajero]['Camion simulacion'] == llave_camion:
                    if camiones[llave_camion]['Plata en camion'] >= 35:
                        cajeros_a_visitar.remove(llave_cajero)
                        camiones_en_decision.remove(llave_camion)
                        camiones_en_camino.append(llave_camion)
                        camiones[llave_camion]['Plata en camion'] = camiones[llave_camion]['Carga maxima plata']
                        camiones[llave_camion]['Tiempo en llegar a objetivo'] = round(distancia(cajeros[camiones[llave_camion]['Objetivo']], cajeros[llave_cajero])*3.6/velocidad_camion, 0)
                        camiones[llave_camion]['Objetivo'] = llave_cajero
                        volver_bodega = 'No'
                        historial_por_turno.append(f'''[{hora(tiempo_actual)[0]}] - {llave_camion} va al {llave_cajero}. \n''')
                        break
                    else:
                        caso = 'No tiene plata'
                else:
                    caso = 'No alcanza a ir'
            if volver_bodega == 'Si':
                camiones[llave_camion]['Historial'].append(('Bodega', tiempo_actual))
                camiones_en_decision.remove(llave_camion)
                camiones_en_camino.append(llave_camion)
                camiones[llave_camion]['Tiempo en llegar a objetivo'] = round(distancia(cajeros[camiones[llave_camion]['Objetivo']], cajeros['Bodega'])*3.6/velocidad_camion, 0)
                camiones[llave_camion]['Objetivo'] = 'Bodega'
                historial_por_turno.append(f'''[{hora(tiempo_actual)[0]}] - {llave_camion} va a la Bodega. {caso}. \n''')

        # Se recorren los camiones en camino
        for llave_camion in camiones_en_camino:
            if camiones[llave_camion]['Tiempo en llegar a objetivo'] == 0:
                if camiones[llave_camion]['Objetivo'] == 'Bodega':
                    camiones[llave_camion]['Tiempo en movimiento'] = 0
                    camiones_en_bodega.append(llave_camion)
                    camiones[llave_camion]['Plata en camion'] = 0
                    historial_por_turno.append(f'''[{hora(tiempo_actual)[0]}] - {llave_camion} llega a la Bodega. \n''')

                # Entra a recargar
                else:
                    camiones[llave_camion]['Historial'].append((camiones[llave_camion]['Objetivo'], tiempo_actual))
                    camiones[llave_camion]['Tiempo en llegar a objetivo'] = round(cajeros[camiones[llave_camion]['Objetivo']]['Duracion de la recarga']*3600, 0)
                    camiones_recargando.append(llave_camion)
                    cajeros[camiones[llave_camion]['Objetivo']]['Estado'] = 'Recarga'
                    llegada = (tiempo_actual + camiones[llave_camion]['Tiempo en llegar a objetivo'])
                    
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
                historial_por_turno.append(f'''[{hora(tiempo_actual)[0]}] - {llave_camion} termina de recargar al {camiones[llave_camion]['Objetivo']}. \n''')
                historial_por_turno.append(f'''[{hora(tiempo_actual)[0]}] * {camiones[llave_camion]['Objetivo']} recargado. \n''')
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
                        historial_por_turno.append(f'''[{hora(tiempo_actual)[0]}] * {llave_cajero} entra en Stock Out. \n''')                        
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
    draw_by_turno(cajeros, camiones, semana, dia, turno)
    cajeros_a_visitar = []
    for llave_camion in camiones:
        camiones[llave_camion]['Tiempo en simulacion'] = 0
        camiones[llave_camion]['Cajero simulacion'] = 'Bodega'
        camiones[llave_camion]['Pre historial'] = []
    for llave_cajero in cajeros:
        if llave_cajero != 'Bodega':
            cajeros[llave_cajero]['Camion simulacion'] = "ninguno"
            

    # Se traspasa el historial del turno al general
    historial_por_turno.append('\n')
    historial_general.append(historial_por_turno)
    for llave_camion in camiones:
        # print(f'{llave_camion}: {camiones[llave_camion]["Historial"]}')
        camiones[llave_camion]['Historial'] = []


# Se obtienen los resultados
resultados = ['\n', '\n', '\n', 'RESULTADOS: \n']
suma_fijo = 0
suma_variable = 0
suma_traslado = 0
for llave_cajero in cajeros:
    if llave_cajero != 'Bodega':
        suma_fijo += cajeros[llave_cajero]['Costo fijo acumulado stock out']
        suma_variable += cajeros[llave_cajero]["Costo variable acumulado stock out"]
for llave_camion in camiones:
    suma_traslado += camiones[llave_camion]['Costo traslado acumulado']
resultados.append(f'> Total costo variable Stock Out: MM${suma_variable}.\n')
resultados.append(f'> Total costo fijo Stock Out: MM${suma_fijo}.\n')
resultados.append(f'> Total en traslado: MM${suma_traslado}.\n')
resultados.append(f'TOTAL> MM${suma_variable + suma_fijo + suma_traslado}.')

# Se traspasan los resultados al historial
historial_general.append(resultados)

# Se escribe el archivo con los resultados
with open(f'Resultados FIXED {numero_de_días} dias [MM$ {int(plata_inicial)}].txt', 'w') as archivo:
    for sublista in historial_general:
        for linea in sublista:
            archivo.write(linea)
