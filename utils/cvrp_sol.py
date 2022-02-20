import sys
import math
from .cvrp import Cvrp
from .cvrp_state import Cvrp_state
# import string as str


class Cvrp_sol:
    """
    """

    def __init__(
		self,
		routes,
        cost
	):
         self.routes = routes
         self.cost = cost
         

    def __str__(self):
        s = "Solução: \n"
        s += "      Rotas: \n"
        for route in self.routes:
            s += "            " + str(route)
            s += "\n"
        s += "      Custo: " + str(self.cost)
        s += "\n"
        return s

    def state_to_sol(self, problem: Cvrp, state: Cvrp_state):
        warehouse = 0 # O caminhão inicia do galpão
        previous_city = 0
        new_route = []
        current_truck_capacity = 0
        max_truck_capacity = problem.truck_capacity
        cost = 0
        
        for current_city in state.sol_path:
            if new_route == []:
                new_route.append(int(current_city))
                current_truck_capacity += problem.demands[int(current_city)]
                cost += problem.compute_distance_warehouses(int(current_city))
            else:
                if (current_truck_capacity + problem.demands[int(current_city)] < max_truck_capacity):
                    new_route.append(int(current_city))
                    current_truck_capacity += problem.demands[int(current_city)]
                    cost += problem.compute_distance_cities(previous_city, current_city)
                else:
                    current_truck_capacity = 0
                    self.routes.append(new_route)
                    # print(new_route)
                    # return
                    new_route = []
                    new_route.append(int(current_city))
                    cost += problem.compute_distance_warehouses(int(current_city))

            previous_city = current_city
        self.routes.append(new_route)
        # print(new_route)
        self.calc_cost(problem)
        # print(self.cost)
            

    # Calcula o custo de uma dada solução
    # Os vários "int()" são para converter o conteúdo da lista de string para interios
    # Os vários "-1" são para corrigir os valores, pois as cidades são numeradas de 1 a n
    # enquanto vetores em python são contados de 0 a 30.
    def calc_cost(self, problem: Cvrp ):
        cost = 0
        # print(self.routes)
        for route in self.routes:
            first_city = int(route[0]) - 1
            last_city_index = int(len(route))-1
            last_city = int(route[last_city_index]) -1

            if(first_city != last_city):
                previous_city = first_city
                for current_city in route:
                    current_city = int(current_city)- 1
                    cost += problem.compute_distance_cities(int( previous_city), int(current_city))
                    previous_city = current_city
            
            cost += problem.compute_distance_warehouses(first_city)
            cost += problem.compute_distance_warehouses(last_city)
            # return
        
        # print(cost)
        self.cost = cost
        return cost

