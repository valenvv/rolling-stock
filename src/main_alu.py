import json
import networkx as nx
import math
import pprint

def crearGrafo(instance, flag):
	G = nx.DiGraph()
	maxVagones = instance["rs_info"]["max_rs"]
	capacidadVagon = instance["rs_info"]["capacity"]

	# ARISTAS DE TREN
	for s in instance["services"]:
		servicio = instance["services"][s]
		tiempoPartida = servicio["stops"][0]["time"]
		tiempoArribo = servicio["stops"][1]["time"]
		cotaInferior = math.ceil(servicio["demand"][0] / capacidadVagon)
		estacionPartida = servicio["stops"][0]["station"]
		estacionArribo = servicio["stops"][1]["station"]
		G.add_edge((estacionPartida, tiempoPartida), 
					(estacionArribo, tiempoArribo), 
					capacity = maxVagones - cotaInferior,
					weight = 0)
		G.nodes[(estacionPartida, tiempoPartida)]["demand"] = cotaInferior
		G.nodes[(estacionArribo, tiempoArribo)]["demand"] = -cotaInferior
	
	# ARISTAS DE TRASPASO
	nombreEst1 = instance["stations"][0]
	nombreEst2 = instance["stations"][1]
	estacion1 = [] # Tigre en las instancias dadas
	estacion2 = [] # Retiro

	for nodo in G:
		if nodo[0] == nombreEst1:
			estacion1.append(nodo)
		else:
			estacion2.append(nodo)

	estacion1 = sorted(estacion1, key=lambda x: x[1]) # Lista ordenada con los nodos de la primera estación
	estacion2 = sorted(estacion2, key=lambda x: x[1])

	# Agregamos aristas de traspaso en la estación 1
	for i in range(len(estacion1) - 1): # para no incluir el ultimo
		G.add_edge(estacion1[i], estacion1[i + 1], capacity = math.inf, weight = 0)

	# Agregamos aristas de traspaso en la estación 2
	for i in range(len(estacion2) - 1): # para no incluir el ultimo
		G.add_edge(estacion2[i], estacion2[i + 1], capacity = math.inf, weight = 0)
	
	# Nodos extra para conexión de estaciones durante la noche
	nodoFinalEst1 = (nombreEst1,math.inf)
	nodoFinalEst2 = (nombreEst2,math.inf)

	# Aristas de traspaso que conectan el último servicio con el nuevo nodo
	G.add_edge(estacion1[-1], nodoFinalEst1, capacity = math.inf, weight = 0)
	G.add_edge(estacion2[-1], nodoFinalEst2, capacity = math.inf, weight = 0)

	# ARISTA SERVICIO NOCTURNO
	G.add_edge(nodoFinalEst1,nodoFinalEst2,capacity = math.inf, weight = 0)
	G.add_edge(nodoFinalEst2,nodoFinalEst1,capacity = math.inf, weight = 0)
	
	# Costos de las aristas de trasnoche
	costoTrasnocheEst1 = instance["cost_per_unit"][nombreEst1]
	costoTrasnocheEst2 = instance["cost_per_unit"][nombreEst2]
	
	if flag:
		# En el caso de que una estación necesite más trenes al comienzo del día de los que puede almacenar
		nodoComienzoEst1 = (nombreEst1, -1)
		nodoComienzoEst2 = (nombreEst2, -1)

		# ARISTA PRE SERVICIO 
		G.add_edge(nodoComienzoEst1,nodoComienzoEst2,capacity = math.inf, weight = 0)
		G.add_edge(nodoComienzoEst2,nodoComienzoEst1,capacity = math.inf, weight = 0)

		# ARISTA DE TRASPASO
		G.add_edge(nodoComienzoEst1, estacion1[0], capacity = math.inf, weight = 0)
		G.add_edge(nodoComienzoEst2, estacion2[0], capacity = math.inf, weight = 0)

		# ARISTA DE TRASNOCHE
		capTrasnocheEst1 = instance["rs_info"]["night_capacity"][nombreEst1]
		G.add_edge(nodoFinalEst1, nodoComienzoEst1, capacity = capTrasnocheEst1, weight = costoTrasnocheEst1)
		capTrasnocheEst2 = instance["rs_info"]["night_capacity"][nombreEst2]
		G.add_edge(nodoFinalEst2, nodoComienzoEst2, capacity = capTrasnocheEst2, weight = costoTrasnocheEst2)

	else:
		# ARISTAS DE TRASNOCHE
		G.add_edge(nodoFinalEst1, estacion1[0], capacity = math.inf, weight = costoTrasnocheEst1)
		G.add_edge(nodoFinalEst2, estacion2[0], capacity = math.inf, weight = costoTrasnocheEst2)
	
	return G

def circulacion(G, instance):
	flowDict = nx.min_cost_flow(G)
	
	capacidadVagon = instance["rs_info"]["capacity"]

	for s in instance["services"]:
		servicio = instance["services"][s]
		tiempoPartida = servicio["stops"][0]["time"]
		tiempoArribo = servicio["stops"][1]["time"]
		cotaInferior = math.ceil(servicio["demand"][0] / capacidadVagon)
		estacionPartida = servicio["stops"][0]["station"]
		estacionArribo = servicio["stops"][1]["station"]
		flowDict[(estacionPartida, tiempoPartida)][(estacionArribo, tiempoArribo)] += cotaInferior

	return flowDict

def main():

	''' Descomentar la instancia con la que se quiera trabajar '''

	filename = "instances/toy_instance.json"
	#filename = "instances/retiro-tigre-semana.json"
	#filename = "instances/maipu-delta-semana.json"
	#filename = "instances/maipu-delta-semana-HP.json" # Instancia que diferencia demanda en hora pico y no pico
	#filename = "instances/maipu-delta-finde.json"

	'''
	La variable flag determina si existe limitación en la cantidad de unidades que pueden permancer durante
	la noche en una estación.
	En el caso de que sea True, se requerirá que el json utilizado como instancia tenga "night_capacity".
	Por defecto, si la misma no se modifica, cada instancia tendrá como night_capacity la cantidad
	de unidades que permanecen en cada estación del flujo original.
	'''

	flag = False

	with open(filename) as json_file:
		data = json.load(json_file)

	G = crearGrafo(data, flag)
	estacion1 = [] # Tigre
	estacion2 = [] # Retiro
	nombreEst1 = data["stations"][0]
	nombreEst2 = data["stations"][1]

	for nodo in G:
		if nodo[0] == nombreEst1:
			estacion1.append(nodo)
		else:
			estacion2.append(nodo)
	estacion1 = sorted(estacion1, key=lambda x: x[1]) # Lista ordenada con los nodos de la primera estación
	estacion2 = sorted(estacion2, key=lambda x: x[1])
	
	flowDict = circulacion(G, data)
	print("La solución para el problema de circulación es la siguiente:")
	pprint.pprint(flowDict)
	print(f"Cantidad de vagones que permanecen en {nombreEst1}: {flowDict[estacion1[-1]][estacion1[0]]}")
	print(f"Cantidad de vagones que permanecen en {nombreEst2}: {flowDict[estacion2[-1]][estacion2[0]]}")

if __name__ == "__main__":
	main()