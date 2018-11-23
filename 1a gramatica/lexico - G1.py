# Compiladores I - 2o/2018
# Pedro Henrique Oliveira Veloso - 0002346
# Thales Henrique Damasceno Lima - 

class Token:
    ABREPAR  = 0;
    FECHAPAR = 1;
    VIRG     = 2;
    PTOVIRG  = 3;
    NUM      = 4;
    IDENT    = 5;
    STR      = 6;
    SOMA     = 7;
    MULT     = 8;
    DIV      = 9;
    SUB      = 10;
    MOD      = 11;
    POT      = 12;
    INPUT    = 13;
    OUTPUT   = 14;
    EOF      = 15;
    ERRO     = 16;
    IGUAL    = 17;

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
        print("Token: " + Token.msg[cls.token] + "\tLexema: " + cls.lexema);

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
        Atual.coluna = Atual.coluna - 1;
        Atual.lexema = Atual.lexema[:-1];

    def atualizaToken(self, tok):
        Atual.token = tok;
        self.removeChar();

        if(Atual.lexema == "output"):
            Atual.token = Token.OUTPUT;
        elif(Atual.lexema == "input"):
            Atual.token = Token.INPUT;

        #Atual.imprime();
        return;

    def getToken(self):
        
        estado = 1;
        Atual.lexema = "";

        while(True):
            char = self.getchar();
            #print("Char: " + char + "\t Estado: " + str(estado) + "\t Lexema: |" + Atual.lexema + "|");

            # Se achar comentario, procura pelo fim da linha:
            if(char == "#"):
                while((char != "\n") and (char != "EOF")):
                    char = self.getchar();

            Atual.coluna = Atual.coluna + 1;

            # Adiciona ao lexema se nao for EOF:
            if(char != 'EOF'):
                Atual.lexema = Atual.lexema + char;
            else:
                Atual.lexema = Atual.lexema + ' ';

            # Conta uma nova linha:
            if(char == '\n'):
                Atual.linha = Atual.linha + 1;

            # Automato:
            if(estado == 1):
                if(char in [' ', '\t', '\n']):
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
                else:
                    self.removeChar();
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
            # String:
            elif(estado == 21):
                if(char == '"'):
                    estado = 22;
                else:
                    estado = 21;
            elif(estado == 22):
                self.atualizaToken(Token.STR);
                return;


            

if __name__ == "__main__":

    lex = Lexico();
    lex.abre("teste.txt");

    while(Atual.token != Token.EOF):
        lex.getToken();
        Atual.imprime();

    lex.fecha();