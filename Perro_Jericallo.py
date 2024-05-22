import itertools
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.scrolledtext import ScrolledText

########################################
#                                      #
#   EMMANUEL MARTIN MARIN              #
#   FABIAN JOHESHUA ESCALANTE FERNANDEZ#
#   MARRIO ZAHIT FLORES GRANERO        #
#                                      #
#                                      #
########################################

def InicializacionDeRuta(numVertices):
    peso = [[0 for b in range(numVertices)] for x in range(numVertices)]
    return peso

def AgregarCamino(peso, origin, destino, distancia):
    peso[origin][destino] = distancia
    peso[destino][origin] = distancia
    return peso

def RutaEsValida(peso, ruta):
    for i in range(len(ruta) - 1):
        ubicacionActual = ruta[i]
        siguienteUbicacion = ruta[i + 1]
        if peso[ubicacionActual][siguienteUbicacion] == 0:
            return False
    return True

def DistanciaTotal(peso, ruta):
    distanciaTotal = 0
    for i in range(len(ruta) - 1):
        ubicacionActual = ruta[i]
        siguienteUbicacion = ruta[i + 1]
        distanciaTotal += peso[ubicacionActual][siguienteUbicacion]
    return distanciaTotal

def FuerzaBruta(peso, inicio, final):
    numVertices = len(peso)
    caminoCorto = []
    distancia = float("inf")

    posiblesParadas = [i for i in range(numVertices) if i != inicio and i != final]
    for paradas in range(len(posiblesParadas) + 1):
        for paradas in itertools.combinations(posiblesParadas, paradas):
            ruta = [inicio] + list(paradas) + [final]

            if RutaEsValida(peso, ruta):
                caminoRecorridoSuma = DistanciaTotal(peso, ruta)

                if caminoRecorridoSuma < distancia:
                    distancia = caminoRecorridoSuma
                    caminoCorto = ruta

    return caminoCorto, distancia

def DivideYVenceras(peso, inicio, final, memo, visitados):
    if (inicio, final) in memo:
        return memo[(inicio, final)]

    numVertices = len(peso)

    if inicio == final:
        return [inicio], 0

    if peso[inicio][final] != 0:
        return [inicio, final], peso[inicio][final]

    distanciaMinima = float('inf')
    caminoMinimo = []

    for k in range(numVertices):
        if k != inicio and k != final and peso[inicio][k] != 0 and k not in visitados:
            visitados.add(k)
            subCamino1, subDistancia1 = DivideYVenceras(peso, inicio, k, memo, visitados)
            subCamino2, subDistancia2 = DivideYVenceras(peso, k, final, memo, visitados)
            visitados.remove(k)

            if subCamino1 and subCamino2 and subCamino1[-1] == k and subCamino2[0] == k:
                subDistanciaTotal = subDistancia1 + subDistancia2
                if subDistanciaTotal < distanciaMinima:
                    distanciaMinima = subDistanciaTotal
                    caminoMinimo = subCamino1[:-1] + subCamino2

    memo[(inicio, final)] = (caminoMinimo, distanciaMinima if caminoMinimo else float('inf'))
    return memo[(inicio, final)]

# Función para graficar el grafo y los caminos encontrados
def GraficarGrafo(peso, camino, titulo):
    plt.ion()  # modo interactivo
    G = nx.Graph()
    for i in range(len(peso)):
        for j in range(i + 1, len(peso)):
            if peso[i][j] != 0:
                G.add_edge(i, j, weight=peso[i][j])

    pos = nx.spring_layout(G)  # posición de los nodos

    nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=12, font_weight="bold")  # dibujar el grafo

    # Agregar etiquetas de peso a los ejes
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # Dibujar el camino encontrado
    if camino:
        edges = [(camino[i], camino[i + 1]) for i in range(len(camino) - 1)]
        nx.draw_networkx_edges(G, pos, edgelist=edges, width=3, edge_color='r')

    plt.title(titulo)
    plt.axis('off')
    plt.axis('off')
    plt.draw()  # Dibujar sin bloquear
    plt.pause(0.001)  # Pausa muy corta para permitir que se renderice la gráfica
    plt.show(block=False)  # Mostrar sin bloquear


inicio = 0
final = 4
numVertices = 5

