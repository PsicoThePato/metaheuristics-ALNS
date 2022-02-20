import sys
import math
# sys.path.append('./')
from utils.cvrp import Cvrp
import utils.cvrp_factory as cvrp_factory
from utils.cvrp_sol import Cvrp_sol
import utils.cvrp_sol_factory as Cvrp_sol_factory
from utils.cvrp_state import Cvrp_state 
import heuristics.destruction


def main(instance_file):
    print(instance_file)
    print(sol_file)
    nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands, nb_trucks = cvrp_factory.factory(instance_file, 0, 0, 0)
    cvrp_test = Cvrp(nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands, nb_trucks)
    # print(cvrp_test)
    cvrp_state = Cvrp_state(cvrp_test)
    cvrp_sol = Cvrp_sol([], 0)
    cvrp_sol.state_to_sol(cvrp_test, cvrp_state)
    # heuristics.destruction.random_destroyer(cvrp_test,cvrp_state)
    heuristics.destruction.worst_destroyer(cvrp_test, cvrp_state, 5)

    # routes, const = Cvrp_sol_factory.factory(sol_file)
    # test_crvp_sol = Cvrp_sol(routes,const)
    # print(test_crvp_sol)
    # print(cvrp_sol)

    

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cvrp.py input_file [output_file] [time_limit] [nb_trucks]")
        sys.exit(1)

    instance_file = sys.argv[1]
    sol_file = sys.argv[2] if len(sys.argv) > 2 else None
    str_time_limit = sys.argv[3] if len(sys.argv) > 3 else "20"
    str_nb_trucks = sys.argv[4] if len(sys.argv) > 4 else "0"

    main(instance_file)
