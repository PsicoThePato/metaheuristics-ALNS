from os import remove
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from utils.cvrp import Cvrp
from utils.cvrp_sol import Cvrp_sol
from utils.cvrp_state import Cvrp_state
import random
import numpy as np
import copy 

def random_constructor (old_state: Cvrp_state, problem: Cvrp):
    state = copy.copy(old_state)
    # print("--------------random_constructor--------------")
    for city in state.deleted_cities:
        remove_index = state.deleted_cities_index.pop(random.randrange(len(state.deleted_cities_index)))
        # print("index: ",remove_index, " City: ",city)
        state.sol_path[remove_index] = city
    return state
    
    # print(state.sol_path)

def greedy_constructor (old_state: Cvrp_state, problem: Cvrp):
    state = copy.copy(old_state)
    # print("--------------greedy_constructor--------------")
    best_cost = 999999
    current_cost = 0
    selected_index = 0
    
    # para cada cidade tentar inserir em um dos indices
    # disponíveis na state.sol_path (TSP), essa tentativa
    # busca inserir a cidade que irá gerar menor vusto 
    for city in state.deleted_cities:
        for city_index in state.deleted_cities_index:
            if city_index-1 >= 0:
                current_cost += problem.compute_distance_cities(city,
                    state.sol_path[city_index-1])
            if city_index+1 < len(state.sol_path):
                current_cost += problem.compute_distance_cities(city,
                    state.sol_path[city_index+1])
            # if(current_cost == 0):
            #     print("Cidade problema fora: ", city)
            #     print("Cidade problema dentro: ", state.sol_path[city_index])
            #     print("cidades vizinhas: ", state.sol_path[city_index-1], " ", state.sol_path[city_index+1])
            #     return
            # print("fora", current_cost)
            if best_cost > current_cost:
                # print("dentro",current_cost)
                state.sol_path[city_index] = city
                selected_index = city_index
                best_cost = current_cost
            current_cost = 0
        state.deleted_cities_index.remove(selected_index)
        best_cost = 99999
        # print()
        

    # print("deleted index: ",state.deleted_cities_index)
    # print("state tsp: ", state.sol_path)
    return state
