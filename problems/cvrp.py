from dataclasses import dataclass
import numpy as np

from .definitions import ProblemDefinition


@dataclass
class CityNode:
    id: int
    x_coord: int
    y_coord: int
    demand: int


class CvrpState:
    """Holds the current state"""

    def __init__(self) -> None:
        self.sol_path = np.array([])
    
    def get_cvrp_sol(self) -> np.ndarray:
        """
        Puts depot nodes inbetween sol_path each time the maximum capacity is reached
        """

class Cvrp:
    """
    Cvrp specific attributes
    """

    def __init__(self, path: str):
        self._file_path = path
        # Distance between cities
        self.distance_matrix = None
        # np.ndarray[CityNode]
        self.cities = None
        # int
        self.depot_id = None
        # int
        self.truck_capacity = None
    
    def read_from_file(self) -> None:
        pass
        