peso = InicializacionDeRuta(numVertices)
peso = AgregarCamino(peso, 0, 1, 10)
peso = AgregarCamino(peso, 0, 2, 15)
peso = AgregarCamino(peso, 1, 2, 5)
peso = AgregarCamino(peso, 1, 3, 2)
peso = AgregarCamino(peso, 2, 3, 8)
peso = AgregarCamino(peso, 3, 4, 6)

# Llamar a los algoritmos y obtener los caminos más cortos
caminoCortoDV, distanciaDV = DivideYVenceras(peso, inicio, final, {}, set())
caminoCortoFB, distanciaFB = FuerzaBruta(peso, inicio, final)

# Graficar los grafos y los caminos encontrados
def GrafoD():
    GraficarGrafo(peso, caminoCortoDV, f'Divide y Vencerás: {caminoCortoDV}, Distancia: {distanciaDV}')
    ResultadoD= f"{caminoCortoDV}"
    DistanciaD=f"{distanciaDV}"
    Texto2.config(state = 'normal')
    Texto2.delete(0, END)
    Texto2.insert(0, ResultadoD)
    Texto2.config(state = 'readonly')

    Texto2_1.config(state = 'normal')
    Texto2_1.delete(0, END)
    Texto2_1.insert(0, DistanciaD)
    Texto2_1.config(state = 'readonly')
    


def GrafoF():
    GraficarGrafo(peso, caminoCortoFB, f'Fuerza Bruta: {caminoCortoFB}, Distancia: {distanciaFB}')
    ResultadoF =f" {caminoCortoFB}"
    DistanciaF=f" {distanciaFB}"
    Texto1.config(state = 'normal')
    Texto1.delete(0, END)
    Texto1.insert(0, ResultadoF)
    Texto1.config(state = 'readonly')

    Texto1_1.config(state = 'normal')
    Texto1_1.delete(0, END)
    Texto1_1.insert(0, DistanciaF)
    Texto1_1.config(state = 'readonly')
    
    
#################### Ventana/Interfaz ##################################

Ventana = Tk()
Ventana.title("Algoritmo Metahuristico")

# Crear los Label, Entry y Botones

Texto1 = Entry(Ventana, width=30)
Texto1_1= Entry (Ventana, width = 30)
Texto2 = Entry(Ventana, width=30)
Texto2_1= Entry (Ventana , width=30)


Boton1 = Button(Ventana, text="Fuerza Bruta", command=GrafoF, bg="lightgreen", fg="black")
Boton2 = Button(Ventana, text="Divide y Venceras", command=GrafoD, bg="lightgreen", fg="black")

Fuerza = Label(Ventana, text="Fuerza Bruta", bg="lightgray", fg="black")
Divide = Label(Ventana, text="Divide y Venceras", bg="lightgray", fg="black")

ResultadoCamino1 = Label(Ventana, text="Camino")
ResultadoDistancia1 = Label(Ventana, text="Distancia")
ResultadoCamino2 = Label(Ventana, text="Camino" )
ResultadoDistancia2 = Label(Ventana, text="Distancia")

# Crear los Entry
Texto1 = Entry(Ventana, width=30)
Texto1_1 = Entry(Ventana, width=30)
Texto2 = Entry(Ventana, width=30)
Texto2_1 = Entry(Ventana, width=30)

# Configuración de los Entry para que sean de solo lectura
Texto1.config(state='readonly')
Texto1_1.config(state='readonly')
Texto2.config(state='readonly')
Texto2_1.config(state='readonly')

# Configuración de la ventana
Fuerza.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
Divide.grid(row=0, column=2, padx=10, pady=10, columnspan=2)

# Layout para "Fuerza Bruta"
ResultadoCamino1.grid(row=1, column=0, padx=10, pady=5, sticky=E)
Texto1.grid(row=1, column=1, padx=10, pady=5)
ResultadoDistancia1.grid(row=2, column=0, padx=10, pady=5, sticky=E)
Texto1_1.grid(row=2, column=1, padx=10, pady=5)
Boton1.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Layout para "Divide y Venceras"
ResultadoCamino2.grid(row=1, column=2, padx=10, pady=5, sticky=E)
Texto2.grid(row=1, column=3, padx=10, pady=5)
ResultadoDistancia2.grid(row=2, column=2, padx=10, pady=5, sticky=E)
Texto2_1.grid(row=2, column=3, padx=10, pady=5)
Boton2.grid(row=3, column=2, columnspan=2, padx=10, pady=5)



Ventana.mainloop()
