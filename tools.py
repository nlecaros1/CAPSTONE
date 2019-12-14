from bokeh.layouts import row
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool
import bokeh.palettes  as bp
import csv, random
from parameters import cajeros_hora
from bokeh.palettes import Spectral4


def carga_cajeros():
    cajeros = dict()
    with open('ubicaciones.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cajeros[row['Cajero']] = {'Llave': row['Cajero'], 'Pos_x': int(row['X']), 'Pos_y': int(row['Y']),
                                      'Promedio diario de retiro': float(row['Promedio diario de retiro']),
                                      'Costo fijo por Stock Out': float(row['Costo fijo por Stock Out']),
                                      'Costo variable por Stock Out': float(row['Costo variable por Stock Out']),
                                      'Duracion de la recarga': float(row['Duracion de la recarga']),
                                      'Lunes': row['Lunes'], 'Martes': row['Martes'], 'Miercoles': row['Miercoles'],
                                      'Jueves': row['Jueves'], 'Viernes': row['Viernes'], 'Sabado': row['Sabado'],
                                      'Domingo': row['Domingo'], 'Manana': row['Manana'], 'Tarde': row['Tarde'],
                                      'Noche': row['Noche'], 'Plata actual': 0, 'Dias sin plata': 0,
                                      "Costo fijo acumulado stock out": 0, "Costo variable acumulado stock out": 0,
                                      'Estado': 'Normal',
                                      'Orden': 0, 'Motivo a ordenar': 'Normal', 'Tiempo en simulacion': 0, 'Camion simulacion': "ninguno", 'Opcion': 0 , 'Tiempo_a_agregar': 0}
    cajeros['Bodega'] = {'Pos_x': 70, 'Pos_y': 70}
    return cajeros


