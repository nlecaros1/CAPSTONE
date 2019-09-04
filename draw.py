import networkx as nx
from gurobipy import *
import matplotlib.pyplot as plt
import numpy as np
import random

def distancia(pos1, pos2):
    """
    distancia -- calcula distancia entre dos posiciones (de nodos) 
    Parámetros: 
        - pos1, pos2: tupla de posiciones (x,y)
    Retorna distancia entre dos puntos
    """
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def graficar(nodos, arcos):
    """
    graficar -- grafica los nodos y arcos entregados
    Parámetros: 
        - nodos: diccionario con los id de los nodos de la forma {id nodo: (pos_x, pos_y)}
        - arcos: diccionario con los arcos de la forma {(cola,cabeza): costo}
    Retorna en pantalla un gráfico de lo solicitado.
    """
    G = nx.Graph() #esto genera un grafo no dirigido
    posiciones = dict()
    
    for nodo in nodos:
        G.add_node(nodo, pos=nodos[nodo])
        posiciones[nodo] = nodos[nodo]
        
# esto se hace exclusivamente si hay por ejemplo 2 opciones de forma de input de alguna variable.
# En este caso puede ser lista o dict.
    if isinstance(arcos, dict):
        for arco in arcos:
            G.add_edge(arco[0], arco[1], weight=arcos[arco])
    elif isinstance(arcos, list): 
        for arco in arcos:
            G.add_edge(arco[0], arco[1])
            
    nx.draw(G, pos=posiciones, with_labels=True, node_shape="o", font_size=14)
    plt.show()

def datos():
    """
    datos -- genera datos para el problema
    Retorna diccionario para nodos y para arcos
    """
    nodos = dict()
    arcos = dict()
    n = 10 #número de nodos
    
    for nodo in range(n):
        nodos[nodo] = (random.randint(0,30), random.randint(0,30)) #posición x,y del nodo
    for nodo in nodos: #recorre todos los id de los nodos ya creados
        for nodo2 in nodos:
            if nodo2 > nodo: #grafo completo no dirigido
                arcos[(nodo, nodo2)] = distancia(nodos[nodo], nodos[nodo2]) #{id arco: costo}
    
    return nodos, arcos

nodos, arcos = datos()
graficar(nodos, arcos)

