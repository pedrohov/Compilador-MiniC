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

        # Escopo de Bloco:
        self.blocoAtual = -1;

    def fecha(self):
        self.lexico.fecha();

    def parse(self):
        self.lexico.getToken();
        codigo = self.function();
        self.consume(Atual.token);
        self.consume(Token.EOF);
        codigo.append(('stop', None, None, None));
        return codigo;

    def consume(self, token):
        if(Atual.token == token):
            self.lexico.getToken();
        else:
            raise ErroSintatico(token);

    def geraTemp(self):
        if(len(self.tempLivres) > 0):
            return self.tempLivres.pop();
        
        self.tempSeed += 1;
        return "b_" + str(self.blocoAtual) + "_temp" + str(self.tempSeed);

    def liberaTemp(self, temp):
        if(temp not in self.tempLivres):
            self.tempLivres.append(temp);

    def geraLabel(self):
        if(len(self.labelLivres) > 0):
            return self.labelLivres.pop();
        
        self.labelSeed += 1;
        return "label_" + str(self.labelSeed);

    def liberaLabel(self, label):
        if(label not in self.labelLivres):
            self.labelLivres.append(label);

    def formatVarName(self, var):
        return "b_" + str(self.blocoAtual) + "_" + var;

    def existeVarEscopo(self, var):
        """ Busca pela variavel em todos os escopos com id menor ou igual ao atual. """
        index = var.find('_', 2);
        idBloco = int(var[2:index]);
        nomeVar = var[(index + 1):];

        for variavel, tipo in self.tabSimb.items():
            indexA = variavel.find('_', 2);
            idBlocoA = int(variavel[2:indexA]);
            nomeVarA = variavel[(indexA + 1):];

            if(idBlocoA <= idBloco) and (nomeVar == nomeVarA):
                return True;

        return False;

    def getVarEscopo(self, var):
        """ Busca pela variavel em todos os escopos com id menor ou igual ao atual. """
        index = var.find('_', 2);
        idBloco = int(var[2:index]);
        nomeVar = var[(index + 1):];

        # Procura primeiro por var:
        if var in self.tabSimb:
            return var;

        # Procura por variaveis com o mesmo nome em escopos diferentes:
        for variavel, tipo in self.tabSimb.items():
            indexA = variavel.find('_', 2);
            idBlocoA = int(variavel[2:indexA]);
            nomeVarA = variavel[(indexA + 1):];

            if(idBlocoA <= idBloco) and (nomeVar == nomeVarA):
                return variavel;

        return var;

    def liberaVarsBloco(self):
        """ Libera todas as variaveis e temps do bloco atual. """
        paraDeletar = [];

        for variavel, tipo in self.tabSimb.items():
            index = variavel.find('_', 2);
            idBloco = int(variavel[2:index]);
            nomeVar = variavel[(index + 1):];

            if(idBloco == self.blocoAtual):
                paraDeletar.append(variavel);

        for var in paraDeletar:
            del self.tabSimb[var];

    def function(self):
        self.type();
        self.consume(Token.IDENT);
        self.consume(Token.ABREPAR);
        listaA = self.argList();
        self.consume(Token.FECHAPAR);
        listaB = self.bloco(None, None);
        return listaA + listaB;

    def type(self):
        if(Atual.token == Token.FLOAT):
            self.consume(Token.FLOAT);
            return 'float';
        else:
            self.consume(Token.INT);
            return 'int';

    def bloco(self, inicio, fim):
        self.consume(Token.ABRECHA);
        self.blocoAtual += 1;
        codigo = self.stmtList(inicio, fim);
        self.liberaVarsBloco();
        self.blocoAtual -= 1;
        self.consume(Token.FECHACHA);
        return codigo;

    def argList(self):
        if(Atual.token in self.first["argList"]):
            listaA = self.arg();
            listaR = self.restoArgList();
            return listaA + listaR;
        else:
            return [];

    def restoArgList(self):
        if(Atual.token == Token.VIRG):
            self.consume(Token.VIRG);
            self.argList();
            return [];
        else:
            return [];

    def arg(self):
        self.type();
        self.consume(Token.IDENT);
        return [];

    def stmtList(self, inicio, fim):
        if(Atual.token in self.first["stmtList"]):
            codigoStmt = self.stmt(inicio, fim);
            codigoList = self.stmtList(inicio, fim);
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
            return self.ifStmt(inicio, fim);
        elif(Atual.token in self.first["bloco"]):
            return self.bloco(inicio, fim);
        elif(Atual.token == Token.BREAK):
            return self.Break(fim);
        elif(Atual.token == Token.CONTINUE):
            return self.Continue(inicio);
        elif(Atual.token == Token.RETURN):
            self.consume(Token.RETURN);
            (_, _, _) = self.fator();
            self.consume(Token.PTOVIRG);
            return [];
        elif(Atual.token in self.first["declaration"]):
            return self.declaration();
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
        labInc = self.geraLabel();
        fim    = self.geraLabel();

        listaCom = self.stmt(labInc, fim);
        codigo   = [];
        codigo = codigo + atrib;
        codigo.append(('label', inicio, None, None));
        codigo = codigo + compa;
        codigo.append(('if', resC, None, fim));
        codigo = codigo + listaCom;
        codigo.append(('label', labInc, None, None));
        codigo = codigo + incre;
        codigo.append(('jump', inicio, None, None));
        codigo.append(('label', fim, None, None));

        return codigo;

    def ioStmt(self):
        if(Atual.token == Token.SCAN):
            self.consume(Token.SCAN);
            self.consume(Token.ABREPAR);

            # String antes do scan:
            msg = Atual.lexema;

            self.consume(Token.STR);
            self.consume(Token.VIRG);

            local = self.formatVarName(Atual.lexema);
            local = self.getVarEscopo(local);

            self.consume(Token.IDENT);
            self.consume(Token.FECHAPAR);
            self.consume(Token.PTOVIRG);

            return [('scan', local, msg, None)];

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
        codigo = [];
        codigo.append(('label', inicio, None, None));
        codigo = codigo + expr;
        codigo.append(('if', res, None, fim));
        codigo = codigo + listaCom;
        codigo.append(('jump', inicio, None, None));
        codigo.append(('label', fim, None, None));

        return codigo;

    def ifStmt(self, inicio, fim):
        self.consume(Token.IF);
        self.consume(Token.ABREPAR);

        (expr, res) = self.expr();

        self.consume(Token.FECHAPAR);

        true  = self.geraLabel();
        false = self.geraLabel();

        listaCom = self.stmt(inicio, fim);
        listaComElse = self.elsePart(inicio, fim);

        codigo = [];
        codigo = codigo + expr;
        codigo.append(('if', res, None, false));
        codigo = codigo + listaCom;
        codigo.append(('jump', true, None, None));
        codigo.append(('label', false, None, None));
        codigo = codigo + listaComElse;
        codigo.append(('label', true, None, None));

        return codigo;

    def elsePart(self, inicio, fim):
        if(Atual.token == Token.ELSE):
            self.consume(Token.ELSE);
            return self.stmt(inicio, fim);
        else:
            return []; # Vazio.

    def Break(self, fim):
        if(fim is not None):
            self.consume(Token.BREAK);
            self.consume(Token.PTOVIRG);
            return [('jump', fim, None, None)];
        else:
            self.consume(Token.BREAK);
            self.consume(Token.PTOVIRG);
            return [];

    def Continue(self, inicio):
        if(inicio is not None):
            self.consume(Token.CONTINUE);
            self.consume(Token.PTOVIRG);
            return [('jump', inicio, None, None)];
        else:
            self.consume(Token.BREAK);
            self.consume(Token.PTOVIRG);
            return [];

    def declaration(self):
        tipo = self.type();
        listaVar = self.identList();
        lista = []; # Lista de declaracoes.

        # Para cada id na lista declarada:
        for id in listaVar:
            varNome = self.formatVarName(id);

            # Se a id ja existir:
            if(varNome in self.tabSimb):
                raise ErroSemantico("Varivel ja declarada.");
            # Senao adiciona a tabela de simbolos:
            else:
                # Define o tipo:
                valor = int(0);
                if(tipo == 'float'):
                    valor = float(0);

                # Cria novo comando para a maquina virtual:
                quad = ('=', varNome, valor, None);
                lista.append(quad);

                # Adiciona novo simbolo:
                self.tabSimb[varNome] = tipo;

        self.consume(Token.PTOVIRG);
        return lista;

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
            pass; # Vazio.

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
            lexema = Atual.lexema;
            self.consume(Token.NUMfloat);
            quad = ('print', None, float(lexema), None);
            return [quad];
        # String:
        elif(Atual.token == Token.STR):
            quad = ('print', None, Atual.lexema, None);
            self.consume(Token.STR);
            return [quad];
        # Identificador:
        elif(Atual.token == Token.IDENT):

            varName = self.formatVarName(Atual.lexema);

            # Variavel nao declarada:
            if(self.existeVarEscopo(varName) is False):
                raise ErroSemantico("Varivel " + Atual.lexema + " nao foi declarada.");
            else:
                varName = self.getVarEscopo(varName);

            quad = ('print', None, varName, None);
            self.consume(Token.IDENT);
            return [quad];
        # Inteiro:
        else:
            lexema = Atual.lexema;
            self.consume(Token.NUMint);
            quad = ('print', None, int(lexema), None);
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
            (_, lista, res) = self.atrib();
            lista.append(('=', valor, res, None));
            return (False, lista, res);
        else:
        	return (True, [], valor); # Vazio.

    def Or(self):
        (leftA, listaA, resA) = self.And();
        (leftO, listaO, resO) = self.restoOr(resA);

        if(leftA and leftO):
            return (True, listaA + listaO, resO);
        else:
            return (False, listaA + listaO, resO);

    def restoOr(self, valor):
        if(Atual.token == Token.OR):
            self.consume(Token.OR);
            (_, listaA, resA) = self.And();
            (_, listaO, _) = self.restoOr(valor);
            temp = self.geraTemp();
            quad = ('||', temp, valor, resA);
            listaA.append(quad);
            return (False, listaA + listaO, temp);
        else:
        	return (True, [], valor);

    def And(self):
        (leftN, listaN, resN) = self.Not();
        (leftA, listaA, resA) = self.restoAnd(resN);

        if(leftN and leftA):
            return (True, listaN + listaA, resA);
        else:
            return (False, listaN + listaA, resA);

    def restoAnd(self, valor):
        if(Atual.token == Token.AND):
            self.consume(Token.AND);
            (_, listaN, resN) = self.Not();
            (_, listaA, _) = self.restoAnd(valor);
            temp = self.geraTemp();
            quad = ('&&', temp, valor, resN);
            listaN.append(quad);
            return (False, listaN + listaA, temp);
        else:
        	return (True, [], valor); # Vazio.

    def Not(self):
        if(Atual.token == Token.NOT):
            self.consume(Token.NOT);
            (_, lista, res) = self.Not();
            temp = self.geraTemp();
            quad = ('!', temp, res, None);
            lista.append(quad);
            return (False, lista, temp);
        else:
            return self.rel();

    def rel(self):
        (leftA, listaA, resA) = self.add();
        (leftR, listaR, resR) = self.restoRel(resA);

        if(leftA and leftR):
            return (True, listaA + listaR, resR);
        else:
            return (False, listaA + listaR, resR);

    def restoRel(self, valor):
        if(Atual.token == Token.CIGUAL):
            self.consume(Token.CIGUAL);
            (_, lista, res) = self.add();
            temp = self.geraTemp();
            quad = ('==', temp, valor, res);
            lista.append(quad);
            return (False, lista, temp);
        elif(Atual.token == Token.MAIOR):
            self.consume(Token.MAIOR);
            (_, lista, res) = self.add();
            temp = self.geraTemp();
            quad = ('>', temp, valor, res);
            lista.append(quad);
            return (False, lista, temp);
        elif(Atual.token == Token.MENOR):
            self.consume(Token.MENOR);
            (_, lista, res) = self.add();
            temp = self.geraTemp();
            quad = ('<', temp, valor, res);
            lista.append(quad);
            return (False, lista, temp);
        elif(Atual.token == Token.MAIORI):
            self.consume(Token.MAIORI);
            (_, lista, res) = self.add();
            temp = self.geraTemp();
            quad = ('>=', temp, valor, res);
            lista.append(quad);
            return (False, lista, temp);
        elif(Atual.token == Token.MENORI):
            self.consume(Token.MENORI);
            (_, lista, res) = self.add();
            temp = self.geraTemp();
            quad = ('<=', temp, valor, res);
            lista.append(quad);
            return (False, lista, temp);
        elif(Atual.token == Token.DIFFER):
            self.consume(Token.DIFFER);
            (_, lista, res) = self.add();
            temp = self.geraTemp();
            quad = ('!=', temp, valor, res);
            lista.append(quad);
            return (False, lista, temp);
        else:
        	return (True, [], valor);

    def add(self):
        (leftM, listaM, resM) = self.mult();
        (leftA, listaA, resA) = self.restoAdd(resM);

        if(leftM and leftA):
            return (True , listaM + listaA, resA);
        else:
            return (False, listaM + listaA, resA);
        
    def restoAdd(self, valor):
        if(Atual.token == Token.SOMA):
            self.consume(Token.SOMA);
            (_, listaM, resM) = self.mult();
            (_, listaA, _) = self.restoAdd(valor);
            temp = self.geraTemp();
            quad = ('+', temp, valor, resM);
            listaM.append(quad);
            return (False, listaM + listaA, temp);
        elif(Atual.token == Token.SUB):
            self.consume(Token.SUB);
            (_, listaM, resM) = self.mult();
            (_, listaA, _) = self.restoAdd(valor);
            temp = self.geraTemp();
            quad = ('-', temp, valor, resM);
            listaM.append(quad);
            return (False, listaM + listaA, temp);
        else:
            return (True, [], valor); # Vazio.

    def mult(self):
        (leftU, listaU, resU) = self.uno();
        (leftM, listaM, resM) = self.restoMult(resU);

        if(leftU and leftM):
            return (True, listaU + listaM, resM);
        else:
            return (False, listaU + listaM, resM);

    def restoMult(self, valor):
        if(Atual.token == Token.MULT):
            self.consume(Token.MULT);
            (_, listaU, resU) = self.uno();
            (_, listaM, _) = self.restoMult(valor);
            temp = self.geraTemp();
            quad = ('*', temp, valor, resU);
            listaU.append(quad);
            return (False, listaU + listaM, temp);
        elif(Atual.token == Token.DIV):
            self.consume(Token.DIV);
            (_, listaU, resU) = self.uno();
            (_, listaM, _) = self.restoMult(valor);
            temp = self.geraTemp();
            quad = ('/', temp, valor, resU);
            listaU.append(quad);
            return (False, listaU + listaM, temp);
        elif(Atual.token == Token.MOD):
            self.consume(Token.MOD);
            (_, listaU, resU) = self.uno();
            (_, listaM, _) = self.restoMult(valor);
            temp = self.geraTemp();
            quad = ('%', temp, valor, resU);
            lista = listaU.append(quad);
            return (False, listaU + listaM, temp);
        else:
            return (True, [], valor); # Vazio.

    def uno(self):
        if(Atual.token == Token.SOMA):
            self.consume(Token.SOMA);
            (_, lista, res) = self.uno();
            temp = self.geraTemp();
            lista.append(('+', temp, 0, res));
            return (False, lista, temp);
        elif(Atual.token == Token.SUB):
            self.consume(Token.SUB);
            (_, lista, res) = self.uno();
            temp = self.geraTemp();
            lista.append(('-', temp, 0, res));
            return (False, lista, temp);
        else:
            return self.fator();

    def fator(self):
        if(Atual.token == Token.NUMfloat):
            temp = self.geraTemp();
            lexema = Atual.lexema;
            self.consume(Token.NUMfloat);
            quad = ('=', temp, float(lexema), None);
            return (False, [quad], temp);
        elif(Atual.token == Token.IDENT):

            varName = self.formatVarName(Atual.lexema);

            # Variavel nao declarada:
            if(self.existeVarEscopo(varName) is False):
                raise ErroSemantico("Varivel " + Atual.lexema + " nao foi declarada.");
            else:
                varName = self.getVarEscopo(varName);

            quad = ('=', varName, varName, None);
            self.consume(Token.IDENT);
            return (True, [], varName);
        elif(Atual.token == Token.ABREPAR):
            self.consume(Token.ABREPAR);
            (left, lista, res) = self.atrib();
            self.consume(Token.FECHAPAR);
            return (False, lista, res);
        else:
            temp = self.geraTemp();
            lexema = Atual.lexema;
            self.consume(Token.NUMint);
            quad = ('=', temp, int(lexema), None);
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
                Token.FLOAT, Token.FOR, Token.IF, Token.INT, Token.PRINT, Token.SCAN, Token.WHILE, Token.ABRECHA, Token.RETURN, -1],
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
        codigo = sint.parse();
        
        # Exibe o codigo:
        for cod in codigo:
        	print(cod);
    except ErroSintatico:
        raise;

    sint.fecha();