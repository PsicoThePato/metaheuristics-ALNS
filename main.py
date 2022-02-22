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
    # print(instance_file)
    # list_path = instance_file.split('/')
    # list_path[-1] = "opt-"+(list_path[-1].split('.')[0])
    # opt_path = "/".join(list_path)
    # print("opt_path: ", opt_path)

    # routes, opt_cost = Cvrp_sol_factory.read_input_cvrp_sol(opt_path)

    # percent = 20/100
    nb_customers, truck_capacity, distance_matrix, distance_warehouses, demands, nb_trucks, opt_cost = cvrp_factory.factory(instance_file, 0, 0, 0)
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
    # cvrp_sol.state_to_sol(cvrp_test, cvrp_state)
    # print(cvrp_sol)

    destroy_heuristics = [destruction.random_destroyer, destruction.worst_destroyer]
    constructor_heuristics = [reconstruction.random_constructor, reconstruction.greedy_constructor]
    scoring_function = calc_cost_func
    # acceptance_function
    # ALNSProbbParameters
    f = 0.9
    lambd = LambdaWeights(1.0, 2.0, 3.3)
    alnsProb = ALNSProbParameters(lambd, 2, 2, 2)

    # Critérios a serem registrados:
    # I) TEMPO <= 300 PARA O ALGORITMO GERAR A MELHOR SOLUÇÃO
    total_time = time.time()
    # II) NÚMERO DE ITERAÇÕES PARA O ALGORITMO GERAR A MELHOR SOLUÇÃO
    total_iteration = 0
    # III) MELHOR RESULTADO DAS 5 EXECUÇÕES
    result = 999999
    # IV) MÉDIA DOS RESULTADOS DAS 5 EXECUÇÕES
    avarage_result = 0
    # V) TEMPO COMPUTACIONAL DA EXECUÇÃO QUE GEROU O MELHOR RESULTADO
    time_best_result = time.time()
    # VI) TEMPO COMPUTACIONAL MÉDIO DAS 5 EXECUÇÕES
    avarage_time_iteration = 0
    # TODO !VII) DESVIO DO RESULTADO OBTIDO EM RELAÇÃO AO ÓTIMO PARA CADA INSTÂNCIA
    desvio_custo = cvrp_sol.cost
    
    # Auxiliares
    cont_iter = 0
    inicio = total_time
    # print("Melhor custo: " ,calc_cost_func(alnsIter.best_state, cvrp_test))
    # alnsIter.do_alns_iteraction(50, cvrp_state, cvrp_test )
    # print()
    for _ in range(5):
        alnsIter = ALNSIter(destroy_heuristics, constructor_heuristics, 
                        scoring_function, acceptance_function, 
                        alnsProb )
        cvrp_state = Cvrp_state(cvrp_test)
        alnsIter.do_alns_iteraction(intensity, cvrp_state, cvrp_test )
        best_result = calc_cost_func(alnsIter.best_state, cvrp_test)
        reduce_value = best_result*percent
        goal_value = best_result - reduce_value
        initial_cost = best_result

        internal_iteration = time.time()

        # print("Òtimo custo: ", int(opt_cost))

        while(1):
            cont_iter += 1
            # print("intensity: ", intensity)

            alnsIter.do_alns_iteraction( percent, None, cvrp_test )
            current_best_result = calc_cost_func(alnsIter.best_state, cvrp_test)
            # print(calc_cost_func(alnsIter.best_state, cvrp_test))
            # print("best state: ",alnsIter.best_state.sol_path)
            print("Best cost: ", calc_cost_func(alnsIter.best_state, cvrp_test))
            # print("current state: ",alnsIter.current_state.sol_path,  " cost: ", calc_cost_func(alnsIter.current_state, cvrp_test))
            print("Current cost: ", calc_cost_func(alnsIter.current_state, cvrp_test))
            print("Goal cost: ", goal_value)
            print("inital cost: ", initial_cost)
            # print()
            # print(current_result)
            if current_best_result < best_result:
                best_result = current_best_result

                if current_best_result <= goal_value:
                    exit(1)
                    break
            
            # deveria ser 300 segundo o enunciado
            fim = time.time()
            # print(fim - inicio)
            # print("\n\n")
            if fim - inicio > str_time_limit:
                break
        # print("Best result: ", best_result)
        
        internal_iteration = time.time() - internal_iteration

        if best_result < result:
            # Total de iterações para alcançar o melhor resultado
            total_iteration = cont_iter
            # Guarda o melhor resultado obtido até então
            result = best_result
            time_best_result = time.time() - inicio
        
        # Média dos resultados obtidos
        avarage_result += best_result/5
        avarage_time_iteration += internal_iteration/5



    # Critérios a serem registrados:
    total_time = time.time() - total_time
    # print("I)   TEMPO <= 300 PARA O ALGORITMO GERAR A MELHOR SOLUÇÃO ", round(total_time, 2))
    # print("II)  NÚMERO DE ITERAÇÕES PARA O ALGORITMO GERAR A MELHOR SOLUÇÃO ", total_iteration)
    # print("III) MELHOR RESULTADO DAS 5 EXECUÇÕES ", result)
    # print("IV)  MÉDIA DOS RESULTADOS DAS 5 EXECUÇÕES ", round(avarage_result,2))
    # print("V)   TEMPO COMPUTACIONAL DA EXECUÇÃO QUE GEROU O MELHOR RESULTADO",  round(time_best_result,2))
    # print("VI)  TEMPO COMPUTACIONAL MÉDIO DAS 5 EXECUÇÕES ", round(avarage_time_iteration,2))
    
    
    # print(cost, " ", result, " ", result - int(cost))
    print(instance_file.split('/')[-1], ';', intensity  , ';' , str_time_limit , ';', percent*100 , ";" , # PARAMETROS
        round(total_time, 4),';' ,  total_iteration,';' , 
        result, ';' , round(avarage_result,4),';' , 
        round(time_best_result,4),';' , 
        round(avarage_time_iteration,4), ';', 
        result - int(opt_cost) )
    # print("test ", alnsIter.current_state.sol_path)



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
        print("Usage: python cvrp.py input_file [intensity] [str_time_limit] [percent]")
        sys.exit(1)

    instance_file = sys.argv[1]
    intensity = int(sys.argv[2]) if len(sys.argv) > 2 else int("50")
    str_time_limit = int(sys.argv[3]) if len(sys.argv) > 3 else int("20")
    percent = int(sys.argv[4]) if len(sys.argv) > 4 else int("10")

    if(intensity > 100 or intensity < 0):
        print("Intensidade é uma porcentagem, não pode ser maior que 100% nem menor que 0%.")
        print("Usage: python cvrp.py input_file [intensity] [str_time_limit] [percent]")
        sys.exit(1)

    if(str_time_limit > 300 or str_time_limit < 0):
        print("str_time_limit deve ser um valor positivo e menor que 300 segundos (tempo limite)")
        print("Usage: python cvrp.py input_file [intensity] [str_time_limit] [percent]")
        sys.exit(1)
    
    if(percent > 100 or percent < 0):
        print("Porcentagem é uma porcentagem, não pode ser maior que 100% nem menor que 0%.")
        print("Usage: python cvrp.py input_file [intensity] [str_time_limit] [percent]")
        sys.exit(1)

    intensity = intensity/100
    percent = percent/100


    # print("intensity: ", intensity)
    # print("str_time_limit: ", str_time_limit)
    # print("percent: ", percent)

    

    main(instance_file)
