from tools import *
from parameters import *
from time import sleep

print('Cargando la infomacion de los camiones')
camiones = carga_camiones()
print('Listo')
print('Cargando la infomacion de los cajeros')
cajeros = carga_cajeros()
print('Listo')
print('Cargando la infomacion de los cassetes')
cassetes = carga_cassetes()
print('Listo')
print("""
==================  CASO BASE  ==================
""")
dias_semana = ['1', '2', '3', '4', '5', '6', '7']
horarios = ['1', '2', '3']
dias_totales = float(input('Ingrese el numero de dias que desea calcular: '))
dia_semana = input(f''' Seleccione el dia que quiere:
1) Lunes
2) Martes
3) Miercoles
4) Jueves
5) Viernes
6) Sabado
7) Domingo
>> ''')
while dia_semana not in dias_semana:
    print("No existe esa opcion.")
    dia_semana = input(f'''Seleccione el dia que quiere:
1) Lunes
2) Martes
3) Miercoles
4) Jueves
5) Viernes
6) Sabado
7) Domingo
>> ''')
dia_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'][int(dia_semana) - 1]
horario = input(f'''Seleccione el horario con que quiere partir el turno:
1) Manana
2) Tarde
3) Noche
>> ''')
while horario not in horarios:
    print("No existe esa opcion.")
    horario = input(f'''Seleccione el horario:
1) Manana
2) Tarde
3) Noche
>> ''')
horario = ['Manana', 'Tarde', 'Noche'][int(horario) - 1]
plata_a_recargar = float(input('Ingrese la plata con que parten todos los cajeros: '))
for llave in cajeros:
    if llave != 'Bodega':
        cajeros[llave]['Plata actual'] += plata_a_recargar
print("-------------------------------------------------------------------------------------")
print(f'Elegiste {dias_totales} de simulación, partiendo el {dia_semana} en {horario} con MM {plata_a_recargar}')
print("")

# Se va a modelar en segundos, siendo cada vuelta un segundo
tiempo = 0
turno = 8 * 3600
inicio_turno = 0
fin_turno = False
cajeros_a_stock_out = []
cajeros_con_plata = [llave for llave in cajeros.keys() if llave != 'Bodega']
# print(cajeros_con_plata)
cajeros_en_stock_out = []
cajeros_en_stock_out_disponibles = []
print("Empieza el ciclo")
rellenados = 0

