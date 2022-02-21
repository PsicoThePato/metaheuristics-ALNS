from copyreg import constructor
import sys
import math
# sys.path.append('./')
from utils.cvrp import Cvrp
import utils.cvrp_factory as cvrp_factory
from utils.cvrp_sol import Cvrp_sol, calc_cost_func2
from utils.cvrp_sol import calc_cost_func
import utils.cvrp_sol_factory as Cvrp_sol_factory
from utils.cvrp_state import Cvrp_state 
import heuristics.destruction as destruction
import heuristics.reconstruction as reconstruction

# alns
from meta.alns import ALNSIter
from meta.alns import StateTransition
from meta.alns import LambdaWeights
from meta.alns import ALNSProbParameters

import time

def main(instance_file):
    print(instance_file)
    print(sol_file)
    percent = 10/100
    nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands, nb_trucks = cvrp_factory.factory(instance_file, 0, 0, 0)
    cvrp_test = Cvrp(nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands, nb_trucks)
    # print(cvrp_test)
    cvrp_state = Cvrp_state(cvrp_test)
    cvrp_sol = Cvrp_sol([], 0)
    cvrp_sol.state_to_sol(cvrp_test, cvrp_state)
    # destruction.random_destroyer(cvrp_test,cvrp_state, 30)
    # destruction.worst_destroyer(cvrp_test, cvrp_state, 50)
    # reconstruction.random_constructor(cvrp_test, cvrp_state)
    # reconstruction.greedy_constructor(cvrp_test, cvrp_state)
    # print(cvrp_sol)
    cvrp_sol.state_to_sol(cvrp_test, cvrp_state)
    # print(cvrp_sol)

    destroy_heuristics = [destruction.random_destroyer, destruction.worst_destroyer]
    constructor_heuristics = [reconstruction.random_constructor, reconstruction.greedy_constructor]
    scoring_function = calc_cost_func
    # acceptance_function
    # ALNSProbbParameters
    f = 0.9
    lambd = LambdaWeights(1.0, 2.0, 3.3)
    alnsProb = ALNSProbParameters(lambd, 2, 2, 2)

   

    # print("Melhor custo: " ,calc_cost_func(alnsIter.best_state, cvrp_test))
    # alnsIter.do_alns_iteraction(50, cvrp_state, cvrp_test )
    # print()
    result = 999999
    inicio = time.time()
    for _ in range(5):
        alnsIter = ALNSIter(destroy_heuristics, constructor_heuristics, 
                        scoring_function, acceptance_function, 
                        alnsProb )
        cvrp_state = Cvrp_state(cvrp_test)
        alnsIter.do_alns_iteraction(50, cvrp_state, cvrp_test )
        best_result = calc_cost_func(alnsIter.best_state, cvrp_test)
        reduce_value = best_result*percent

        while(1):
            alnsIter.do_alns_iteraction( 50, None, cvrp_test )
            current_result = calc_cost_func(alnsIter.best_state, cvrp_test)
            # print(calc_cost_func(alnsIter.best_state, cvrp_test))
            
            if current_result <= best_result - reduce_value:
                best_result = current_result
                break
            
            # deveria ser 300 segundo o enunciado
            fim = time.time()
            if fim - inicio > 300:
                break

        if best_result < result:
            result = best_result
        
        print("Melhor custo local: " ,calc_cost_func2(alnsIter.best_state, cvrp_test))
        print("---------------------")
        print()
        return
    
    print("Melhor custo geral: " , result)

    # print("test ", alnsIter.current_state.sol_path)


    # routes, const = Cvrp_sol_factory.factory(sol_file)
    # test_crvp_sol = Cvrp_sol(routes,const)
    # print(test_crvp_sol)

    # print(cvrp_sol)

    
def acceptance_function(states ,problem:Cvrp):
    for state in states:
        if state == None:
            continue
        # print("state ",state.sol_path)
        # print("state.len ", len(state.sol_path))
        # print("pproblem.nb_citys-1", problem.nb_citys-1)
        if len(state.sol_path) != problem.nb_citys:
            # print("len(state.sol_path) != problem.nb_citys-1:")
            return False
        for city in state.sol_path:
            if city > problem.nb_citys-1:
                # print("city > problem.nb_citys-1:")
                return False
            if city < 0:
                # print("city < 0")
                return False
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cvrp.py input_file [output_file] [time_limit] [nb_trucks]")
        sys.exit(1)

    instance_file = sys.argv[1]
    sol_file = sys.argv[2] if len(sys.argv) > 2 else None
    str_time_limit = sys.argv[3] if len(sys.argv) > 3 else "20"
    str_nb_trucks = sys.argv[4] if len(sys.argv) > 4 else "0"

    main(instance_file)
