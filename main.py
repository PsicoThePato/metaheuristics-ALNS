import sys
import math
# sys.path.append('./')
from utils.crvp import crvp
import utils.cvrp_factory as cvrp_factory
from utils.crvp_sol import crvp_sol
import utils.crvp_sol_factory as crvp_sol_factory
import destruction_heuristics.random_destroyer as rd


def main(instance_file):
    print(instance_file)
    print(sol_file)
    nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands, nb_trucks = cvrp_factory.factory(instance_file, 0, 0, 0)
    test_crvp = crvp(nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands, nb_trucks)
    routes, const = crvp_sol_factory.factory(sol_file)
    test_crvp_sol = crvp_sol(routes,const)
    # print(test_crvp)
    # print(test_crvp_sol)
    # rd.random_destroyer(2,test_crvp, test_crvp_sol)
    # test_crvp_sol.calc_cost(test_crvp)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cvrp.py input_file [output_file] [time_limit] [nb_trucks]")
        sys.exit(1)

    instance_file = sys.argv[1]
    sol_file = sys.argv[2] if len(sys.argv) > 2 else None
    str_time_limit = sys.argv[3] if len(sys.argv) > 3 else "20"
    str_nb_trucks = sys.argv[4] if len(sys.argv) > 4 else "0"

    main(instance_file)
