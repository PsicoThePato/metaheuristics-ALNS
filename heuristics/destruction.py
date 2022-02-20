import sys
sys.path.append("..") # Adds higher directory to python modules path.
from utils.cvrp import Cvrp
from utils.cvrp_sol import Cvrp_sol
from utils.cvrp_state import Cvrp_state
import random
import numpy as np


def random_destroyer ( problem: Cvrp, state: Cvrp_state, intensity: int  ):
    if intensity == 0:
        return
    intensity = int(intensity/100 * len(state.sol_path))
    print(state.sol_path)
    for _ in range(intensity):
        i = int(random.randrange(0, intensity) - 1)
        state.sol_path = np.delete(state.sol_path, i)
    print(state.sol_path)


    # print(sol.routes)

def worst_destroyer ( problem: Cvrp, state: Cvrp_state, intensity: float):
    if intensity == 0:
        return
    intensity = int(intensity/100 * len(state.sol_path))
    state_distance = []
    previus_city = state.sol_path[0]
    for current_city in state.sol_path[1:]:
        state_distance.append(problem.compute_distance_cities(previus_city, current_city))
        previus_city = current_city

    state_distance_aux = state_distance.copy()
    state_distance.sort()
    print(state.sol_path)
    print(state_distance)
    print(state_distance_aux)

    for i in range(intensity):
        # print(state_distance[-i-1]) # Percorre os valores do maior para o menor
        # print(state_distance_aux.index(state_distance[-i])) #pega o index do mesmo na lista original de distancias
        # print(state.sol_path[state_distance_aux.index(state_distance[-i])]) # o index se refere a um vertice na tsp(state do problema)
        np.delete(state.sol_path, state_distance_aux.index(state_distance[-i]))
        # print("\n")
    print(state.sol_path)

