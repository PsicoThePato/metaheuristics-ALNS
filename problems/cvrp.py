from dataclasses import dataclass
import numpy as np
from itertools import islice

from .definitions import ProblemDefinition


@dataclass
class CityNode:
    """Node definition"""
    id: int
    x_coord: int
    y_coord: int
    demand: int=None


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

    def __init__(self, path):
        self._file_path = path
        # CvrpState
        self.state = None
        # np.ndarray[CityNode]
        self.cities = None
        # int
        self.depot_id = None
        # int
        self.truck_capacity = None
        # str
        self.problem_name = None

    def read_from_file(self) -> None:
        """
        Reads file and set Cvrp attributes
        """

        with open(self._file_path, "r", encoding="utf-8") as file_pointer:
           # header attributes
            header_raw_text = list(islice(file_pointer, 7))
            header_text_attributes = [header_raw_text[0].strip()] + [header_raw_text[3].strip()] + [header_raw_text[5].strip()]
            attribute_gen = map(lambda line: line.split(': ')[-1], header_text_attributes)
            self.problem_name = next(attribute_gen)
            dimension = int(next(attribute_gen))
            self.cities = np.empty(dimension, dtype=object)
            self.truck_capacity = int(next(attribute_gen))

            # creates cities without their demand information
            empty_city_space = 0
            while ((line := file_pointer.readline().strip()) != "DEMAND_SECTION"):
                parsed_line = line.split()
                id, x_coord, y_coord = parsed_line
                self.cities[empty_city_space] = CityNode(id, x_coord, y_coord)
                empty_city_space = empty_city_space + 1

            # adds demands on coties
            undemanding_city = 0
            while ((line := file_pointer.readline().strip()) != "DEPOT_SECTION"):
                _, city_demand = line.split()
                self.cities[undemanding_city].demand = city_demand
                undemanding_city = undemanding_city + 1

            self.depot_id = int(file_pointer.readline())


if __name__ == '__main__':
    obj = Cvrp("problems/data/A/A-n32-k5.vrp")
    obj.read_from_file()
    print("############")
    print(obj.cities)
    print(obj.depot_id)
    print(obj.truck_capacity)
