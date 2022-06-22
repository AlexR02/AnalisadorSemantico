# Analisador Sintático em Python para C

## Compilação

Para compilar o programa é necessário utilizar o python3 e basta utilizar o seguinte comando no terminal:

``python3 analiseSemantica.py`` 

O retorno da execução será um print contendo todos os tokens encontrados e sua devida descrição.

## Sobre o Analisador - Parte Léxica e Sintática
O analisador desenvolvido tem como o intuito separar em tokens um código simples escrito em C com algumas contas matemáticas. Após identificados os tokens eles são inseridos em um dicionário, como o dicionário é baseado em chave e valor ,chaves repetidas não são inseridas novamente, o que não é necessário e ainda economiza memória. Essa análise é uma melhora da Léxica e também realiza verificações como balanceamento de parênteses e chaves por exemplo, a ideia era incluir a estruturação de declarações de variáveis e passagem de parâmetros em funções também, mas foram encontrados problemas nessas implementações e elas serão feitas assim que possível.

## Analise Semantica
A quantidade de implementação para englobar todos os casos acabou escalando muito rápido, então algumas partes da análise semantica foram deixadas de fora.

## Está Funcionando
Está sendo possível validar a declaração em cadeia de variáveis e a verificação dá já declaração de uma variável, assim como saber qual o seu escopo e seu valor na declaração. O código de exemplo junto do reposítorio exemplifica o caso.

## Não Está Funcionando
Ainda precisa ser inserido a validação e verificação de operações matemáticas
