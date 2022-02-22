# Modifique as variaveis conforme o seu setup.
EXEC=python3 main.py

# Diretório para os casos de teste
DATA=instances
IN1=$(DATA)/Augeratetal
IN2=$(DATA)/Fisher

# Parametros
intensity = 30
str_time_limit = 300

runall:
	echo "Entrada;Intensidade ( (quantidade de cidades a ser removida na heuristica de destruição));\
	Tempo máximo;Percent(quanto que a resposta deve diminuir);Tempo de execução;\
	N° Iterações;Resultado Final;Média de resultado por iteração;Tempo para chegar no melhor resultado;\
	Tempo médio por iteração; Desvio em relação a solução ótima" >> test.csv 
	-for FILE in $(IN1)/*.vrp; do \
        echo "\nRunning $${FILE}" &&\
		$(EXEC) $${FILE} ${intensity} ${str_time_limit} &&\
		echo;\
    done;

clean:
	@rm -f test.csv