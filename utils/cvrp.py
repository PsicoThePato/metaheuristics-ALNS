import sys
import math
# import string as str


class Cvrp:
    """
    """

    def __init__(
		self,
		nb_citys,
		truck_capacity,
		distance_matrix,
		distance_warehouses,
		demands,
		nb_trucks,
	):
         self.nb_citys = nb_citys
         self.truck_capacity = truck_capacity
         #distancia entre as cidades, arestas da matrix
         self.distance_matrix = distance_matrix 
         self.distance_warehouses = distance_warehouses
         self.demands = demands
         self.nb_trucks = nb_trucks

    def __str__(self):
        s = "Entrada:\n"
        s += "      Cidades atendidas: " + str(self.nb_citys) + "\n" 
        s += "      Número de caminhões:  " + str(self.nb_trucks) + "\n"
        s += "      Capacidade máxima: " + str(self.truck_capacity) + "\n"
        s += "      Distâncias entre cidades: \n"
        for x in self.distance_matrix:
            s += "            "  + str(x)
            s += "\n"
        #    print (x, " ", len(distance_matrix))
        # print("Total de membros da distance matrix: ", len(distance_matrix))
        
        s += "      Demanda das cidades: " + str(self.demands) + " " + str(len(self.demands)) + "\n"
        s += "      Distâncias entre as cidades e o depósito: " + str(self.distance_warehouses) + " "  + str(len(self.distance_warehouses))
        s += "\n"
        return s

    def compute_distance_warehouses(self, index: int):
        return self.distance_warehouses[index]

    # Retorna distância entre uma "city1" e "city2"
    def compute_distance_cities(self, index_city1: int, index_city2: int):
        # print(index_city1, index_city2)
        # print(self.distance_matrix[index_city1])
        # print(self.distance_matrix[index_city1][index_city2])
        return self.distance_matrix[index_city1][index_city2]
    

