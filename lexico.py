# Compiladores I     -    2o semestre/2018
# Pedro Henrique Oliveira Veloso - 0002346
# Thales Henrique Damasceno Lima - 0002859

import sys;

class Token:
    ABREPAR  = 0;
    FECHAPAR = 1;
    VIRG     = 2;
    PTOVIRG  = 3;
    NUMint   = 4;
    NUMfloat = 5;
    IDENT    = 6;
    STR      = 7;
    SOMA     = 8;
    MULT     = 9;
    DIV      = 10;
    SUB      = 11;
    MOD      = 12;
    POT      = 13;
    SCAN     = 14;
    PRINT    = 15;
    EOF      = 16;
    ERRO     = 17;
    IGUAL    = 18;
    FOR      = 19;
    WHILE    = 20;
    IF       = 21;
    ELSE     = 22;
    AND      = 23; # &&
    OR       = 24; # ||
    NOT      = 25; # !
    BREAK    = 26; 
    CONTINUE = 27;
    INT      = 28;
    FLOAT    = 29;
    MAIOR    = 30; # >
    MENOR    = 31; # <
    MAIORI   = 32; # >=
    MENORI   = 33; # <=
    CIGUAL   = 34; # ==
    DIFFER   = 35; # !=
    ABRECHA  = 36; # {
    FECHACHA = 37; # }
    RETURN   = 38;

    msg = ['('       , ')'     , ','       , ';'     , 'NUMint',
           'NUMfloat', 'IDENT' , 'STR'     , '+'     , '*'     ,
           '/'       , '-'     , '%'       , '**'    , 'SCAN'  ,
           'PRINT'   , 'EOF'   , 'ERRO'    , '='     , 'FOR'   , 
           'WHILE'   , 'IF'    , 'ELSE'    , 'AND'   , 'OR'    ,
           'NOT'     , 'BREAK' , 'CONTINUE', 'INT'   , 'FLOAT' ,
           '>'       , '<'     , '>='      , '<='    , '=='    ,
           '!='      , '{'     , '}'       , 'RETURN'];

class Atual:
    linha  = 1;
    coluna = 1;
    token  = None;
    lexema = "";

    @classmethod
    def imprime(cls):
        print("Token: " + Token.msg[cls.token] + "\tLexema: " + cls.lexema +
              "\tLinha: " + str(cls.linha) + "\tColuna: " + str(cls.coluna));

