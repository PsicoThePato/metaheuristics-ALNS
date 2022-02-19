import sys
sys.path.append("..") # Adds higher directory to python modules path.
from utils.crvp import crvp
from utils.crvp_sol import crvp_sol
import random

def random_destroyer ( intensity: int , problem: crvp, sol: crvp_sol  ):
    # print(sol.routes)
    i = 0
    for r in sol.routes:
        for x in r:
            # print(x)
            i = i+int(x)
    # print(i)

    for i in range(problem.nb_citys):
        random_select = random.randrange(0, 20)
        if(random_select > 10): # 50 < probabilidade
            continue

        random_route = random.randrange(0, len(sol.routes)-1)
        route_len = len(sol.routes[random_route])-1
        if(route_len):
            random_index = random.randrange(0, route_len)
            sol.routes[random_route].pop(random_index)
    
    # print(sol.routes)