while turno:
    print(f"Tiempo: {tiempo} segs")
    if inicio_turno == tiempo:
        print('Inicio de turno')
        fin_turno = 60 * 60 * 8  # 8 horas en segundo
        cajeros_disponibles = disponibilidad(cajeros, dia_semana, horario)
        for llave in cajeros_en_stock_out:
            if llave in cajeros_disponibles:
                cajeros_en_stock_out_disponibles.append(llave)
                cajeros_en_stock_out.remove(camiones[llave]['Objetivo'])
        for llave in cajeros_con_plata:
            if llave in cajeros_disponibles:
                if (cajeros[llave]['Promedio diario de retiro'] / 3 > cajeros[llave]['Plata actual']):
                    print(
                        f'''El {llave} va a quedarse en stock out (prom retiro: {cajeros[llave]['Promedio diario de retiro'] / 3} vs Plata actual: {cajeros[llave]['Plata actual']} )''')
                    cajeros_a_stock_out.append(llave)
                else:
                    pass
        sleep(10)
        # print(f'''El {llave} no va a tener stock out ({cajeros[llave]['Promedio diario de retiro']/3} vs {cajeros[llave]['Plata actual']} )''')
        # cajeros_con_plata.append(llave)
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")
        # print("---------------------------------------------------------------------------------------------------------------------------------------------------")

    # print("  >> Se recorren los camiones - mandar a casa")
    for llave in camiones.keys():
        if camiones[llave]['Estado'] == 'parado' and camiones[llave]['Objetivo'] != 'Bodega':
            if ((camiones[llave]['Tiempo maximo'] >= (
                    camiones[llave]['Tiempo en movimiento'] + distancia(cajeros[camiones[llave]['Objetivo']], cajeros[
                'Bodega']) * 3.6 / velocidad_camion))) or (camiones[llave]['Plata en camion'] == 0):
                camiones[llave]['Tiempo en llegar a objetivo'] = distancia(cajeros[camiones[llave]['Objetivo']],
                                                                           cajeros['Bodega']) * 3.6 / velocidad_camion
                print(
                    f'''El {llave} va a Bodega a recargar, se demora {camiones[llave]['Tiempo en llegar a objetivo']}''')
                camiones[llave]['Objetivo'] = 'Bodega'
                camiones[llave]['Estado'] = 'viajando'
                sleep(5)
    # print("  >> Se recorren los cajeros con plata")
    for llave in cajeros_con_plata:
        cajeros[llave]['Plata actual'] -= cajeros[llave]['Promedio diario de retiro'] / (24 * 3600)
        if cajeros[llave]['Plata actual'] <= 0.0:
            cajeros[llave]['Plata actual'] = 0  # para que no queden con plata negativa
            cajeros_con_plata.remove(llave)
            cajeros_en_stock_out.append(llave)
            cajeros[llave]['Estado'] = "Stock out"
            cajeros[llave]["Costo fijo acumulado stock out"] += cajeros[llave]['Costo fijo por Stock Out']
    # print("  >> Se recorren los cajeros con stock out disponibles")    
    for llave in cajeros_en_stock_out_disponibles:
        for id_camion in camiones:
            if camiones[id_camion]['Estado'] == 'parado' and cajeros[llave]['Estado'] == 'normal':
                if camiones[id_camion]['Tiempo maximo'] >= (
                        camiones[id_camion]['Tiempo en movimiento'] + distancia(cajeros[llave], cajeros[
                    'Bodega']) * 3.6 / velocidad_camion + cajeros[llave]['Duracion de la recarga'] * 3600 +
                        distancia(cajeros[llave], cajeros['Bodega']) * 3.6 / velocidad_camion):
                    # Se recarga el camion con el maximo de su capacidad con cassetes de 35 (chicos)
                    camiones[id_camion]['Objetivo'] = llave
                    camiones[id_camion]['Estado'] = 'viajando'
                    camiones[id_camion]['Plata en camion'] = camiones[id_camion]['Carga maxima plata']
                    camiones[id_camion]['Tiempo en llegar a objetivo'] = distancia(cajeros[llave], cajeros[
                        'Bodega']) * 3.6 / velocidad_camion
                    cajeros[llave]['Estado'] = 'en camino'
                    print(
                        f'''El {id_camion} va al {llave} que esta en stock out, se demora {camiones[id_camion]['Tiempo en llegar a objetivo']}''')
                    sleep(2)

                break
    # print("  >> Se recorren los cajeros a stock out")
    for llave in cajeros_a_stock_out:
        cajeros[llave]['Plata actual'] -= cajeros[llave]['Promedio diario de retiro'] / (24 * 3600)
        if cajeros[llave]['Plata actual'] <= 0:
            # Entra en stock out
            pass
        for id_camion in camiones:
            if camiones[id_camion]['Estado'] == 'parado' and cajeros[llave]['Estado'] == 'normal':
                # Se recarga el camion con el maximo de su capacidad con cassetes de 35 (chicos)
                camiones[id_camion]['Objetivo'] = llave
                camiones[id_camion]['Estado'] = 'viajando'
                camiones[id_camion]['Plata en camion'] = camiones[id_camion]['Carga maxima plata']
                camiones[id_camion]['Tiempo en llegar a objetivo'] = distancia(cajeros[llave], cajeros[
                    'Bodega']) * 3.6 / velocidad_camion
                cajeros[llave]['Estado'] = 'en camino'
                print(
                    f'''El {id_camion} va al {llave} que va a quedar stock out, se demora {camiones[id_camion]['Tiempo en llegar a objetivo']}''')
                sleep(2)
                break
    # print("  >> Se recorren los camiones - tiempo")    
    for llave in camiones.keys():
        if camiones[llave]['Estado'] == 'viajando':
            camiones[llave]['Costo traslado acumulado'] += (55 / 3600) * costo_traslado  # kilometros en un segundo por costo por km de traslado
            if camiones[llave]['Tiempo en llegar a objetivo'] <= 0:
                # sleep(10)
                if camiones[llave]['Objetivo'] != 'Bodega':
                    print(f'''El {llave} ha llegado al {camiones[llave]['Objetivo']}, empieza a recargar''')
                    sleep(2)

                    camiones[llave]['Estado'] = 'recargando'
                    camiones[llave]['Tiempo en llegar a objetivo'] = cajeros[camiones[llave]['Objetivo']][
                                                                         'Duracion de la recarga'] * 3600
                else:
                    camiones[llave]['Estado'] = 'parado'
                    camiones[llave]['Tiempo en movimiento'] = 0
        elif camiones[llave]['Estado'] == 'recargando':
            if camiones[llave]['Tiempo en llegar a objetivo'] <= 0:
                # sleep(10)
                rellenados += 1
                cajeros[camiones[llave]['Objetivo']]['Estado'] = 'normal'
                cajeros[camiones[llave]['Objetivo']]['Plata actual'] = 35  # Aca vamos a tener que poner el cassete
                cajeros_con_plata.append(camiones[llave]['Objetivo'])
                if camiones[llave]['Objetivo'] in cajeros_en_stock_out:
                    cajeros_en_stock_out.remove(camiones[llave]['Objetivo'])
                else:
                    cajeros_a_stock_out.remove(camiones[llave]['Objetivo'])
                camiones[llave]['Plata en camion'] -= 35
                camiones[llave]['Estado'] = 'parado'
                print(f'''El {llave} ha de recargar al {camiones[llave]['Objetivo']}''')

                sleep(2)

        if camiones[llave]['Objetivo'] == 'Bodega':
            if camiones[llave]['Estado'] == 'viajando':
                camiones[llave]['Tiempo en llegar a objetivo'] -= 1
                camiones[llave]['Tiempo en movimiento'] += 1
        elif camiones[llave]['Objetivo'] != 'Bodega':
            if camiones[llave]['Estado'] == 'viajando':
                camiones[llave]['Tiempo en llegar a objetivo'] -= 1
                camiones[llave]['Tiempo en movimiento'] += 1
            elif camiones[llave]['Estado'] == 'recargando':
                camiones[llave]['Tiempo en movimiento'] += 1
                camiones[llave]['Tiempo en llegar a objetivo'] -= 1
    for llave in cajeros_en_stock_out:
        cajeros[llave]["Costo variable acumulado stock out"] += cajeros[llave]['Costo variable por Stock Out']
        cajeros[llave]['Plata actual'] = 0
    tiempo += 1
    if tiempo == fin_turno:
        turno = False
print(rellenados)
for llave in cajeros.keys():
    if llave != 'Bodega':
        print(f'''{llave}:
Plata actual: {cajeros[llave]['Plata actual']}
Costo variable acumulado: {cajeros[llave]["Costo variable acumulado stock out"]}
Costo fijo acumulado: {cajeros[llave]["Costo fijo acumulado stock out"]}
Estado: {cajeros[llave]["Estado"]}
''')
for llave in camiones:
    print(f"Costo total en traslado: {llave}: {camiones[llave]['Costo traslado acumulado']}")

#print("Suma total costo variable Stock Out:", sum([(cajeros[llave]["Costo variable acumulado stock out"]) for llave in cajeros]))
#print("Suma total costo fijo Stock Out:", sum([(cajeros[llave]["Costo fijo acumulado stock out"]) for llave in cajeros]))
#print("Suma total costo traslado:", sum([(camiones[llave]['Costo traslado acumulado']) for llave in camiones]))
