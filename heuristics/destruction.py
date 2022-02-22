import sys
sys.path.append("..") # Adds higher directory to python modules path.
from utils.cvrp import Cvrp
from utils.cvrp_sol import Cvrp_sol
from utils.cvrp_state import Cvrp_state
import random
import numpy as np


def random_destroyer (intensity: float, state: Cvrp_state, problem: Cvrp,):
    if intensity == 0:
        return state
    state.deleted_cities = []
    # print("Random intensity:",intensity, " ", len(state.sol_path))
    # print("Random intensity2:", (intensity * len(state.sol_path)))
    state.deleted_cities_index = []
    intensity = int(intensity * len(state.sol_path))
    # print("Random intensity2:",intensity)
    # print(state.sol_path)
    loop = random.sample(range(0,len(state.sol_path)), intensity)
    # print("loop: ",loop)
    for i in loop:
        
        state.deleted_cities.append(state.sol_path[i])
        state.deleted_cities_index.append(i)
        state.sol_path[i] = -1

    # print("Cidades removidas: ",state.deleted_cities)
    # print("Index das cidades removidas: ",state.deleted_cities_index)
    # print("Vetor de cidades após remoção: ",state.sol_path)
    return state


    # print(sol.routes)

def worst_destroyer (intensity: float, state: Cvrp_state, problem: Cvrp,):
    # print("worst intensity:",intensity, " ", len(state.sol_path))
    # print("worst intensity2:", (intensity * len(state.sol_path)))
    if intensity == 0:
        return
    state.deleted_cities = []
    state.deleted_cities_index = []
    # print("Worst intensity0:",intensity)
    # print("Worst intensity:", intensity, " ", len(state.sol_path))
    # print(state.sol_path)
    intensity = int(intensity * len(state.sol_path))
    # print("Worst intensity2:",intensity)
    state_distance = []
    previus_city = state.sol_path[0]
    for current_city in state.sol_path[1:]:
        state_distance.append(problem.compute_distance_cities(previus_city, current_city))
        previus_city = current_city

    state_distance_aux = state_distance.copy()
    state_distance.sort()
    # print(state.sol_path)
    # print("Lista de distâncias entre cidades: ",state_distance_aux)
    # print("Lista de distâncias entre cidades ordenada: ",state_distance)

    for i in range(intensity):
        # o "-i-1" serve para evitar o valor 0, pois o for irá percorrer de 0 a intensity a princípio
        # print(state_distance[-i-1]) # Percorre os valores do maior para o menor
        # print(state_distance_aux.index(state_distance[-i-1])) #pega o index do mesmo na lista original de distancias
        # print(state.sol_path[state_distance_aux.index(state_distance[-i-1])]) # o index se refere a um vertice na tsp(state do problema)
        index_deleted = state_distance_aux.index(state_distance[-i-1])
        value_deleted = state.sol_path[index_deleted]
        state.deleted_cities_index.append(index_deleted) # guarda o index do valor removido
        state.deleted_cities.append(value_deleted) # guarda valor removido

        state.sol_path[index_deleted] = -1
        state_distance_aux[index_deleted] = -1 # uma vez q a cidade é removida a distância tb deve ser removida
        # pois não será mais usada, porém sua posição deve ser preservada para não adulterar as demais posições.
        # por isso é atribuido um valor negativo, pois não haverá cidades de valor negativo.
        # print("\n")
    # print("Cidades removidas: ",state.deleted_cities)
    # print("Index das cidades removidas: ",state.deleted_cities_index)
    # print("Vetor de cidades após remoção: ",state.sol_path)

    return state