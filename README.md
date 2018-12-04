# Compilador-MiniC
Compilador da gramática MiniC desenvolvido em Python 3.7.1.
- o script *maquinaVirtual.py* simula o código em C fornecido como parâmetro;
- o script *sintatico.py* verifica se o código segue a gramática e exibe o código gerado para a máquina virtual;
- o script *lexico.py* exibe todos os tokens do código informado.

```
python3 maquinaVirtual.py <prog.c>
python3 sintatico.py <prog.c>
python3 lexico.py <prog.c>
```
