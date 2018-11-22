# Compiladores I     -    2o semestre/2018
# Pedro Henrique Oliveira Veloso - 0002346
# Thales Henrique Damasceno Lima - 0002859

from sintatico import *;
import sys;

# Esconde o traceback das excecoes.
# Comentar para debug.
sys.tracebacklimit = 0;

class Semantico():
    def __init__(self):
        pass;

    def novoLabel(self):
        pass;

    def novoTemp(self):
        pass;

    def liberaTemp(self, temp):
        pass;

    # Tupla geraTupla(a, b, c, d)

if __name__ == "__main__":

    if(len(sys.argv) < 2):
        print("Especifique o nome do arquivo.");
        exit();

    