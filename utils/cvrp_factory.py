########## cvrp.py ##########
import sys
import math

def factory(instance_file, str_time_limit, sol_file, str_nb_trucks):
    nb_trucks = int(str_nb_trucks)

    #
    # Reads instance data
    #
    (nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands) = read_input_cvrp(instance_file)

    # The number of trucks is usually given in the name of the file
    # nb_trucks can also be given in command line
    if nb_trucks == 0:
        nb_trucks = get_nb_trucks(instance_file)

    # print("Cidades atendidas: ", nb_customers)
    # print("Número de caminhões:  ", nb_trucks)
    # print("Capacidade máxima: ", truck_capacity)
    # print("Distâncias entre cidades: ")
    # for x in distance_matrix:
    #      print ("      " ,x)
    # #    print (x, " ", len(distance_matrix))
    # print("Total de membros da distance matrix: ", len(distance_matrix))
    # print ('')
    # print("Demanda das cidades: ",demands, " " ,len(demands))
    # print("Distâncias entre as cidades e o depósito: ", distance_warehouses, " " ,len(distance_warehouses))

    return nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands, nb_trucks

def read_elem(filename):
    with open(filename) as f:
        return [str(elem) for elem in f.read().split()]

# The input files follow the "Augerat" format.
def read_input_cvrp(filename):
    file_it = iter(read_elem(sys.argv[1]))

    nb_nodes = 0
    
    while (1):
        token = next(file_it)
        if token == "NAME":
            next(file_it)  # Removes the ":"
            nome = next(file_it)
        elif token == "DIMENSION":
            next(file_it)  # Removes the ":"
            nb_nodes = int(next(file_it))
            nb_customers = nb_nodes - 1
        elif token == "CAPACITY":
            next(file_it)  # Removes the ":"
            truck_capacity = int(next(file_it))
        elif token == "EDGE_WEIGHT_TYPE":
            next(file_it)  # Removes the ":"
            token = next(file_it)
            if token != "EUC_2D":
                print("Edge Weight Type " + token + " is not supported (only EUD_2D)")
                sys.exit(1)
        elif token == "NODE_COORD_SECTION":
            break

    customers_x = [None] * nb_customers
    customers_y = [None] * nb_customers
    depot_x = 0
    depot_y = 0
    for n in range(nb_nodes):
        node_id = int(next(file_it))
        if node_id != n + 1:
            print("Unexpected index")
            sys.exit(1)
        if node_id == 1:
            depot_x = int(next(file_it))
            depot_y = int(next(file_it))
        else:
            # -2 because orginal customer indices are in 2..nbNodes
            customers_x[node_id - 2] = int(next(file_it))
            customers_y[node_id - 2] = int(next(file_it))

    # Compute distance matrix
    distance_matrix = compute_distance_matrix(customers_x, customers_y)
    distance_warehouses = compute_distance_warehouses(depot_x, depot_y, customers_x, customers_y)

    token = next(file_it)
    if token != "DEMAND_SECTION":
        print("Expected token DEMAND_SECTION")
        sys.exit(1)

    demands = [None] * nb_customers
    for n in range(nb_nodes):
        node_id = int(next(file_it))
        if node_id != n + 1:
            print("Unexpected index")
            sys.exit(1)
        if node_id == 1:
            if int(next(file_it)) != 0:
                print("Demand for depot should be 0")
                sys.exit(1)
        else:
            # -2 because orginal customer indices are in 2..nbNodes
            demands[node_id - 2] = int(next(file_it))

    token = next(file_it)
    if token != "DEPOT_SECTION":
        print("Expected token DEPOT_SECTION")
        sys.exit(1)

    warehouse_id = int(next(file_it))
    if warehouse_id != 1:
        print("Warehouse id is supposed to be 1")
        sys.exit(1)

    end_of_depot_section = int(next(file_it))
    if end_of_depot_section != -1:
        print("Expecting only one warehouse, more than one found")
        sys.exit(1)

    return (nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands)


# Computes the distance matrix
def compute_distance_matrix(customers_x, customers_y):
    nb_customers = len(customers_x)
    distance_matrix = [[None for i in range(nb_customers)] for j in range(nb_customers)]
    for i in range(nb_customers):
        distance_matrix[i][i] = 0
        for j in range(nb_customers):
            dist = compute_dist(customers_x[i], customers_x[j], customers_y[i], customers_y[j])
            distance_matrix[i][j] = dist
            distance_matrix[j][i] = dist
    return distance_matrix


# Computes the distances to warehouse
def compute_distance_warehouses(depot_x, depot_y, customers_x, customers_y):
    nb_customers = len(customers_x)
    distance_warehouses = [None] * nb_customers
    for i in range(nb_customers):
        dist = compute_dist(depot_x, customers_x[i], depot_y, customers_y[i])
        distance_warehouses[i] = dist
    return distance_warehouses


def compute_dist(xi, xj, yi, yj):
    exact_dist = math.sqrt(math.pow(xi - xj, 2) + math.pow(yi - yj, 2))
    return int(math.floor(exact_dist + 0.5))


def get_nb_trucks(filename):
    begin = filename.rfind("-k")
    if begin != -1:
        begin += 2
        end = filename.find(".", begin)
        return int(filename[begin:end])
    print("Error: nb_trucks could not be read from the file name. Enter it from the command line")
    sys.exit(1)


# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         print("Usage: python cvrp.py input_file [output_file] [time_limit] [nb_trucks]")
#         sys.exit(1)

#     instance_file = sys.argv[1]
#     sol_file = sys.argv[2] if len(sys.argv) > 2 else None
#     str_time_limit = sys.argv[3] if len(sys.argv) > 3 else "20"
#     str_nb_trucks = sys.argv[4] if len(sys.argv) > 4 else "0"

#     cvrp_factory(instance_file, str_time_limit, sol_file, str_nb_trucks)