class Lexico:
    def __init__(self):
        self.nome    = None;
        self.arquivo = None;
        self.linha   = None;
        self.codigo  = "";
        self.cursor  = -1;
        self.blkCom  = False; # Detecta comentarios em bloco.

    def abre(self, local):
        self.arquivo = open(local, 'r');
        self.codigo  = self.arquivo.read();
        self.nome    = local;

    def fecha(self):
        self.arquivo.close();

    def getchar(self):
        self.cursor = self.cursor + 1;
        if(self.cursor >= len(self.codigo)):
            return 'EOF';
        Atual.coluna = Atual.coluna + 1;
        return self.codigo[self.cursor];

    def removeChar(self):
        self.cursor = self.cursor - 1;
        Atual.coluna = Atual.coluna - 1;
        Atual.lexema = Atual.lexema[:-1];

    def atualizaToken(self, tok):
        Atual.token = tok;
        self.removeChar();

        # Lista de palavras reservadas:
        if(Atual.lexema == "print"):
            Atual.token = Token.PRINT;
        elif(Atual.lexema == "scan"):
            Atual.token = Token.SCAN;
        elif(Atual.lexema == "for"):
            Atual.token = Token.FOR;
        elif(Atual.lexema == "while"):
            Atual.token = Token.WHILE;
        elif(Atual.lexema == "if"):
            Atual.token = Token.IF;
        elif(Atual.lexema == "else"):
            Atual.token = Token.ELSE;
        elif(Atual.lexema == "break"):
            Atual.token = Token.BREAK;
        elif(Atual.lexema == "continue"):
            Atual.token = Token.CONTINUE;
        elif(Atual.lexema == "return"):
        	Atual.token = Token.RETURN;
        elif(Atual.lexema == "int"):
            Atual.token = Token.INT;
        elif(Atual.lexema == "float"):
            Atual.token = Token.FLOAT;

        return;

    def getToken(self):
        
        estado = 1;
        Atual.lexema = "";

        while(True):
            char = self.getchar();

            # Adiciona ao lexema se nao for EOF:
            if(char != 'EOF'):
                Atual.lexema = Atual.lexema + char;
            else:
                Atual.lexema = Atual.lexema + ' ';

            # Conta uma nova linha:
            if(char == "\n"):
                Atual.lexema = Atual.lexema[:-1];
                Atual.linha = Atual.linha + 1;
                Atual.coluna = 1;

            # Automato:
            elif(estado == 1):
                if(char in [' ', '\t']):
                    Atual.lexema = Atual.lexema[:-1];
                    continue;
                elif(char == 'EOF'):
                    self.atualizaToken(Token.EOF);
                    return;
                elif(char == '%'):
                    estado = 9;
                elif(char == '/'):
                    estado = 10;
                elif(char == '-'):
                    estado = 11;
                elif(char == '+'):
                    estado = 12;
                elif(char == '='):
                    estado = 13;
                elif(char == ','):
                    estado = 14;
                elif(char == ';'):
                    estado = 15;
                elif(char == '('):
                    estado = 16;
                elif(char == ')'):
                    estado = 17;
                elif(char == '*'):
                    estado = 18;
                elif(char == '"'):
                    estado = 21;
                elif(char.isalpha()):
                    estado = 2;
                elif(char.isdigit()):
                    estado = 4;
                elif(char == '&'):
                    estado = 24;
                elif(char == '|'):
                    estado = 26;
                elif(char == '!'):
                    estado = 28;
                elif(char == '>'):
                    estado = 31;
                elif(char == '<'):
                    estado = 33;
                elif(char == '{'):
                    estado = 35;
                elif(char == '}'):
                    estado = 36;
                else:
                    estado = 8;
            # Identificador:
            elif(estado == 2):
                if(char.isalnum() and (char != "EOF")):
                    estado = 2;
                else:
                    self.removeChar();
                    estado = 3;
            elif(estado == 3):   
                self.atualizaToken(Token.IDENT);
                return;
            # Numeros:
            elif(estado == 4):
                if(char.isdigit()):
                    estado = 4;
                elif(char == '.'):
                    estado = 6;
                elif(char.isalpha() and char != "EOF"):
                    estado = 2;
                else:
                    self.removeChar();
                    estado = 5;
            elif(estado == 5):
                self.atualizaToken(Token.NUMint);
                return;
            elif(estado == 6):
                if(char.isdigit()):
                    estado = 7;
                else:
                    self.removeChar();
                    estado = 8;
            elif(estado == 7):
                if(char.isdigit()):
                    estado = 7;
                else:
                    self.removeChar();
                    estado = 23;
            elif(estado == 8):
                self.removeChar();
                self.atualizaToken(Token.ERRO);
                return;
            elif(estado == 9):
                self.atualizaToken(Token.MOD);
                return;
            elif(estado == 10):
                if(char == "/"):
                    estado = 37; # Comentario em linha.
                elif(char == "*"):
                    estado = 38; # Comentario em bloco.
                else:
                    self.atualizaToken(Token.DIV);
                    return;
            elif(estado == 11):
                self.atualizaToken(Token.SUB);
                return;
            elif(estado == 12):
                self.atualizaToken(Token.SOMA);
                return;
            elif(estado == 13):
                if(char == '='):
                    estado = 30;
                else:
                    self.atualizaToken(Token.IGUAL);
                    return;
            elif(estado == 14):
                self.atualizaToken(Token.VIRG);
                return;
            elif(estado == 15):
                self.atualizaToken(Token.PTOVIRG);
                return;
            elif(estado == 16):
                self.atualizaToken(Token.ABREPAR);
                return;
            elif(estado == 17):
                self.atualizaToken(Token.FECHAPAR);
                return;
            elif(estado == 18):
                if(char == '*'):
                    estado = 20;
                else:
                    self.removeChar();
                    estado = 19;
            elif(estado == 19):
                self.atualizaToken(Token.MULT);
                return;
            elif(estado == 20):
                self.atualizaToken(Token.POT);
                return;
            # String:
            elif(estado == 21):
                if(char == "\\"):
                    estado = 39;
                elif(char == '"'):
                    estado = 22;
                else:
                    estado = 21;
            elif(estado == 22):
                # Remove aspas:
                Atual.lexema = Atual.lexema[1:-1];
                self.atualizaToken(Token.STR);
                return;
            # Float:
            elif(estado == 23):
                self.atualizaToken(Token.NUMfloat);
                return;
            # AND, OR, NOT:
            elif(estado == 24):
                if(char == '&'):
                    estado = 25;
                else:
                    estado = 8;
            elif(estado == 25):
                self.atualizaToken(Token.AND);
                return;
            elif(estado == 26):
                if(char == '|'):
                    estado = 27;
                else:
                    estado = 8;
            elif(estado == 27):
                self.atualizaToken(Token.OR);
                return;
            elif(estado == 28):
                if(char == '='):
                    estado = 29;
                else:
                    self.atualizaToken(Token.NOT);
                    return;
            elif(estado == 29):
                self.atualizaToken(Token.DIFFER);
                return;
            elif(estado == 30):
                self.atualizaToken(Token.CIGUAL);
                return;
            elif(estado == 31):
                if(char == '='):
                    estado = 32;
                else:
                    self.atualizaToken(Token.MAIOR);
                    return;
            elif(estado == 32):
                self.atualizaToken(Token.MAIORI);
                return;
            elif(estado == 33):
                if(char == '='):
                    estado = 34;
                else:
                    self.atualizaToken(Token.MENOR);
                    return;
            elif(estado == 34):
                self.atualizaToken(Token.MENORI);
                return;
            elif(estado == 35):
                self.atualizaToken(Token.ABRECHA);
                return;
            elif(estado == 36):
                self.atualizaToken(Token.FECHACHA);
                return;
            elif(estado == 37):
                while(char != '\n'):
                    char = self.getchar();
                    if(char == "EOF"):
                        break;

                Atual.linha = Atual.linha + 1;
                Atual.coluna = 1;
                Atual.lexema = Atual.lexema[:-3];
                estado = 1;
            elif(estado == 38):
                if(char != '*') and (char != "EOF"):
                    estado = 38;
                else:
                    estado = 40;
            elif(estado == 39):
                if(char == 'n'):
                    Atual.lexema = Atual.lexema[:-2] + "\n";
                elif(char == 't'):
                    Atual.lexema = Atual.lexema[:-2] + "\t";
                    
                estado = 21;
            elif(estado == 40):
                if(char == "/") or (char == "EOF"):
                    Atual.lexema = Atual.lexema[-2:-2];
                    estado = 1;
                elif(char == "*"):
                    estado = 40;
                else:
                    estado = 38;
            # elif(estado == 41):
            #     if(char == '/'):


if __name__ == "__main__":

    if(len(sys.argv) < 2):
        print("Especifique o nome do arquivo.");
        exit();

    lex = Lexico();
    lex.abre(sys.argv[1]);

    while(Atual.token != Token.EOF):
        lex.getToken();
        Atual.imprime();

    lex.fecha();