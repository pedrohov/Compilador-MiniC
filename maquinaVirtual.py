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
        self.labels  = {};
        self.vars    = {};

    def createLabels(self):
        """ Armazena o index das labels do codigo. """
        for i in range(len(self.codigo)):
            if(self.codigo[i][0] == 'label'):
                # key = label, valor = index do codigo:
                self.labels[self.codigo[i][1]] = i;

    def start(self):
        sintatico = Sintatico(self.arquivo);

        # Executa o analisador sintatico:
        try:
            self.codigo = sintatico.parse();
            self.createLabels();
            self.run();
        except Exception:
            raise;

    def run(self):
        # Define os metodos para cada operador:
        operadores = {
            "-" : self.sub,
            "+" : self.soma,
            "/" : self.divisao,
            "//": self.div,
            "%" : self.mod,
            "*" : self.mult,
            "=" : self.atrib,
            ">=": self.maiorI,
            "<=": self.menorI,
            "<" : self.menor,
            ">" : self.maior,
            "==": self.equals,
            "!=": self.diferenca,
            "&&": self.And,
            "||": self.Or,
            "!" : self.Not
        }
        # Define os metodos para syscalls:
        calls = {
            "scan": self.scan,
            "print": self.print
        }
        # Define os metodos para saltos:
        saltos = {
            "if": self.If,
            "jump": self.jump
        }

        PC = 0;
        while self.codigo[PC][0] != 'stop':
            # Salta labels:
            if(self.codigo[PC][0] == 'label'):
                PC += 1;
                continue;
            # Executa saltos:
            elif self.codigo[PC][0] in saltos:
                funcao = saltos[self.codigo[PC][0]];
                expr = self.codigo[PC][1];
                if(expr in self.vars):
                    expr = self.vars[expr];

                novoPC = funcao(expr, self.codigo[PC][2], self.codigo[PC][3]);
                if(novoPC is not None):
                    PC = novoPC;

            # Executa operacoes:
            elif self.codigo[PC][0] in operadores:

                op1 = self.codigo[PC][2];
                op2 = self.codigo[PC][3];
                funcao = operadores[self.codigo[PC][0]];

                # Determina se valor dos operadores esta em uma variavel
                # e define o valor real de cada um:
                if(op1 in self.vars):
                    op1 = self.vars[op1];

                if(op2 in self.vars):
                    op2 = self.vars[op2];

                # Executa a operacao e trata os tipos do resultado:
                result = funcao(op1, op2);

                if(self.codigo[PC][1] in self.vars):
                    if(type(self.vars[self.codigo[PC][1]]) is int):
                        result = int(result);

                self.vars[self.codigo[PC][1]] = result;
                
            # Executa chamadas:
            elif self.codigo[PC][0] in calls:
                funcao = calls[self.codigo[PC][0]];

                op1 = self.codigo[PC][2];
                if(op1 in self.vars):
                    op1 = self.vars[op1];

                op2 = self.codigo[PC][3];
                if(op2 in self.vars):
                    op2 = self.vars[op1];

                # Chamada com retorno:
                if(self.codigo[PC][1] is not None):
                    if(type(self.vars[self.codigo[PC][1]]) is float):
                        self.vars[self.codigo[PC][1]] = float(funcao(op1, op2));
                    else:
                        self.vars[self.codigo[PC][1]] = int(funcao(op1, op2));
                # Metodo (print):
                else:
                    funcao(op1, op2);

            PC += 1;

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
        return x;

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
            return float(input(x));
        else:
            return float(input("''"));

    def print(self, x, y):
        if x is not None:
            print(str(x), end='');
        if y is not None:
            print(str(y), end='');

    def If(self, exp, lab1, lab2):
        if(exp == 0):
            return self.labels[lab2];

    def jump(self, indice, lab1, lab2):
        return self.labels[indice];

if __name__ == '__main__':
    if(len(sys.argv) < 2):
        print("Especifique o nome do arquivo.");
        exit();

    vMachine = MaquinaVirtual(sys.argv[1]);

    try:
        vMachine.start();
    except Exception:
        raise;