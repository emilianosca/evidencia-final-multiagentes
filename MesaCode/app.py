"""
Evidencia 2 Multiagentes

Miguel Pedraza A01284469

"""

# ------------------------------------ Imports ------------------------------------

# Importamos flask
from flask import Flask, request, jsonify

# Importamos de mesa Agent y Model
from mesa import Agent, Model 

# Importamos nuestro grid de manera Multigrid que permite que puedan existir multiples agentes en una celda
from mesa.space import MultiGrid 

# Definimos el tiempo en el que se realizan los pasos, en este caso SimultaneousActivation hace que en cada paso todas las aspiradoras se tienen que mover
from mesa.time import SimultaneousActivation

# Traemos una manera de poder recolectar información con el data collector
from mesa.datacollection import DataCollector

# Importamos numpy, pandas y random para facilitar operaciones
import numpy as np
import pandas as pd
import random

# Importamos el tiempo para poder determinar como funciona el programa
import time
import datetime

# ------------------------------------ Termina imports ------------------------------------

# ------------------------------------ Agentes y modelos ------------------------------------

# Funcion para poder determinar los colores en la animacion y asignar cuales son aspiradoras en la habitacion
def obtener_grid(modelo):
    habitacion = np.zeros((modelo.grid.width, modelo.grid.height))
    for celda in modelo.grid.coord_iter():
        contenido_celda, x, y = celda
        for contenido in contenido_celda:
            if isinstance(contenido, Semaforo):
                habitacion[x][y] = contenido.estado                
            elif isinstance(contenido, Carro):
                habitacion[x][y] = 4      
            elif isinstance(contenido, not Carro and not Semaforo):
                habitacion[x][y] = 7
    return habitacion

# Clase carro que es nuestro primer agente
class Carro(Agent):
    def __init__(self, id_unico, modelo, ruta, posicion_actual):
        super().__init__(id_unico, modelo)
        self.posicionesUnity = []
        self.posicion_actual = posicion_actual
        self.nueva_posicion = None
        self.posicionIndex = 0 # Representa el indice de la lista de la ruta en la que vamos
        # Rutas dependiendo del carril en el que se encuentra
        self.ruta1 = [
            [(4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7)],
            [(4,0), (4,1), (4,2), (4,3), (5,3), (6,3), (7,3)]
        ]
        self.ruta2 = [
            [(3,7), (3,6), (3,5), (3,4), (3,3), (3,2), (3,1), (3,0)],
            [(3,7), (3,6), (3,5), (3,4), (2,4), (1,4), (0,4)]
        ]
        self.ruta3 = [
            [(0,3), (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3)],
            [(0,3), (1,3), (2,3), (3,3), (3,2), (3,1), (3,0)]
        ]
        self.ruta4 = [
            [(7,4), (6,4), (5,4), (4,4), (3,4), (2,4), (1,4), (0,4)],
            [(7,4), (6,4), (5,4), (4,4), (4,5), (4,6), (4,7)]
        ]
        # Guardamos el numero de ruta que tomara
        self.ruta = ruta
        # Lista de todas las rutas disponibles
        self.rutas = [self.ruta1, self.ruta2, self.ruta3, self.ruta4]
        # Obtenemos cual de las dos rutas seguira de manera random
        self.pathChoice = random.randint(0, 1)
    
    def step(self):        
        # Revisamos si la posicion actual es donde se encuentra de lado de un semaforo 
        if self.posicion_actual == self.rutas[self.ruta][self.pathChoice][2]:  
            # De ser así entonces revisamos nuestros vecinos para almacenarlos en una variable
            vecinos = self.model.grid.get_neighbors(
                self.pos,
                moore = True
            )        

            # Ahora recorreremos nuestros vecinos
            for vecino in vecinos:               
                # Si uno de los vecinos es una instancia de un agente semaforo y se encuentra en rojo (Rojo = 1)
                if isinstance(vecino, Semaforo) and vecino.estado == 1:
                    # De ser asi asignamos que la nueva posicion sera la posicion actual, es decir, no nos movemos
                    self.nueva_posicion = self.posicion_actual
                elif isinstance(vecino, Semaforo) and vecino.estado == 2:                    
                    # De lo contario si hay un semaforo pero su estado es 2 (Verde = 2) entonces revisamos que aun 
                    # estemos dentro de la ruta y avanzamos
                    if self.posicionIndex < len(self.rutas[self.ruta][self.pathChoice]):   
                        # Si es asi cambiamos la nueva posicion y aumentamos el indice de posicion en la ruta
                        self.nueva_posicion = self.rutas[self.ruta][self.pathChoice][self.posicionIndex]                        
                        self.posicionIndex = self.posicionIndex + 1
        else:
            # En caso de que no estemos de lado de un semaforo simplemente avanzamos
            if self.posicionIndex < len(self.rutas[self.ruta][self.pathChoice]):                           
                self.nueva_posicion = self.rutas[self.ruta][self.pathChoice][self.posicionIndex]                
                self.posicionIndex = self.posicionIndex + 1
        self.posicionesUnity.append(self.nueva_posicion)
    
    def advance(self):
        # Actualizamos la posicon actual a la nueva posicon y ponemos dicho agente en la nueva posicion
        self.posicion_actual = self.nueva_posicion        
        self.model.grid.move_agent(self, self.posicion_actual)

