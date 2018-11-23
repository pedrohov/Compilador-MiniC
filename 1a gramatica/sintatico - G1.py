# Compiladores I     -    2o semestre/2018
# Pedro Henrique Oliveira Veloso - 0002346
# Thales Henrique Damasceno Lima - 0002859

from lexico import *;

class Sintatico():
    def __init__(self, arquivo):
        self.lexico = Lexico();
        self.lexico.abre(arquivo);
        self.tabSimb = {};

    def fecha(self):
        self.lexico.fecha();

    def parse(self):
        self.lexico.getToken();
        
        self.exp();
        self.consome(Atual.token);

    def consome(self, token):
        if(Atual.token == token):
            self.lexico.getToken();
        else:
            print("ERRO (lin " + str(Atual.linha) + ", col " + str(Atual.coluna) + ") : Era esperado o token " + Token.msg[token] + ", mas veio " + Token.msg[Atual.token]);

    def exp(self):
        #print("Exp");
        self.soma();

    def soma(self):
        #print("Soma");
        self.mult();
        self.restoSoma();

    def mult(self):
        #print("Mult");
        self.uno();
        self.restoMult();

    def uno(self):
        #print("Uno");
        if(Atual.token == Token.SOMA):
            self.consome(Token.SOMA);
            self.uno();
        elif(Atual.token == Token.SUB):
            self.consome(Token.SUB);
            self.uno();
        else:
            self.fator();

    def fator(self):
        res = None;

        #print("Fator");
        if(Atual.token == Token.NUM):
            #res = int(Atual.lexema);
            self.consome(Token.NUM);
        elif(Atual.token == Token.IDENT):
            #res = self.tabSimb[Atual.lexema];
            self.consome(Token.IDENT);
        elif(Atual.token == Token.ABREPAR):
            self.consome(Token.ABREPAR);
            res = self.soma();
            self.consome(Token.FECHAPAR);
        else:
            self.consome(Token.ABREPAR);

        return res;

    def restoSoma(self):
        #print("Resto Soma");
        if(Atual.token == Token.SOMA):
            self.consome(Token.SOMA);
            self.mult();
            self.restoSoma();
        elif(Atual.token == Token.SUB):
            self.consome(Token.SUB);
            self.mult();
            self.restoSoma();
        else:
            return;

    def restoMult(self):
        #print("Resto Mult");
        if(Atual.token == Token.MULT):
            self.consome(Token.MULT);
            self.uno();
            self.restoMult();
        elif(Atual.token == Token.DIV):
            self.consome(Token.DIV);
            self.uno();
            self.restoMult();
        else:
            return;

if __name__ == "__main__":
    sint = Sintatico("tst.txt");
    sint.parse();
    sint.fecha();