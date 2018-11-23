class Token:
    ABREPAR  = 1;
    FECHAPAR = 2;
    VIRG     = 3;
    PTOVIRG  = 4;
    NUM      = 5;
    IDENT    = 6;
    STR      = 7;
    SOMA     = 8;
    MULT     = 9;
    DIV      = 10;
    SUB      = 11;
    MOD      = 12;
    POT      = 13;
    INPUT    = 14;
    OUTPUT   = 15;
    EOF      = 16;
    ERRO     = 17;
    IGUAL    = 18;

    msg = ['(', ')', ',', ';', 'NUM',
           'IDENT', 'STR', '+', '*',
           '/', '-', '%', '**', 'INPUT',
           'OUTPUT', 'EOF', 'ERRO', '='];

class Atual:
    linha  = 1;
    coluna = 0;
    token  = None;
    lexema = "";

    @classmethod
    def imprime(cls):
        print("Token: " + Token.msg[cls.token - 1] + "\tLexema: " + cls.lexema);

class Lexico:
    def __init__(self):
        self.nome    = None;
        self.arquivo = None;
        self.linha   = None;
        self.codigo  = "";
        self.cursor  = -1;

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
        return self.codigo[self.cursor];

    def removeChar(self):
        self.cursor = self.cursor - 1;
        Atual.lexema = Atual.lexema[:-1];

    def atualizaToken(self, tok):
        Atual.token = tok;
        self.removeChar();
        Atual.imprime();
        return;

    def getToken(self):
        
        estado = 1;
        Atual.lexema = "";

        while(True):
            char = self.getchar();
            #print("Char: " + char + ". Estado: " + str(estado));

            Atual.coluna = Atual.coluna + 1;
            if(char != 'EOF'):
                Atual.lexema = Atual.lexema + char;
            if(char == '\n'):
                Atual.linha = Atual.linha + 1;

            if(estado == 1):
                if(char in [' ', '\t', '\n']):
                    return;
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
                elif(char.lower() == 'i'):
                    estado = 21;
                elif(char.lower() == 'o'):
                    estado = 27;
                elif(char == '"'):
                    estado = 34;
                elif(char.isalpha()):
                    estado = 2;
                elif(char.isdigit()):
                    estado = 4;
                else:
                    self.removeChar();
                    estado = 8;
            # Identificador:
            elif(estado == 2):
                if(char.isalnum()):
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
                self.atualizaToken(Token.NUM);
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
                    estado = 5;
            elif(estado == 8):
                self.atualizaToken(Token.ERRO);
                return;
            elif(estado == 9):
                self.atualizaToken(Token.MOD);
                return;
            elif(estado == 10):
                self.atualizaToken(Token.DIV);
                return;
            elif(estado == 11):
                self.atualizaToken(Token.SUB);
                return;
            elif(estado == 12):
                self.atualizaToken(Token.SOMA);
                return;
            elif(estado == 13):
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
            # Input:
            elif(estado == 21):
                if(char.lower() == 'n'):
                    estado = 22;
                elif(char.isalnum()):
                    estado = 2;
                else:
                    estado = 3;
            elif(estado == 22):
                if(char.lower() == 'p'):
                    estado = 23;
                elif(char.isalnum()):
                    estado = 2;
                else:
                    estado = 3;
            elif(estado == 23):
                if(char.lower() == 'u'):
                    estado = 24;
                elif(char.isalnum()):
                    estado = 2;
                else:
                    estado = 3;
            elif(estado == 24):
                if(char.lower() == 't'):
                    estado = 25;
                elif(char.isalnum()):
                    estado = 2;
                else:
                    estado = 3;
            elif(estado == 25):
                if(char.isalnum()):
                    estado = 2;
                else:
                    self.removeChar();
                    estado = 26;
            elif(estado == 26):
                self.atualizaToken(Token.INPUT);
                return;
            # Output:
            elif(estado == 27):
                if(char.lower() == 'u'):
                    estado = 28;
                elif(char.isalnum()):
                    estado = 2;
                else:
                    estado = 3;
            elif(estado == 28):
                if(char.lower() == 't'):
                    estado = 29;
                elif(char.isalnum()):
                    estado = 2;
                else:
                    estado = 3;
            elif(estado == 29):
                if(char.lower() == 'p'):
                    estado = 30;
                elif(char.isalnum()):
                    estado = 2;
                else:
                    estado = 3;
            elif(estado == 30):
                if(char.lower() == 'u'):
                    estado = 31;
                elif(char.isalnum()):
                    estado = 2;
                else:
                    estado = 3;
            elif(estado == 31):
                if(char.lower() == 't'):
                    estado = 32;
                elif(char.isalnum()):
                    estado = 2;
                else:
                    estado = 3;
            elif(estado == 32):
                if(char.isalnum()):
                    estado = 2;
                else:
                    self.removeChar();
                    estado = 33;
            elif(estado == 33):
                self.atualizaToken(Token.OUTPUT);
                return;
            # String:
            elif(estado == 34):
                if(char == '"'):
                    estado = 35;
                else:
                    estado = 34;
            elif(estado == 35):
                self.atualizaToken(Token.STR);
                return;


            

if __name__ == "__main__":

    lex = Lexico();
    lex.abre("teste.txt");

    while(Atual.token != Token.EOF):
        lex.getToken();

    lex.fecha();