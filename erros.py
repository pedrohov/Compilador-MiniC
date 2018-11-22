# Compiladores I     -    2o semestre/2018
# Pedro Henrique Oliveira Veloso - 0002346
# Thales Henrique Damasceno Lima - 0002859

from lexico import *;

class ErroSintatico(Exception):
    def __init__(self, token, msg=None):
        self.token = token;
        self.msg = msg;

    def __str__(self):
        if(self.msg is None):
            return "(lin " + str(Atual.linha) + ", col " + str(Atual.coluna) + ") : Era esperado o token " + Token.msg[self.token] + ", mas veio " + Token.msg[Atual.token];
        else:
            return "(lin " + str(Atual.linha) + ", col " + str(Atual.coluna) + ") : " + self.msg;

class ErroSemantico(Exception):
    def __init__(self, msg=None):
        self.msg = msg;

    def __str__(self):
        if(self.msg is None):
            return "(lin " + str(Atual.linha) + ", col " + str(Atual.coluna) + ")";
        else:
            return "(lin " + str(Atual.linha) + ", col " + str(Atual.coluna) + ") : " + self.msg;