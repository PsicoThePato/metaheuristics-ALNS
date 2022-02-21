# Modifique as variaveis conforme o seu setup.
EXEC=python3 main.py

# Eu uso ROOT como o diretório raiz para os meus labs.
YEAR=$(shell pwd | grep -o '20..-.')
# Aleks
# ROOT=/usr/local/lib
# ANTLR_PATH=$(ROOT)/antlr-4.9.2-complete.jar
# Lucas
ROOT=/home/lucas/desktop/ufes/compiladores
ANTLR_PATH=$(ROOT)/antlr-4.9.3-complete.jar

CLASS_PATH_OPTION=-cp .:$(ANTLR_PATH)

# Diretório para os arquivos .class
BIN_PATH=bin

# Comandos como descritos na página do ANTLR.
ANTLR4=$(JAVA) -jar $(ANTLR_PATH)
GRUN=$(JAVA) $(CLASS_PATH_OPTION):$(BIN_PATH) org.antlr.v4.gui.TestRig

# Diretório para aonde vão os arquivos gerados.
GEN_PATH=parser

# Diretório para os casos de teste
DATA=instances
IN1=$(DATA)/Augeratetal
IN2=$(DATA)/Fisher


runall:
	-for FILE in $(IN1)/*.vrp; do \
        echo "\nRunning $${FILE}" &&\
		$(EXEC) $${FILE} &&\
		echo;\
    done;

runallFalse:
	-for FILE in $(IN2)/*.c; do \
        echo "\nRunning $${FILE}" &&\
		$(JAVA) $(CLASS_PATH_OPTION):$(BIN_PATH) Main $${FILE} &&\
		echo;\
    done;

clean:
	@rm -rf $(GEN_PATH) $(BIN_PATH)