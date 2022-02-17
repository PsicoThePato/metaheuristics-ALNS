import sys
import math
# import string as str


class crvp:
    """
    """

    def __init__(
		self,
		nb_customers,
		truck_capacity,
		distance_matrix,
		distance_warehouses,
		demands,
		nb_trucks,
	):
         self.nb_customers = nb_customers,
         self.truck_capacity = truck_capacity,
         self.distance_matrix = distance_matrix,
         self.distance_warehouses = distance_warehouses,
         self.demands = demands,
         self.nb_trucks = nb_trucks

    def __str__(self):
        s = "Cidades atendidas: " + str(self.nb_customers) + "\n" 
        s += "Número de caminhões:  " + str(self.nb_trucks) + "\n"
        s += "Capacidade máxima: " + str(self.truck_capacity) + "\n"
        s += "Distâncias entre cidades: \n"
        for x in self.distance_matrix:
            s += "      "  + str(x) + "\n"
        #    print (x, " ", len(distance_matrix))
        # print("Total de membros da distance matrix: ", len(distance_matrix))
        
        s += "Demanda das cidades: " + str(self.demands) + " " + str(len(self.demands)) + "\n"
        s += "Distâncias entre as cidades e o depósito: " + str(self.distance_warehouses) + " "  + str(len(self.distance_warehouses))
        return s

