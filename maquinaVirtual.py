# Compiladores I     -    2o semestre/2018
# Pedro Henrique Oliveira Veloso - 0002346
# Thales Henrique Damasceno Lima - 0002859

from sintatico import *;
import sys;

# Esconde o traceback das excecoes.
# Comentar para debug.
sys.tracebacklimit = 0;


class MaquinaVirtual(object):
    
    def __init__(self, arquivo):
        self.arquivo = arquivo;
        self.codigo  = [];
        self.label   = {};
        self.var     = {};

    def createLabels(self):
        pass;

    def start(self):
        sintatico = Sintatico(self.arquivo);

        # Executa o analisador sintatico:
        try:
            self.codigo = sintatico.parse();
            sintatico.consume(Token.EOF);
        except ErroSintatico:
            raise;

        print(self.codigo);

    def run(self):
    	pass;

    def soma(self, x, y):
        return x + y;

    def sub(self, x, y):
        return x - y;

    def divisao(self, x, y):
        return x / y;

    def mult(self, x, y):
        return x * y;

    def mod(self, x, y):
        return x % y;

    def div(self, x, y):
        return x // y;

    def atrib(self, x, y):
        return y;

    def maiorI(self, x, y):
        return x >= y;

    def menorI(self, x, y):
        return x <= y;

    def diferenca(self, x, y):
        return x != y;

    def maior(self, x, y):
        return x > y;

    def menor(self, x, y):
        return x < y;

    def igualdade(self, x, y):
        return x == y;

    def And(self, x, y):
        return x and y;

    def Or(self, x, y):
        return x or y;

    def Not(self, x, y):
        return not y;

    def equals(self, x, y):
        return x == y;

    def scan(self, x, y):
        if x is not None:
            print(x)
        return float(input(""));

    def print(self, x, y):
        if x is not None:
            print(str(x));
        if y is not None:
            print(self.tabSimbolos[y]);

    def If(self, exp, lab1, lab2):
        print(exp)
        if(exp):
            return self.labels[lab1];
        else:
            return self.labels[lab2];

    def jump(self, indice, lab1, lab2):
        return self.labels[indice]

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Especifique o nome do arquivo.");
        exit();

    vMachine = MaquinaVirtual(sys.argv[1]);

    try:
        vMachine.start();
    except Exception:
        raise;