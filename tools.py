from bokeh.layouts import row
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool
import csv, random


# Se carga el nombre y la ubicacion de los cajeros
cajeros = dict()
with open('ubicaciones.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cajeros[row['Cajero']] = {'Pos_x':row['X'], 'Pos_y':row['Y']}

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
for numero in cajeros.keys():
    dot.circle(int(cajeros[numero]['Pos_x']), int(cajeros[numero]['Pos_y']), size=3, fill_color="red", line_color="black", line_width=0.5, name=numero)


# Posible ruta
a = [random.randint(0, 120) for i in range(121)]
b = [random.randint(0, 120) for i in range(121)]
c = [random.randint(0, 120) for i in range(121)]
d = [random.randint(0, 120) for i in range(121)]
e = [random.randint(0, 120) for i in range(121)]
f = [random.randint(0, 120) for i in range(121)]
colors = [
    "#0B486B", "#79BD9A", "#CFF09E",
    "#79BD9A", "#0B486B", "#79BD9A",
    "#CFF09E", "#79BD9A", "#0B486B"
]
lista = [a, b, c, d, e, f]
for i in range(9):
    h = random.choice(lista)
    l = random.choice(lista)
    dot.step(h, l, line_width=2, color=colors[i], legend=str(i))
dot.legend.location = "top_left"
dot.legend.click_policy="hide"
# dot.add_tools(HoverTool(detalles_mostrados))
output_file("ubicaciones.html", title="Ubicaciones ATM's")
show(dot, sizing_mode="scale_width")  # open a browser
print("Terminado bro")

# Idea: graficar las listas para cada camion como si fueran horas de la semana, teniendo finalmente cada camión una lista con [7*24 elementos]
# En caso de que se quede paradado/bodega, se mantiene la posicion

# Para calcular la distacia, calcularlo como la [(x1-x2) + (y1 - y2)]*100 mts.