# Clase semaforo que es nuestro segundo y ultimo agente
class Semaforo(Agent):
    # VERDE = 2
    # ROJO = 1
    
    def __init__(self, unique_id, modelo, pos):
        super().__init__(unique_id, modelo) #Datos iniciales que se usan para el Agent
        self.posicion = pos 
        self.siguiente_estado = None
        # Asignamos dos listas con los dos semaforos que estan unidos 
        self.semaforos1 = [(2, 2), (5, 5)]
        self.semaforos2 = [(2, 5), (5, 2)]
        # Asignamos los semaforos en la primera lista en 1, es decir rojo, y verde los otros, 2
        self.estado = 1 if self.posicion in self.semaforos1 else 2
        self.steps = 10
        
    def step(self):        
        # Asignamos que el tiempo de cambio entre verde y rojo son 10 steps
        if self.steps <= 0:
            # Cuando termine el contador de steps entonces cambiamos el estado al contrario y reiniciar 
            # el contador
            self.siguiente_estado = 2 if self.estado == 1 else 1
            self.steps = 10
        else:
            # De lo contario seguimos asignando el mismo estado y decrementamos el contador
            self.siguiente_estado = self.estado
            self.steps -= 1
            
    def advance(self):
        # Actualizamos el estado
        self.estado = self.siguiente_estado
        
# Clase Interseccion que representa nuestro modelo
class Interseccion(Model):    
    def __init__(self, num_agentes):
        self.num_agentes = num_agentes        
        self.grid = MultiGrid(8, 8, True)
        self.schedule = SimultaneousActivation(self)             
        # Esta lista sera utilizada para mandar por json usando flask
        self.carros = []    
        
        # Primero generamos las posiciones de nuestros 4 semaforos
        pos = [(2, 2), (2, 5), (5, 2), (5, 5)]
        for i in range(4):
            semaforo = Semaforo(i, self, pos[i])
            self.grid.place_agent(semaforo, pos[i])
            self.schedule.add(semaforo)
        
        # Posicionar carros    
        posicionIncialCarros = [(4,0), (3, 7), (0, 3), (7, 4)]
        for i in range(num_agentes):
            carro = Carro(i + 4, self, i, posicionIncialCarros[i])
            self.carros.append(carro)
            self.grid.place_agent(carro, posicionIncialCarros[i])
            self.schedule.add(carro)
            
        # Usamos data collector para almacenar informacion que se nos pidió
        self.colectordatos = DataCollector(
            # Definimos colectores a nivel de modelo para ver toda la habitacion y a nivel de agente para ver cada movimiento de los agentes
            model_reporters = {'Interseccion' : obtener_grid},
        )    

    #Funcion que se usa para mandar el json. Se recorre la lista de coches y se manda su info
    def generateJson(self):        
        data = []
        for carro in self.carros:            
            pos = {
                'id': str(carro.unique_id),
                'camino': carro.posicionesUnity,                
            }                              
            data.append(pos)            
        return jsonify({'posiciones':data})
        
    def step(self):
        # Cada step hacemos que se colecten los datos definidos
        self.colectordatos.collect(self)
        self.schedule.step()

# ------------------------------------ Termina agentes y modelos ------------------------------------

# ------------------------------------ Main ------------------------------------

# Solicitamos el número de agentes
num_agentes = 4

# Tiempo maximo de ejercución (segundos)
tMax = 0.004

# Corremos hasta que termine el tiempo
start_time = time.time()
tiempo_inicio = str(datetime.timedelta(seconds = tMax))
modelo = Interseccion(num_agentes)

# Tamaño del tablero
width = 10
height = 10

# Lista numero de agentes
agents = []

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def boidPosition():    
    if request.method == 'GET':
        return modelo.generateJson()
    elif request.method == 'POST':
        return "Post request from Boids example\n"

@app.route('/init', methods=['POST', 'GET'])
def boidsInit():
    global agents
    if request.method == 'GET':
        # Set the number of agents here:
        flock = [4]
        return jsonify({"num_agents":4, "w": 10, "h": 10})
    elif request.method == 'POST':
        return "Post request from init\n"

if __name__ == "__main__":
    app.run(debug=True)

while((time.time() - start_time) < tMax):
    modelo.step()
    
# Imprimimos el timepo que le tomó correr al modelo
tiempo_ejecucion = str(datetime.timedelta(seconds = (time.time() - start_time)))

# ------------------------------------ Termina main ------------------------------------