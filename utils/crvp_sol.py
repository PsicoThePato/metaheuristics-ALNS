import sys
import math
from .crvp import crvp
# import string as str


class crvp_sol:
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

    def calc_cost(self, problem: crvp):
        cost = 0
        print(self.routes)
        for route in self.routes:
            first_city = int(route.pop(0))
            last_city = int(route.pop(len(route)-1))
            cost += problem.compute_distance_warehouses(first_city)

            last_city = route.pop(0)
            for current_city in route:
                cost += problem.compute_distance_cities(int(last_city), int(current_city))
                last_city = int(current_city)
            cost += problem.compute_distance_warehouses(last_city)
        
        print(cost)

