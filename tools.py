from bokeh.layouts import row
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool
import csv, random


def carga_cajeros():
    cajeros = dict()
    with open('ubicaciones.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cajeros[row['Cajero']] = {'Pos_x': row['X'], 'Pos_y': row['Y'],
                                      'Promedio diario de retiro': float(row['Promedio diario de retiro']),
                                      'Costo fijo por Stock Out': float(row['Costo fijo por Stock Out']),
                                      'Costo variable por Stock Out': float(row['Costo variable por Stock Out']),
                                      'Duracion de la recarga': float(row['Duracion de la recarga']),
                                      'Lunes': row['Lunes'], 'Martes': row['Martes'], 'Miercoles': row['Miercoles'],
                                      'Jueves': row['Jueves'], 'Viernes': row['Viernes'], 'Sabado': row['Sabado'],
                                      'Domingo': row['Domingo'], 'Manana': row['Manana'], 'Tarde': row['Tarde'],
                                      'Noche': row['Noche'], 'Plata actual': 0, 'Dias sin plata': 0,
                                      "Costo fijo acumulado stock out": 0, "Costo variable acumulado stock out": 0,
                                      'Estado': 'Normal'}
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
                                                       'Costo traslado acumulado': 0}  # En segundo el tiempo
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
    # dot.legend.location = "right"
    # dot.legend.click_policy="hide"

    output_file("ubicaciones.html", title="Ubicaciones ATM's")
    show(dot, sizing_mode="scale_width")  # open a browser
    return


def draw_by_disponibility(cajeros, disponibles, nombre):
    detalles_mostrados = [("nombre", "$name")]
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


def distancia(punto_1, punto_2):
    return abs(int(punto_1['Pos_x']) - int(punto_2['Pos_x']))*100 + abs(int(punto_1['Pos_y']) - int(punto_2['Pos_y']))*100 #entrega distancia en mts


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
