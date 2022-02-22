from dataclasses import dataclass
import numpy as np
import random

from .cvrp import Cvrp


# from .definitions import ProblemDefinition


@dataclass
class CityNode:
    id: int
    x_coord: int
    y_coord: int
    demand: int


class Cvrp_state:
    """Holds the current state"""

    def __init__(self, cvrp_input: Cvrp) -> None:
        salesman_array = random.sample(range(cvrp_input.nb_citys), cvrp_input.nb_citys)
        # print(salesman_array)
        self.sol_path = np.array(salesman_array)
        self.deleted_cities = []
        self.deleted_cities_index = []
    
    def get_cvrp_sol(self, cvrp_input: Cvrp) -> np.ndarray:
        """
        Puts depot nodes inbetween sol_path each time the maximum capacity is reached
        """


# class Cvrp:
#     """
#     Cvrp specific attributes
#     """

#     def __init__(self, path: str): 
#         self._file_path = path
#         # CvrpState
#         self.state = None
#         # np.ndarray[CityNode]
#         self.cities = None
#         # int
#         self.depot_id = None
#         # int
#         self.truck_capacity = None
    
#     def read_from_file(self) -> None:
#         pass
        