def carga_camiones():
    camiones = dict()
    contador = 0
    with open('camiones.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for number in range(int(row['Cantidad de camiones'])):
                camiones['Camion ' + str(contador)] = {'Tipo': row['Tipo de Camion'][:-1].lower(),
                                                       'Tiempo maximo': float(row['Tiempo maximo en Ruta']) * 3600,
                                                       'Carga maxima plata': float(row['Carga en dinero']),
                                                       'Tiempo en movimiento': 0, 'Plata en camion': 0,
                                                       'Objetivo': 'Bodega', 'Tiempo en llegar a objetivo': -1,
                                                       'Estado': 'parado',
                                                       'Costo traslado acumulado': 0, 'Cajero simulacion': "Bodega", 'Tiempo en simulacion': 0,
                                                       'Historial': [], "Tiempo simulacion": 0, 'Pre historial': []}  # En segundo el tiempo
                contador += 1
    return camiones


def carga_cassetes():
    cassetes = dict()
    with open('cassetes.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cassetes[row['Tamano']] = {'Cantidad de plata': row['Cantidad de dinero']}
    return cassetes


def draw(cajeros):
    detalles_mostrados = [("nombre", "$name")]
    # Se crea los elementos del grafico
    dot = figure(title="Ubicaciones de cajeros", tooltips=detalles_mostrados, toolbar_location='above',
                 y_range=[0, 120], x_range=[0, 120], x_axis_label='X', y_axis_label='Y')

    # Se crea el mapa
    factors = [str(i) for i in range(120)]
    lineas = [120 for i in range(120)]
    dot.segment(0, factors, lineas, factors, line_width=0.5, line_color="gray")
    dot.segment(factors, 0, factors, lineas, line_width=0.5, line_color="gray")

    # Carga la ubicacion de los cajeros en el mapa
    # lista = disponibilidad(cajeros,"Lunes", "Manana")
    for llave in cajeros:
        if llave != 'Bodega':
            if cajeros[llave]['Promedio diario de retiro'] >= 21:
                tamano = 7
            elif cajeros[llave]['Promedio diario de retiro'] <= 11:
                tamano = 3
            else:
                tamano = 5
            if distancia(cajeros[llave], cajeros['Bodega'])/100 >= 90:
                color = 'red'
            elif distancia(cajeros[llave], cajeros['Bodega'])/100 <= 35:
                color = 'green'
            else:
                color = 'yellow'
            dot.circle(int(cajeros[llave]['Pos_x']), int(cajeros[llave]['Pos_y']), size=tamano, fill_color=color,
                       line_color="black", line_width=0.5, name=llave, legend="Cajeros")

    # Carga la bodega en el mapa
    dot.circle(70, 70, size=5, fill_color="black", line_color="black", line_width=0.5, name='Bodega', legend="Bodega")

    # Posible ruta
    # a = [random.randint(0, 120) for i in range(121)]
    # b = [random.randint(0, 120) for i in range(121)]
    # c = [random.randint(0, 120) for i in range(121)]
    # d = [random.randint(0, 120) for i in range(121)]
    # e = [random.randint(0, 120) for i in range(121)]
    # f = [random.randint(0, 120) for i in range(121)]
    # colors = [
    #     "#0B486B", "#79BD9A", "#CFF09E",
    #     "#79BD9A", "#0B486B", "#79BD9A",
    #     "#CFF09E", "#79BD9A", "#0B486B"
    # ]
    # lista = [a, b, c, d, e, f]
    # for i in range(9):
    #     h = random.choice(lista)
    #     l = random.choice(lista)
    #     dot.step(h, l, line_width=2, color=colors[i], legend=str(i))

    output_file("ubicaciones.html", title="Ubicaciones ATM's")
    show(dot, sizing_mode="scale_width")  # open a browser
    return


def draw_by_disponibility(cajeros, disponibles, nombre):
    # detalles_mostrados = [("nombre", "$name")]
    # Se crea los elementos del grafico
    dot = figure(title="Ubicaciones de cajeros", tooltips=detalles_mostrados, toolbar_location='above',
                 y_range=[0, 120], x_range=[0, 120], x_axis_label='X', y_axis_label='Y')
    factors = [str(i) for i in range(120)]
    lineas = [120 for i in range(120)]
    dot.segment(0, factors, lineas, factors, line_width=0.5, line_color="gray")
    dot.segment(factors, 0, factors, lineas, line_width=0.5, line_color="gray")
    for llave in disponibles:
        if cajeros[llave]['Promedio diario de retiro'] >= 21:
            tamano = 7
        elif cajeros[llave]['Promedio diario de retiro'] <= 11:
            tamano = 3
        else:
            tamano = 5
        if distancia(cajeros[llave], cajeros['Bodega'])/100 >= 90:
            color = 'red'
        elif distancia(cajeros[llave], cajeros['Bodega'])/100 <= 35:
            color = 'green'
        else:
            color = 'yellow'
        dot.circle(int(cajeros[llave]['Pos_x']), int(cajeros[llave]['Pos_y']), size=tamano, fill_color=color,
                    line_color="black", line_width=0.5, name=llave, legend="Cajeros")

    dot.circle(70, 70, size=5, fill_color="black", line_color="black", line_width=0.5, name='Bodega', legend="Bodega")
    output_file(f'Mapas/{nombre}.html', title="Ubicaciones ATM's")
    show(dot, sizing_mode="scale_width")  # open a browser
    return

def draw_by_turn_initial(cajeros, cajeros_a_visitar, semana, dia, horario):
    detalles_mostrados = [("nombre", "$name")]
    # Se crea los elementos del grafico
    dot = figure(title="Ubicaciones de cajeros", tooltips=detalles_mostrados, toolbar_location='above',
                 y_range=[0, 120], x_range=[0, 120], x_axis_label='X', y_axis_label='Y')
    factors = [str(i) for i in range(120)]
    lineas = [120 for i in range(120)]
    dot.segment(0, factors, lineas, factors, line_width=0.5, line_color="gray")
    dot.segment(factors, 0, factors, lineas, line_width=0.5, line_color="gray")
    maximo = cajeros[cajeros_a_visitar[0]]['Orden']
    tamano_periodo = maximo/11
    lista_colores = sorted(bp.all_palettes['RdYlGn'][11], reverse=True)
    # print(lista_colores)
    for llave in cajeros_a_visitar:
        tamano = 5
        for numero in range(11):
            if numero*tamano_periodo <= cajeros[llave]['Orden'] and  (numero + 1)*tamano_periodo >= cajeros[llave]['Orden']:
                color = lista_colores[numero]
        dot.circle(int(cajeros[llave]['Pos_x']), int(cajeros[llave]['Pos_y']), size=tamano, fill_color=color,
                    line_color="black", line_width=0.5, name=llave, legend="Cajeros")

    dot.circle(70, 70, size=5, fill_color="black", line_color="black", line_width=0.5, name='Bodega', legend="Bodega")
    output_file(f'Mapas/Inicio Semana {semana} {dia} - {horario}.html', title="Ubicaciones ATM's")
    show(dot, sizing_mode="scale_width")  # open a browser
    return

def draw_by_turno(cajeros, camiones, semana, dia, horario):
    detalles_mostrados = [("nombre", "$name")]
    # Se crea los elementos del grafico
    dot = figure(title="Ubicaciones de cajeros", tooltips=detalles_mostrados, toolbar_location='above',
                 y_range=[0, 120], x_range=[0, 120], x_axis_label='X', y_axis_label='Y')
    factors = [str(i) for i in range(120)]
    lineas = [120 for i in range(120)]
    dot.segment(0, factors, lineas, factors, line_width=0.5, line_color="gray")
    dot.segment(factors, 0, factors, lineas, line_width=0.5, line_color="gray")
    lista_colores = sorted(bp.all_palettes['Category20'][12], reverse=True)
    contador = 0
    for llave_camiones in camiones:
        color = lista_colores[contador]
        contador_interno = 0
        previo = 'Bodega'
        for elemento in camiones[llave_camiones]['Historial']:
            if elemento[0] != 'Bodega':
                llave = elemento[0]
                # max_x = max((cajeros[previo]['Pos_x'], cajeros[llave]['Pos_x']))
                # min_x = min((cajeros[previo]['Pos_x'], cajeros[llave]['Pos_x']))
                # max_y = max((cajeros[previo]['Pos_y'], cajeros[llave]['Pos_y']))
                # min_y = min((cajeros[previo]['Pos_y'], cajeros[llave]['Pos_y']))
                # x = []
                # y = []
                # for numero in range(min_x, max_x):
                #     x.append(numero + 1)
                # for numero in range(min_y, max_y):
                #     y.append(numero + 1)
                # # print(len(x), "/", len(y))
                # if len(y) > 0 and len(x) > 0:
                #     if len(y) > len(x):
                #         diferencia = len(y) - len(x)
                #         for i in range(diferencia):
                #             x.append(x[-1])
                #     elif len(y) < len(x):
                #         diferencia = len(x) - len(y)
                #         for i in range(diferencia):
                #             y.append(y[-1])
                # elif len(x) == 0 and len(y) > 0:
                #     for i in range(len(y)):
                #         x.append(cajeros[llave]['Pos_x'])
                # elif len(y) == 0 and len(x) > 0:
                #     for i in range(len(x)):
                #         y.append(cajeros[llave]['Pos_y'])
                x, y = listas_posiciones(cajeros[previo], cajeros[llave])
                tamano = contador_interno
                dot.circle(int(cajeros[llave]['Pos_x']), int(cajeros[llave]['Pos_y']), size=tamano, fill_color=color,
                    line_color="black", line_width=0.5, name=llave, legend=llave_camiones, alpha=0.8, muted_color='#E8E8E8')
                # dot.step(y, x, line_width=2, color=color, legend=llave_camiones)

                contador_interno += 2
            previo = elemento[0]
        contador += 1

    dot.circle(70, 70, size=5, fill_color="black", line_color="black", line_width=0.5, name='Bodega', legend="Bodega")
    # dot.legend.location = "right"
    dot.legend.click_policy="mute"
    output_file(f'Mapas/Final Semana {semana} {dia} - {horario}.html', title="Ubicaciones ATM's")
    show(dot, sizing_mode="scale_width")  # open a browser
    return


def distancia(punto_1, punto_2):
    return abs(int(punto_1['Pos_x']) - int(punto_2['Pos_x']))*100 + abs(int(punto_1['Pos_y']) - int(punto_2['Pos_y']))*100 #entrega distancia en mts

def listas_posiciones(punto_1, punto_2):
    x = []
    y = []
    mayor_x = max(punto_1['Pos_x'], punto_2['Pos_x'])
    menor_x = min(punto_1['Pos_x'], punto_2['Pos_x'])
    mayor_y = max(punto_1['Pos_y'], punto_2['Pos_y'])
    menor_y = min(punto_1['Pos_y'], punto_2['Pos_y'])  
    while mayor_x > menor_x:
        menor_x += 1
        x.append(menor_x)
    while mayor_y > menor_y:
        menor_y += 1
        y.append(menor_y)
    if len(x) == 0:
        if len(y) == 0:
            pass
        else:
            for i in range(len(y)):
                x.append(mayor_x)
    elif len(y) == 0:
        if len(x) == 0:
            pass
        else:
            for i in range(len(x)):
                y.append(mayor_y)
    else:
        if len(x) > len(y):
            diferencia = len(x) - len(y)
            for i in range(diferencia):
                y.append(mayor_y)    
        elif len(y) > len(x):
            diferencia = len(y) - len(x)
            for i in range(diferencia):
                x.append(mayor_x)
        
    # print(len(x), len(y))
    return x, y

def hora(segundos_entrantes):
    # Se calculan el numero de la semana
    semana = (segundos_entrantes + 28800)//(3600*24*7)

    # Se dejan solo los segundos de ese dia y se le agregan las 8 horas iniciales del lunes en la manana. Se transforman en todos a tener dos digitos
    segundos_del_dia = (segundos_entrantes + 28800)%(3600*24)
    hora = str(segundos_del_dia//3600)
    hora = str(0)*(2 - len(hora)) + hora
    minutos = str((segundos_del_dia%3600)//60)
    minutos = str(0)*(2 - len(minutos)) + minutos
    segundos = str(((segundos_del_dia%3600)%60))
    segundos = str(0)*(2 - len(segundos)) + segundos
    return [f'{hora}:{minutos}:{segundos}', semana]
    

def call_draw_disponibility(cajeros):
    semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    horarios =  ['Manana', 'Tarde', 'Noche']
    for dia in semana:
        for turno in horarios:
            draw_by_disponibility(cajeros, disponibilidad(cajeros,dia, turno), f'{dia} - {turno}')
    return

def disponibilidad(cajeros, dia, horario):
    cajeros_disponibles = []
    for llave in cajeros:
        if llave != 'Bodega':
            if cajeros[llave][dia] == '1' and cajeros[llave][horario] == '1':
                cajeros_disponibles.append(llave)
    return cajeros_disponibles


def nuevamente_disponible(cajero, fecha_actual):

    dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    horarios =  ['Manana', 'Tarde', 'Noche']
    opciones = []
    for dia in dias_semana:
        for horario in horarios:
            if cajero[dia] == "1" and cajero[horario] == "1":
                indice_dia = dias_semana.index(dia) + 1            # Lunes: 1, Martes: 2, ..., Domingo: 7
                indice_horario = (horarios.index(horario)) / 3     # Manana: 0, Tarde: 0.333, Noche: 0.666
                fecha_disponible = indice_dia + indice_horario
                opciones.append(fecha_disponible)
    copia = []
    for elemento in opciones:
        copia.append(7 + elemento)
    finales = opciones + copia
    contador = 0
    for elemeto in finales:
        if elemeto < fecha_actual:
            pass
        elif elemeto == fecha_actual:
            contador += 1
            break
        else:
            break
        contador += 1
    indice_final = contador
    # print(f'Entra el cajero {cajero["Llave"]} que se puede recargar en {finales[indice_final] - fecha_actual}, con costo variable {cajero["Costo variable por Stock Out"]} y promedio de retiro {cajero["Promedio diario de retiro"]}')
    return (finales[indice_final] - fecha_actual)


def ponderador(cajeros, cajeros_disponibles, dia, horario):
    dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
    horarios =  ['Manana', 'Tarde', 'Noche']
    indice_dia = dias_semana.index(dia) + 1            # Lunes: 1, Martes: 2, ..., Domingo: 7
    indice_horario = (horarios.index(horario)) / 3     # Manana: 0, Tarde: 0.333, Noche: 0.666
    lista_cajeros = []
    fecha_actual = indice_dia + indice_horario
    lista_ordenada_a_entregar = []
    for llave in cajeros_disponibles:
        if llave != 'Bodega':
        # if llave == 'Cajero 3':
            distancia_disponibilidad  = nuevamente_disponible(cajeros[llave], fecha_actual)*24*60 # distancia_disponibilidad en minutos
            costo_fijo = 0
            if cajeros[llave]['Estado'] == 'Normal':
                costo_fijo = cajeros[llave]['Costo fijo por Stock Out']
                cajeros[llave]

            if ((cajeros[llave]['Plata actual'] - cajeros[llave]['Promedio diario de retiro'])*distancia_disponibilidad + costo_fijo) >= 0:
                cajeros[llave]['Orden'] = 0
            else:
                cajeros[llave]['Orden'] = (cajeros[llave]['Promedio diario de retiro'] - cajeros[llave]['Plata actual'])*distancia_disponibilidad + costo_fijo
            lista_cajeros.append(cajeros[llave])
    lista_ordenada_cajeros = sorted(lista_cajeros, key = lambda x: x['Orden'], reverse=True) 
    for cajero in lista_ordenada_cajeros:
        lista_ordenada_a_entregar.append(cajero['Llave'])
    
    return lista_ordenada_a_entregar


def n_mas_cercanos(posicion, cajeros, visitados_turno, n):
     ordenados = sorted(cajeros, key = lambda x: distancia(posicion,x))
     ordenados.remove(posicion)
     ordenados = [cajero['Llave'] for cajero in ordenados if cajero['Llave'] not in visitados_turno]
     return [cajero for cajero in ordenados[:n]]

def importancia(cajeros, cajeros_disponibles, dia, horario):
    lista_normales = []
    lista_a_stock_out = []
    lista_en_stock_out = []
    for llave in cajeros_disponibles:
        if cajeros[llave]['Motivo a ordenar'] == 'Normal':
            lista_normales.append(llave)
        elif cajeros[llave]['Motivo a ordenar'] == 'Futuro stock out':
            lista_a_stock_out.append(llave)
        else:
            lista_en_stock_out.append(llave)
        # print(f"{llave}: {cajeros[llave]['Motivo a ordenar']}")
    
    lista_normales = ponderador(cajeros, lista_normales, dia, horario)
    lista_a_stock_out = ponderador(cajeros, lista_a_stock_out, dia, horario)
    lista_en_stock_out = ponderador(cajeros, lista_en_stock_out, dia, horario)
    contador_a_stock_out = 0
    contador_en_stock_out = 0
    for llave in lista_normales:
        if len(lista_a_stock_out) > 0:
            if cajeros[lista_a_stock_out[0]]['Orden'] < cajeros[llave]['Orden']:
                contador_a_stock_out += 1
        if len(lista_en_stock_out) > 0:
            if cajeros[lista_en_stock_out[0]]['Orden'] < cajeros[llave]['Orden']:
                contador_en_stock_out += 1
    if contador_a_stock_out + contador_en_stock_out <= cajeros_hora:
        lista_ordenada = []
        lista_ordenada_stock_out = ponderador(cajeros, lista_a_stock_out + lista_en_stock_out, dia, horario)
        if len(lista_normales) > 0:
            verificador = -1
            for indice in range(len(lista_ordenada_stock_out)):
                if cajeros[lista_ordenada_stock_out[indice]]['Orden'] >= cajeros[lista_normales[0]]['Orden']:
                    lista_ordenada.append(llave)
                    
                else:
                    verificador = indice
                    break
            if verificador != -1:
                lista_ordenada = lista_ordenada + ponderador(cajeros, lista_ordenada_stock_out[verificador:] + lista_normales, dia, horario) 
            else:
                lista_ordenada = lista_ordenada + lista_normales
            return lista_ordenada
        else:
            return lista_ordenada_stock_out

    else:
        return ponderador(cajeros, cajeros_disponibles, dia, horario)
    # if len(lista_normales) > 0 :
    #     print(f"Normal mayor {llave}: {cajeros[lista_normales[0]]['Orden']}. Largo: {len(lista_normales)}")
    # if len(lista_a_stock_out) > 0:
    #     print(f"A stock out mayor {llave}: {cajeros[lista_a_stock_out[0]]['Orden']}. Largo: {len(lista_a_stock_out)} y tiene {contador_a_stock_out} mayores en normal")
    # if len(lista_en_stock_out) > 0:
    #     print(f"En stock out mayor {llave}: {cajeros[lista_en_stock_out[0]]['Orden']}. Largo: {len(lista_en_stock_out)} y tiene {contador_en_stock_out} mayores en normal")




def calculador(cajeros, monto):
    dia = 1
    con_plata = []
    sin_platas = []
    for llave in cajeros:
        if llave != 'Bodega':
            cajeros[llave]['Plata actual'] += monto
            con_plata.append(llave)
            cajeros[llave]['Dias sin plata'] = 0
    print("")
    print('-------------- Dia 0 --------------')
    print('> Se recargan todos los cajeros')
    while len(con_plata) > 0:
        for llave in con_plata:
            cajeros[llave]['Plata actual'] -= float(cajeros[llave]['Promedio diario de retiro'])
            if cajeros[llave]['Plata actual'] <= 0:
                cajeros[llave]['Plata actual'] = 0
                cajeros[llave]["Costo fijo acumulado stock out"] += cajeros[llave]['Costo fijo por Stock Out']
                con_plata.remove(llave)
                sin_platas.append(llave)
                cajeros[llave]['Dias sin plata'] = -1
        for llave in sin_platas:
            cajeros[llave]['Dias sin plata'] += 1
            cajeros[llave]["Costo variable acumulado stock out"] += cajeros[llave][
                                                                        'Costo variable por Stock Out'] * 24 * 60
        print("")
        print(f'-------------- Dia {dia} --------------')
        print('> Cajeros con plata:')
        for llave in con_plata:
            print(f'''     - {llave}: MM$ {cajeros[llave]['Plata actual']}''')
        print('> Cajeros sin plata:')
        costos_variables_acumulados = 0
        costos_fijos_acumulados = 0
        for llave in sin_platas:
            print(
                f'     - {llave}: {cajeros[llave]["Dias sin plata"]} dias sin plata. Costos por Stock Out: fijos {cajeros[llave]["Costo fijo acumulado stock out"]}, variables acumulados {cajeros[llave]["Costo variable acumulado stock out"]} [Total: {cajeros[llave]["Costo fijo acumulado stock out"] + cajeros[llave]["Costo variable acumulado stock out"]}]')
            costos_fijos_acumulados += cajeros[llave]["Costo fijo acumulado stock out"]
            costos_variables_acumulados += cajeros[llave]["Costo variable acumulado stock out"]
        costos_totales = costos_fijos_acumulados + costos_variables_acumulados
        print(
            f'====== Costo Fijos Stock Out: {costos_fijos_acumulados} ==== Costos Variables Stock Out: {costos_variables_acumulados} ==== Total: {costos_totales} ======')
        dia += 1

# Idea: graficar las listas para cada camion como si fueran horas de la semana, teniendo finalmente cada camión una lista con [7*24 elementos]
# En caso de que se quede paradado/bodega, se mantiene la posicion


# Para calcular la distacia, calcularlo como la [(x1-x2) + (y1 - y2)]*100 mts.


    