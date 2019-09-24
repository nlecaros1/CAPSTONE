from bokeh.layouts import row
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool
import csv, random

def carga():
    cajeros = dict()
    with open('ubicaciones.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cajeros[row['Cajero']] = {'Pos_x':row['X'], 'Pos_y':row['Y'], 'Promedio diario de retiro': row['Promedio diario de retiro'], 'Costo fijo por Stock Out': row['Costo fijo por Stock Out'], 'Costo variable por Stock Out': row['Costo variable por Stock Out'], 
            'Duracion de la recarga': row['Duracion de la recarga'], 'Lunes': row['Lunes'], 'Martes': row['Martes'], 'Miercoles': row['Miercoles'], 'Jueves': row['Jueves'], 'Viernes': row['Viernes'], 'Sabado': row['Sabado'],
            'Domingo': row['Domingo'], 'Manana': row['Manana'], 'Tarde': row['Tarde'], 'Noche': row['Noche'], 'Plata actual': 0, 'Dias sin plata': 0}
    cajeros['Bodega'] =  {'Pos_x':70, 'Pos_y': 70}
    return cajeros

def draw(cajeros):
    detalles_mostrados = [("nombre", "$name")]
    # Se crea los elementos del grafico
    dot = figure(title="Ubicaciones de cajeros", tooltips=detalles_mostrados, toolbar_location='above',
                y_range=[0,120], x_range=[0,120], x_axis_label='X', y_axis_label='Y')

    # Se crea el mapa
    factors = [str(i) for i in range(120)]
    lineas =  [120 for i in range(120)]
    dot.segment(0, factors, lineas, factors, line_width=0.5, line_color="gray" )
    dot.segment(factors, 0, factors, lineas, line_width=0.5, line_color="gray")

    # Carga la ubicacion de los cajeros en el mapa
    for llave in cajeros.keys():
        if llave != 'Bodega':
            dot.circle(int(cajeros[llave]['Pos_x']), int(cajeros[llave]['Pos_y']), size=3, fill_color="red", line_color="black", line_width=0.5, name=llave, legend="Cajeros")

    # Carga la bodega en el mapa
    dot.circle(70, 70, size=5, fill_color="green", line_color="black", line_width=0.5, name='Bodega', legend="Bodega")

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

def distancia(punto_1, punto_2):
    return abs(int(punto_1['Pos_x']) - int(punto_2['Pos_x'])) + abs(int(punto_1['Pos_y']) - int(punto_2['Pos_y']))

def hora(minutos_entrantes):
    hora = minutos_entrantes//60
    minutos = minutos_entrantes
    return f'{hora}:{minutos}'
    

def disponibilidad(cajeros, numero, dia, horario):
    for llave in cajeros:
        if llave != 'Bodega':
            if cajeros[llave][dia] == '1' and cajeros[llave][horario] == '1':
                print(llave)

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
                con_plata.remove(llave)
                sin_platas.append(llave)
                cajeros[llave]['Dias sin plata'] = -1
        for llave in sin_platas:
            cajeros[llave]['Dias sin plata'] += 1
        print("")
        print(f'-------------- Dia {dia} --------------')
        print('> Cajeros con plata:')
        for llave in con_plata:
            print(f'''     - {llave}: MM$ {cajeros[llave]['Plata actual']}''')
        print('> Cajeros sin plata:')
        for llave in sin_platas:
            print(f'     - {llave}: {cajeros[llave]["Dias sin plata"]} dias sin plata')
        dia += 1

                

# Idea: graficar las listas para cada camion como si fueran horas de la semana, teniendo finalmente cada camión una lista con [7*24 elementos]
# En caso de que se quede paradado/bodega, se mantiene la posicion


# Para calcular la distacia, calcularlo como la [(x1-x2) + (y1 - y2)]*100 mts.
