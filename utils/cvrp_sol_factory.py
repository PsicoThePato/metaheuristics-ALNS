import sys
import math

def read_elem(filename):
    # print(filename)
    with open(filename) as f:
        return [str(elem) for elem in f.read().split()]

def read_input_cvrp_sol(filename):
    file_it = iter(read_elem(filename))
    routes = []
    route = []
    iter_routes = 0
    token = next(file_it)
    while(1):   
        while(1):
            token= next(file_it)
            if token == "Route" or token == "cost": 
                break
            if "#" in token: # ignora #<numero da rota>:
                continue
            route.append(token) # Adiciona cidade a rota
        routes.append(route) # Adiciona rota a solução
        # print(token)
        # print(route)
        route = []
        if(token == "cost"):
            cost = next(file_it) # Pega o custo da solução passada
            break

    return routes, cost

        
        

def factory(sol_file):
   routes, cost =  read_input_cvrp_sol(sol_file)

#    print(routes)
#    print(cost)
   return routes, cost
    