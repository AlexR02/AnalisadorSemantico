import re

class Variavel:
    def __init__(self, identificador, tipo, valor, escopo):
        self.identificador = identificador
        self.valor = valor
        self.escopo = escopo
        self.tipo = tipo
    
    def __str__(self):
        return "Nome de variável{Tipo: " + self.tipo + ", Valor: " + self.valor + "}"

def analiseSintatica():
    #f = open("codigo1.c", "r") #Abre o arquivo para leitura
    #f = open("codigo2.c", "r")
    #f = open("codigo3.c", "r")
    f = open("codigo4.c", "r")
    #f = open("codigo5.c", "r")
    #f = open("codigo6.c", "r")
    #f = open("codigo7.c", "r")
    #f = open("codigo8.c", "r")
    #f = open("codigo9.c", "r")
    #f = open("codigo10.c", "r")
    lines = f.readlines()

    tokens = {}
    qtdLines = 1
    pilhaDelimitadoresC = [] #pilha delimitadores chaves
    pilhaDelimitadoresP = [] #pilha delimitadores parenteses

    for line in lines:
        line = re.sub(r"{", " { ", line)
        line = re.sub(r";", " ;", line)
        line = re.sub(r",", " , ", line)
        line = re.sub(r"[ ]{0,}\(", " ( ", line)
        line = re.sub(r"[ ]{0,}\)", " ) ", line)
        line = re.sub(r"\|\|", " || ", line)
        line = re.sub(r"&&", " && ", line)
        line = re.sub(r"=", " = ", line)
        line = re.sub(r"\+", " + ", line)
        line = re.sub(r"-", " - ", line)
        line = re.sub(r"/", " / ", line)
        line = re.sub(r"\*", " * ", line)
        line = re.sub(r"%", " % ", line)
        line = re.sub(r"[^.h]>", " > ", line)
        line = re.sub(r"<[^A-Za-z]", " < ", line)
        line = re.sub(r"!", " ! ", line)
        line = re.sub(r"=[ ]{0,}=", " == ", line)
        line = re.sub(r">[ ]{0,}=", " >= ", line)
        line = re.sub(r"<[ ]{0,}=", " <= ", line)
        line = re.sub(r"![ ]{0,}=", " != ", line)
        line = re.sub(r"[ ]{2,}", " ", line)
        #print(line)
        if line.strip() != '':
            line = line.strip()

            if re.search(r"^#include <.*[.]h>$", line):
                line = line.split()
                tokens[line[0]] = "Palavra reservada"
                biblioteca = re.sub(r"(<|>)","", line[1])
                tokens[biblioteca] = "Biblioteca"
            elif re.search(r"^int main\(\)( {|)$", line):
                line = line.split()
                tokens[line[0]] = "Palavra reservada"
                tokens[line[1]] = "Palavra reservada"
                if len(line) == 3:
                    tokens[line[2]] = "Delimitador de início"
            elif line == "{":
                tokens[line] = "Delimitador de início"
                pilhaDelimitadoresC.append(qtdLines)
            elif line == "}":
                tokens[line] = "Delimitador de fim"
                if len(pilhaDelimitadoresC) > 0:
                    pilhaDelimitadoresC.pop()
                else:
                    print("Delimitador de fim '}' a mais na linha " + str(qtdLines))
                    return
            else:
                aux = line
                tipoAtribuicaoCorrente = ""
                line = line.split()
                for j in range(len(line)):
                    i = line[j]
                    #print(i)
                    if i == "int" or i == "return" or i == "if" or i == "float":
                        tipoAtribuicaoCorrente = i
                        tokens[i] = "Palavra reservada"
                    elif i == "{" or i == "(":
                        tokens[i] = "Delimitador de início"
                        if i == "{":
                            pilhaDelimitadoresC.append(qtdLines)
                        elif i == "(":
                            pilhaDelimitadoresP.append(qtdLines)
                        tipoAtribuicaoCorrente = ""
                    elif i == "}" or i == ")":
                        tipoAtribuicaoCorrente = ""
                        tokens[i] = "Delimitador de fim"
                        if i == '}' and len(pilhaDelimitadoresC) > 0:
                            pilhaDelimitadoresC.pop()
                        elif i == ")" and len(pilhaDelimitadoresP) > 0:
                            tipoAtribuicaoCorrente = ""
                            pilhaDelimitadoresP.pop()
                        else:
                            print("Delimitador de fim " + i + " a mais na linha " + str(qtdLines))
                            return
                    elif i == "=":
                        tokens[i] = "Comando de atribuição"
                    elif i == "+":
                        tokens[i] = "Operador de adição"
                    elif i == "*":
                        tokens[i] = "Operador de multiplicação"
                    elif i == "-":
                        tokens[i] = "Operador de subtração"
                    elif i == "/":
                        tokens[i] = "Operador de divisão"
                    elif i == "%":
                        tokens[i] = "Operador resto da divisão"
                    elif i == ";":
                        tipoAtribuicaoCorrente = ""
                        tokens[i] = "Finalizador de linha"
                    elif re.search(r"^[a-zA-Z]{1,}[0-9]*$", i):
                        if tipoAtribuicaoCorrente == "" and i not in tokens:
                            print("Erro na linha " + str(qtdLines) + ", a variável '" + i + "' não foi declarada corretamente")
                            return
                        elif tipoAtribuicaoCorrente != "" and i in tokens:
                            print("Erro na linha " + str(qtdLines) + ", a variável '" + i + "' já foi declarada")
                            return
                        else:
                            escopo = pilhaDelimitadoresC[len(pilhaDelimitadoresC) - 1] if len(pilhaDelimitadoresC) > 0 else 0
                            identificador = i
                            tipo = tipoAtribuicaoCorrente
                            valor = ""
                            if line[j + 1] == "=":
                                if tipo == "int" or tipo == "float":
                                    if re.search(r"^[0-9]{1,}([.][0-9]{1,}|)$", line[j + 2]):
                                        valor = line[j + 2]
                                    else:
                                        print("Erro na linha " + str(qtdLines) + ", valor não definido para variável: " + i)
                                        return
                            var = Variavel(identificador, tipo, valor, escopo)
                            tokens[i] = var
                    elif re.search(r"^[0-9]{1,}([.][0-9]{1,}|)$", i):
                        tokens[i] = "Constante numérica"
                    elif re.search(r"^\".+\"$", i):
                        tokens[i] = "String constante"
                    elif i == ",":
                        tokens[i] = "Separador"
                    elif i in ["==", "!="]:
                        tokens[i] = "Operador de igualdade"
                    elif i in [">", "<",">=", "<="]:
                        tokens[i] = "Operador relacional"
                    elif i in ["!", "&&", "||"]:
                        tokens[i] = "Operador lógico"
                    else:
                        if i == "#include":
                            i = aux
                        print("O token '" + i + "' na linha " + str(qtdLines) + " é inválido")
                        return
        qtdLines += 1
    if(len(pilhaDelimitadoresC) > 0):
        print("Delimitador de início '{' a mais na linha " + str(pilhaDelimitadoresC[len(pilhaDelimitadoresC)-1]))
        return
    if(len(pilhaDelimitadoresP) > 0):
        print("Delimitador de início '(' a mais na linha " + str(pilhaDelimitadoresP[len(pilhaDelimitadoresP)-1]))
        return
    for key in tokens:
        print(key + " - " + str(tokens[key]))
    
def main():
    analiseSintatica()

main()
