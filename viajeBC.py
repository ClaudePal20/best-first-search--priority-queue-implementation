import tkinter as tk
from tkinter import ttk, messagebox
from queue import PriorityQueue

def crear_grafo():
    return {}

def agregar_nodo(event):
    x, y = event.x, event.y
    nodo_nombre = entrada_nombre.get()
    if nodo_nombre and nodo_nombre not in grafo:
        grafo[nodo_nombre] = {"x": x, "y": y, "conexiones": {}}
        canvas.create_rectangle(x - CELL_SIZE // 2, y - CELL_SIZE // 2, x + CELL_SIZE // 2, y + CELL_SIZE // 2, fill="blue")
        lista_nodos.insert(tk.END, nodo_nombre)

def quitar_nodo():
    seleccionado = lista_nodos.get(tk.ACTIVE)
    if seleccionado:
        del grafo[seleccionado]
        canvas.delete("all")
        for nodo, info in grafo.items():
            x, y = info["x"], info["y"]
            canvas.create_rectangle(x - CELL_SIZE // 2, y - CELL_SIZE // 2, x + CELL_SIZE // 2, y + CELL_SIZE // 2, fill="blue")
        lista_nodos.delete(tk.ACTIVE)

def agregar_arista():
    nodo1 = entrada_nodo1.get()
    nodo2 = entrada_nodo2.get()
    peso = entrada_peso.get()

    if nodo1 in grafo and nodo2 in grafo and peso:
        grafo[nodo1]["conexiones"][nodo2] = int(peso)
        grafo[nodo2]["conexiones"][nodo1] = int(peso)  # La arista es bidireccional
        lista_aristas.insert(tk.END, f"{nodo1} - {nodo2} (Peso: {peso})")

        x1, y1 = grafo[nodo1]["x"], grafo[nodo1]["y"]
        x2, y2 = grafo[nodo2]["x"], grafo[nodo2]["y"]
        canvas.create_line(x1, y1, x2, y2, fill="black")
    else:
        messagebox.showerror("Error", "Asegúrate de que los nombres de los nodos existan en el grafo y de que se haya ingresado un peso.")

def encontrar_camino():
    inicio = entrada_inicio.get()
    final = entrada_final.get()
    if inicio in grafo and final in grafo:
        try:
            path = encontrar_mejor_camino(grafo, inicio, final)
            resultado_label.config(text="El mejor camino desde {} a {} es: {}\nEl peso total del camino es: {}".format(inicio, final, " -> ".join(path), calcular_peso(path)))
            dibujar_camino(path)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Asegúrate de que los nombres de inicio y final existan en el grafo.")

def dibujar_camino(path):
    canvas.delete("camino")  # Elimina todas las líneas anteriores del camino

    # Cambia el color y la desviación de la línea
    color_camino = "red"
    desviacion = 5

    for i in range(len(path) - 1):
        nodo1 = path[i]
        nodo2 = path[i + 1]
        x1, y1 = grafo[nodo1]["x"], grafo[nodo1]["y"]
        x2, y2 = grafo[nodo2]["x"], grafo[nodo2]["y"]

        # Calcula las coordenadas con desviación
        x1_desviado = x1 + desviacion
        y1_desviado = y1 + desviacion
        x2_desviado = x2 + desviacion
        y2_desviado = y2 + desviacion

        # Dibuja la línea resaltada
        canvas.create_line(x1_desviado, y1_desviado, x2_desviado, y2_desviado, fill=color_camino, width=2, tags="camino")

def encontrar_mejor_camino(grafo, inicio, final):
    visitados = set()
    cola_prioridad = PriorityQueue()
    cola_prioridad.put((0, inicio))
    padres = {}

    while not cola_prioridad.empty():
        _, nodo_actual = cola_prioridad.get()
        visitados.add(nodo_actual)

        if nodo_actual == final:
            return reconstruir_camino(padres, inicio, final)

        for vecino, peso in grafo[nodo_actual]["conexiones"].items():
            if vecino not in visitados:
                cola_prioridad.put((peso, vecino))
                padres[vecino] = nodo_actual

    raise Exception("No hay camino disponible entre {} y {}".format(inicio, final))

def reconstruir_camino(padres, inicio, final):
    camino = [final]
    while final != inicio:
        final = padres[final]
        camino.append(final)
    return camino[::-1]

def calcular_peso(camino):
    peso = 0
    for i in range(len(camino) - 1):
        nodo1 = camino[i]
        nodo2 = camino[i + 1]
        peso += grafo[nodo1]["conexiones"][nodo2]
    return peso

# Tamaño de las celdas del grid
CELL_SIZE = 20

# Crear el grafo
grafo = crear_grafo()

# Crear la ventana
ventana = tk.Tk()
ventana.title("Grafo Interactivo")

# Crear el canvas para el grid
canvas = tk.Canvas(ventana, width=400, height=400, bg="white")
canvas.pack(side=tk.LEFT)
canvas.bind("<Button-1>", agregar_nodo)

# Etiquetas y entradas para agregar nodos y aristas
etiqueta_nombre = ttk.Label(ventana, text="Nombre del Nodo:")
entrada_nombre = ttk.Entry(ventana)
etiqueta_nodo1 = ttk.Label(ventana, text="Nodo 1:")
entrada_nodo1 = ttk.Entry(ventana)
etiqueta_nodo2 = ttk.Label(ventana, text="Nodo 2:")
entrada_nodo2 = ttk.Entry(ventana)
etiqueta_peso = ttk.Label(ventana, text="Peso:")
entrada_peso = ttk.Entry(ventana)
boton_agregar_arista = ttk.Button(ventana, text="Agregar Arista", command=agregar_arista)
boton_quitar_nodo = ttk.Button(ventana, text="Quitar Nodo", command=quitar_nodo)

etiqueta_nombre.pack()
entrada_nombre.pack()
etiqueta_nodo1.pack()
entrada_nodo1.pack()
etiqueta_nodo2.pack()
entrada_nodo2.pack()
etiqueta_peso.pack()
entrada_peso.pack()
boton_agregar_arista.pack()
boton_quitar_nodo.pack()

# Listbox de nodos con barra de desplazamiento
frame_lista_nodos = ttk.Frame(ventana)
frame_lista_nodos.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
scrollbar_nodos = tk.Scrollbar(frame_lista_nodos, orient=tk.VERTICAL)
lista_nodos = tk.Listbox(frame_lista_nodos, yscrollcommand=scrollbar_nodos.set, selectmode=tk.SINGLE)
scrollbar_nodos.config(command=lista_nodos.yview)
scrollbar_nodos.pack(side=tk.RIGHT, fill=tk.Y)
lista_nodos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Listbox de aristas con barra de desplazamiento
frame_lista_aristas = ttk.Frame(ventana)
frame_lista_aristas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
scrollbar_aristas = tk.Scrollbar(frame_lista_aristas, orient=tk.VERTICAL)
lista_aristas = tk.Listbox(frame_lista_aristas, yscrollcommand=scrollbar_aristas.set, selectmode=tk.SINGLE)
scrollbar_aristas.config(command=lista_aristas.yview)
scrollbar_aristas.pack(side=tk.RIGHT, fill=tk.Y)
lista_aristas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Etiquetas y entradas para encontrar el mejor camino
etiqueta_inicio = ttk.Label(ventana, text="Punto de Inicio:")
entrada_inicio = ttk.Entry(ventana)
etiqueta_final = ttk.Label(ventana, text="Punto Final:")
entrada_final = ttk.Entry(ventana)
boton_encontrar_camino = ttk.Button(ventana, text="Buscar Camino", command=encontrar_camino)
resultado_label = ttk.Label(ventana, text="")

etiqueta_inicio.pack()
entrada_inicio.pack()
etiqueta_final.pack()
entrada_final.pack()
boton_encontrar_camino.pack()
resultado_label.pack()

# Iniciar la aplicación
ventana.mainloop()
