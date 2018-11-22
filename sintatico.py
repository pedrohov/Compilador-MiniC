# Compiladores I     -    2o semestre/2018
# Pedro Henrique Oliveira Veloso - 0002346
# Thales Henrique Damasceno Lima - 0002859

from lexico import *;
from erros  import *;
import sys;

# Esconde o traceback das excecoes.
# Comentar para debug.
sys.tracebacklimit = 0;

class Sintatico():
    def __init__(self, arquivo):
        self.lexico  = Lexico();
        self.first   = self.initFirst();
        self.tabSimb = {};
        self.lexico.abre(arquivo);

        # Temporarios:
        self.tempSeed   = 0;
        self.tempLivres = [];

        # Labels:
        self.labelSeed   = 0;
        self.labelLivres = [];

    def fecha(self):
        self.lexico.fecha();

    def parse(self):
        self.lexico.getToken();
        self.function();
        self.consume(Atual.token);

    def consume(self, token):
        if(Atual.token == token):
            self.lexico.getToken();
        else:
            raise ErroSintatico(token);

    def geraTemp(self):
        if(len(self.tempLivres) > 0):
            return self.tempLivres.pop();
        
        self.tempSeed += 1;
        return "_temp" + str(self.tempSeed);

    def liberaTemp(self, temp):
        if(temp not in self.tempLivres):
            self.tempLivres.append(temp);

    def geraLabel(self):
        if(len(self.labelLivres) > 0):
            return self.labelLivres.pop();
        
        self.labelSeed += 1;
        return "_label" + str(self.labelSeed);

    def liberaLabel(self, label):
        if(label not in self.labelLivres):
            self.labelLivres.append(label);

    def function(self):
        self.type();
        self.consume(Token.IDENT);
        self.consume(Token.ABREPAR);
        self.argList();
        self.consume(Token.FECHAPAR);
        self.bloco();

    def type(self):
        if(Atual.token == Token.FLOAT):
            self.consume(Token.FLOAT);
            return 'float';
        else:
            self.consume(Token.INT);
            return 'int';

    def bloco(self):
        self.consume(Token.ABRECHA);
        codigo = self.stmtList();
        print(codigo);
        self.consume(Token.FECHACHA);
        return codigo;

    def argList(self):
        if(Atual.token in self.first["argList"]):
            self.arg();
            self.restoArgList();
        else:
            pass;

    def restoArgList(self):
        if(Atual.token == Token.VIRG):
            self.consume(Token.VIRG);
            self.argList();
        else:
            pass;

    def arg(self):
        self.type();
        self.consume(Token.IDENT);

    def stmtList(self):
        if(Atual.token in self.first["stmtList"]):
            codigoStmt = self.stmt(None, None);
            codigoList = self.stmtList();
            return codigoStmt + codigoList;
        else:
            return [];

    def stmt(self, inicio, fim):
        if(Atual.token in self.first["forStmt"]):
            return self.forStmt();
        elif(Atual.token in self.first["whileStmt"]):
            return self.whileStmt();
        elif(Atual.token in self.first["expr"]):
            (codigo, res) = self.expr();
            self.consume(Token.PTOVIRG);
            return codigo;
        elif(Atual.token in self.first["ifStmt"]):
            return self.ifStmt();
        elif(Atual.token in self.first["bloco"]):
            return self.bloco();
        elif(Atual.token == Token.BREAK):
            self.consume(Token.BREAK);
            self.consume(Token.PTOVIRG);
            return [];
        elif(Atual.token == Token.CONTINUE):
            self.consume(Token.CONTINUE);
            self.consume(Token.PTOVIRG);
            return [];
        elif(Atual.token in self.first["declaration"]):
            self.declaration();
            return [];
        elif(Atual.token in self.first["ioStmt"]):
            return self.ioStmt();
        else:
            self.consume(Token.PTOVIRG);
            return [];

    def forStmt(self):
        self.consume(Token.FOR);
        self.consume(Token.ABREPAR);

        (atrib, resA) = self.optExpr();

        self.consume(Token.PTOVIRG);

        (compa, resC) = self.optExpr();

        self.consume(Token.PTOVIRG);

        (incre, resI) = self.optExpr();

        self.consume(Token.FECHAPAR);

        inicio = self.geraLabel();
        fim    = self.geraLabel();

        listaCom = self.stmt(inicio, fim);
        codigo   = [];
        codigo.append(('label', inicio, None, None));
        codigo = codigo + atrib;
        codigo = codigo + compa;
        codigo.append(('if', resC, fim, None));
        codigo = codigo + listaCom + incre;
        codigo.append(('jump', inicio, None, None));
        codigo.append(('label', fim, None, None));

        return codigo;

    def ioStmt(self):
        if(Atual.token == Token.SCAN):
            self.consume(Token.SCAN);
            self.consume(Token.ABREPAR);
            self.consume(Token.STR);
            self.consume(Token.VIRG);
            self.consume(Token.IDENT);
            self.confume(Token.FECHAPAR);
            self.consume(Token.PTOVIRG);
        else:
            self.consume(Token.PRINT);
            self.consume(Token.ABREPAR);
            codigo = self.outList();
            self.consume(Token.FECHAPAR);
            self.consume(Token.PTOVIRG);
            return codigo;

    def whileStmt(self):
        self.consume(Token.WHILE);
        self.consume(Token.ABREPAR);

        (expr, res) = self.expr();
        
        self.consume(Token.FECHAPAR);

        inicio = self.geraLabel();
        fim    = self.geraLabel();

        listaCom = self.stmt(inicio, fim);
        codigo   = [];
        codigo.append(('label', inicio, None, None));
        codigo   = codigo + expr;
        codigo.append(('if', res, fim, None));
        codigo   = codigo + listaCom;
        codigo.append(('jump', inicio, None, None));
        codigo.append(('label', fim, None, None));

        return codigo;

    def ifStmt(self):
        self.consume(Token.IF);
        self.consume(Token.ABREPAR);

        (expr, res) = self.expr();

        self.consume(Token.FECHAPAR);

        inicio = self.geraLabel();
        fim    = self.geraLabel();

        listaCom = self.stmt(inicio, fim);
        listaComElse = self.elsePart();

        codigo = [];
        codigo.append(('label', inicio, None, None));
        codigo = codigo + expr;
        codigo.append(('if', res, fim, None));
        codigo = codigo + listaCom;
        codigo.append(('label', fim, None, None));
        codigo = codigo + listaComElse;

        return codigo;

    def elsePart(self):
        if(Atual.token == Token.ELSE):
            self.consume(Token.ELSE);
            return self.stmt(None, None);
        else:
            return [];

    def declaration(self):
        temp1 = self.type();
        temp2 = self.identList();

        # Para cada id na lista declarada:
        for id in temp2:
            # Se a id ja existir:
            if(id in self.tabSimb):
                raise ErroSemantico("Varivel ja declarada.");
            # Senao adiciona a tabela de simbolos:
            else:
                # Determina se o valor eh inteiro ou real:
                valor = None;
                if(temp1 == 'int'):
                    valor = int(0);
                else:
                    valor = float(0);

                # Adiciona novo simbolo:
                self.tabSimb[id] = (temp1, valor); # (tipo, valor)

        self.consume(Token.PTOVIRG);

    def identList(self):
        res = [Atual.lexema];
        self.consume(Token.IDENT);
        self.restoIdentList(res);
        return res;

    def restoIdentList(self, idList):
        if(Atual.token == Token.VIRG):
            self.consume(Token.VIRG);
            idList.append(Atual.lexema);
            self.consume(Token.IDENT);
            self.restoIdentList(idList);
        else:
            pass;

    def optExpr(self):
        if(Atual.token in self.first["expr"]):
            return self.expr();
        else:
            return ([], None); # Vazio.

    def outList(self):
        listaO = self.out();
        listaR = self.restoOutList();

        return listaO + listaR;

    def restoOutList(self):
        if(Atual.token == Token.VIRG):
            self.consume(Token.VIRG);
            listaO = self.out();
            listaR = self.restoOutList();
            return listaO + listaR;
        else:
            return []; # Vazio.

    def out(self):
        # Real:
        if(Atual.token == Token.NUMfloat):
            quad = ('print', Atual.lexema, None, None);
            self.consume(Token.NUMfloat);
            return [quad];
        # String:
        elif(Atual.token == Token.STR):
            quad = ('print', Atual.lexema, None, None);
            self.consume(Token.STR);
            return [quad];
        # Identificador:
        elif(Atual.token == Token.IDENT):

            # Variavel nao declarada:
            if(Atual.lexema not in self.tabSimb):
                raise ErroSemantico("Varivel " + Atual.lexema + " nao foi declarada.");

            quad = ('print', Atual.lexema, None, None);
            self.consume(Token.IDENT);
            return [quad];
        # Inteiro:
        else:
            quad = ('print', Atual.lexema, None, None);
            self.consume(Token.NUMint);
            return [quad];

    def expr(self):
        (left, codigo, res) = self.atrib();
        return (codigo, res);

    def atrib(self):
        (leftO, listaO, resO) = self.Or();
        (leftA, listaA, resA) = self.restoAtrib(resO);

        if((not leftO) and (not leftA)):
            raise ErroSintatico(Atual.token, "Atribuicao invalida.");

        return (False, listaO + listaA, resO);

    def restoAtrib(self, valor):
        if(Atual.token == Token.IGUAL):
            self.consume(Token.IGUAL);
            (left, lista, res) = self.atrib();
            lista.append(('=', valor, res, None));
            return (False, lista, res);
        else:
        	return (True, [], None); # Vazio.

    def Or(self):
        (leftA, listaA, resA) = self.And();
        (leftO, listaO, resO) = self.restoOr(resA);

        if(leftA and leftO):
            return (True, listaA + listaO, resA);
        else:
            return (False, listaA + listaO, resA);

    def restoOr(self, valor):
        if(Atual.token == Token.OR):
            self.consume(Token.OR);
            (leftA, listaA, resA) = self.And();
            (leftO, listaO, resO) = self.restoOr(valor);
            quad = ('||', valor, valor, resA);
            listaA.append(quad);
            return (False, listaA + listaO, resA);
        else:
        	return (True, [], None);

    def And(self):
        (leftN, listaN, resN) = self.Not();
        (leftA, listaA, resA) = self.restoAnd(resN);

        if(leftN and leftA):
            return (True, listaN + listaA, resN);
        else:
            return (False, listaN + listaA, resN);

    def restoAnd(self, valor):
        if(Atual.token == Token.AND):
            self.consume(Token.AND);
            (leftN, listaN, resN) = self.Not();
            (leftA, listaA, resA) = self.restoAnd(valor);
            quad = ('&&', valor, valor, resN);
            listaN.append(quad);
            return (False, listaN + listaA, resN);
        else:
        	return (True, [], None); # Vazio.

    def Not(self):
        if(Atual.token == Token.NOT):
            self.consume(Token.NOT);
            (left, lista, res) = self.Not();
            quad = ('!', res, res, None);
            lista.append(quad);
            return (False, lista, res);
        else:
            return self.rel();

    def rel(self):
        (leftA, listaA, resA) = self.add();
        (leftR, listaR, resR) = self.restoRel(resA);

        if(leftA and leftR):
            return (True, listaA + listaR, resA);
        else:
            return (False, listaA + listaR, resA);

    def restoRel(self, valor):
        if(Atual.token == Token.CIGUAL):
            self.consume(Token.CIGUAL);
            (left, lista, res) = self.add();
            quad = ('==', valor, valor, res);
            lista.append(quad);
            return (False, lista, res);
        elif(Atual.token == Token.MAIOR):
            self.consume(Token.MAIOR);
            (left, lista, res) = self.add();
            quad = ('>', valor, valor, res);
            lista.append(quad);
            return (False, lista, res);
        elif(Atual.token == Token.MENOR):
            self.consume(Token.MENOR);
            (left, lista, res) = self.add();
            quad = ('<', valor, valor, res);
            lista.append(quad);
            return (False, lista, res);
        elif(Atual.token == Token.MAIORI):
            self.consume(Token.MAIORI);
            (left, lista, res) = self.add();
            quad = ('>=', valor, valor, res);
            lista.append(quad);
            return (False, lista, res);
        elif(Atual.token == Token.MENORI):
            self.consume(Token.MENORI);
            (left, lista, res) = self.add();
            quad = ('<=', valor, valor, res);
            lista.append(quad);
            return (False, lista, res);
        elif(Atual.token == Token.DIFFER):
            self.consume(Token.DIFFER);
            (left, lista, res) = self.add();
            quad = ('!=', valor, valor, res);
            lista.append(quad);
            return (False, lista, res);
        else:
        	return (True, [], None);

    def add(self):
        (leftM, listaM, resM) = self.mult();
        (leftA, listaA, resA) = self.restoAdd(resM);

        if(leftM and leftA):
            return (True , listaM + listaA, resM);
        else:
            return (False, listaM + listaA, resM);
        
    def restoAdd(self, valor):
        if(Atual.token == Token.SOMA):
            self.consume(Token.SOMA);
            (leftM, listaM, resM) = self.mult();
            (leftA, listaA, resA) = self.restoAdd(valor);
            quad = ('+', valor, valor, resM);
            listaM.append(quad);
            return (False, listaM + listaA, resM);
        elif(Atual.token == Token.SUB):
            self.consume(Token.SUB);
            (leftM, listaM, resM) = self.mult();
            (leftA, listaA, resA) = self.restoAdd(valor);
            quad = ('-', valor, valor, resM);
            listaM.append(quad);
            return (False, listaM + listaA, resM);
        else:
            return (True, [], None); # Vazio.

    def mult(self):
        (leftU, listaU, resU) = self.uno();
        (leftM, listaM, resM) = self.restoMult(resU);

        if(leftU and leftM):
            return (True, listaU + listaM, resU);
        else:
            return (False, listaU + listaM, resU);

    def restoMult(self, valor):
        if(Atual.token == Token.MULT):
            self.consume(Token.MULT);
            (leftU, listaU, resU) = self.uno();
            (leftM, listaM, resM) = self.restoMult(valor);
            quad = ('*', valor, valor, resU);
            listaU.append(quad);
            return (False, listaU + listaM, resU);
        elif(Atual.token == Token.DIV):
            self.consume(Token.DIV);
            (leftU, listaU, resU) = self.uno();
            (leftM, listaM, resM) = self.restoMult(valor);
            quad = ('/', valor, valor, resU);
            listaU.append(quad);
            return (False, listaU + listaM, resU);
        elif(Atual.token == Token.MOD):
            self.consume(Token.MOD);
            (leftU, listaU, resU) = self.uno();
            (leftM, listaM, resM) = self.restoMult(valor);
            quad = ('%', valor, valor, resU);
            lista = listaU.append(quad);
            return (False, listaU + listaM, resU);
        else:
            return (True, [], None); # Vazio.

    def uno(self):
        if(Atual.token == Token.SOMA):
            self.consume(Token.SOMA);
            (left, lista, res) = self.uno();
            temp = self.geraTemp();
            lista.append(('+', temp, 0, res));
            return (False, lista, temp);
        elif(Atual.token == Token.SUB):
            self.consume(Token.SUB);
            (left, lista, res) = self.uno();
            temp = self.geraTemp();
            lista.append(('-', temp, 0, res));
            return (False, lista, temp);
        else:
            return self.fator();

    def fator(self):
        if(Atual.token == Token.NUMfloat):
            temp = self.geraTemp();
            lexema = float(Atual.lexema);
            quad = ('=', temp, lexema, None);
            self.consume(Token.NUMfloat);
            return (False, [quad], temp);
        elif(Atual.token == Token.IDENT):

            # Variavel nao declarada:
            if(Atual.lexema not in self.tabSimb):
                raise ErroSemantico("Varivel " + Atual.lexema + " nao foi declarada.");

            temp = self.geraTemp();
            lexema = Atual.lexema;
            quad = ('=', temp, lexema, None);
            self.consume(Token.IDENT);
            return (True, [quad], temp);
        elif(Atual.token == Token.ABREPAR):
            self.consume(Token.ABREPAR);
            (left, lista, res) = self.atrib();
            self.consume(Token.FECHAPAR);
            return (False, lista, res);
        else:
            lexema = int(Atual.lexema);
            temp = self.geraTemp();
            quad = ('=', temp, lexema, None);
            self.consume(Token.NUMint);
            return (False, [quad], temp); # False: Nao pode aparecer do lado esquerdo.

    def initFirst(self):
        # -1 = LAMBDA.
        first = {
                "function": [Token.FLOAT, Token.INT],
                "argList": [Token.FLOAT, Token.INT, -1],
                "arg": [Token.FLOAT, Token.INT],
                "restoArgList": [-1],
                "type": [Token.FLOAT, Token.INT],
                "bloco": [Token.ABRECHA],
                "stmtList": [Token.NOT, Token.ABRECHA, Token.SOMA, Token.SUB,
                Token.PTOVIRG, Token.IDENT, Token.NUMfloat, Token.NUMint, Token.BREAK, Token.CONTINUE,
                Token.FLOAT, Token.FOR, Token.IF, Token.INT, Token.PRINT, Token.SCAN, Token.WHILE, Token.ABRECHA, -1],
                "stmt": [Token.NOT, Token.ABRECHA, Token.SOMA, Token.SUB,
                Token.PTOVIRG, Token.IDENT, Token.NUMfloat, Token.NUMint, Token.BREAK, Token.CONTINUE,
                Token.FLOAT, Token.FOR, Token.IF, Token.INT, Token.PRINT, Token.SCAN, Token.WHILE, Token.ABRECHA, -1],
                "declaration": [Token.FLOAT, Token.INT],
                "identList": [Token.IDENT],
                "restoIdentList": [-1],
                "forStmt": [Token.FOR],
                "optExpr": [Token.NOT, Token.SOMA, Token.SUB, Token.IDENT, Token.NUMfloat, Token.NUMint, -1],
                "ioStmt": [Token.PRINT, Token.SCAN],
                "outList": [Token.IDENT, Token.NUMfloat, Token.NUMint, Token.STR],
                "out": [Token.IDENT, Token.NUMfloat, Token.NUMint, Token.STR],
                "restoOutList": [-1],
                "whileStmt": [Token.WHILE],
                "ifStmt": [Token.IF],
                "elsePart": [Token.ELSE, -1],
                "expr": [Token.NOT, Token.ABREPAR, Token.SOMA, Token.SUB, Token.IDENT, Token.NUMfloat, Token.NUMint],
                "atrib": [Token.NOT, Token.ABREPAR, Token.SOMA, Token.SUB, Token.IDENT, Token.NUMfloat, Token.NUMint],
                "restoAtrib": [Token.IGUAL],
                "or": [Token.NOT, Token.ABREPAR, Token.SOMA, Token.SUB, Token.IDENT, Token.NUMfloat, Token.NUMint],
                "restoOr": [Token.OR, -1],
                "and": [Token.NOT, Token.ABREPAR, Token.SOMA, Token.SUB, Token.IDENT, Token.NUMfloat, Token.NUMint],
                "restoAnd": [Token.AND, -1],
                "not": [Token.NOT, Token.ABREPAR, Token.SOMA, Token.SUB, Token.IDENT, Token.NUMfloat, Token.NUMint],
                "rel": [Token.ABREPAR, Token.SOMA, Token.SUB, Token.IDENT, Token.NUMfloat, Token.NUMint],
                "restoRel": [Token.MAIOR, Token.MAIORI, Token.MENOR, Token.MENORI, Token.DIFFER, Token.CIGUAL, -1],
                "add": [Token.ABREPAR, Token.SOMA, Token.SUB, Token.IDENT, Token.NUMfloat, Token.NUMint],
                "restoAdd": [Token.SOMA, Token.SUB],
                "mult": [Token.NOT, Token.ABREPAR, Token.SOMA, Token.SUB, Token.IDENT, Token.NUMfloat, Token.NUMint],
                "restoMult": [Token.MOD, Token.MULT, Token.DIV, -1],
                "uno": [Token.ABREPAR, Token.SOMA, Token.SUB, Token.IDENT, Token.NUMfloat, Token.NUMint],
                "fator":  [Token.ABREPAR, Token.IDENT, Token.NUMfloat, Token.NUMint]
            };
        return first;


if __name__ == "__main__":

    if(len(sys.argv) < 2):
        print("Especifique o nome do arquivo.");
        exit();

    sint = Sintatico(sys.argv[1]);

    try:
        sint.parse();
        sint.consume(Token.EOF);
    except ErroSintatico:
        raise;

    #print(sint.tabSimb);
    sint.fecha();