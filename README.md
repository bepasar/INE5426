

# INE5426 - Construção de Compiladores
## Grupo: Bernardo, Klaus e Tiago
## Trabalho 3 - Analise Semânticao

Programa que gera um analisador lexico para a linguagem CC-2021-2, utilizando o módulo lex da ferramenta PLY. As definições e expressões regulares elaboradas utilizam o módulo re, para expressões regulares em python.

- Documentaçao do PLY: https://www.dabeaz.com/ply/ply.html

- Versões do Python testadas:
    - 3.6.9
    - 3.8.10 

- Para instalar as dependencias:
    - make setup
    - ou: pip install -r requirements.txt

- Executar:
    - make FILE='nome do arquivo' run
    - ex.: make FILE=lcc_files/heap_sort.lcc run 

A saída do programa consiste no resultado da análise léxica, a qual é apresentado no próprio terminal, através de prints. Dois cenários são possíveis:

- Caso um erro léxico seja identificado, a análise é interrompida, e como saída serão apresentados o caractere que gerou o erro, a linha e a coluna onde o mesmo se encontra no código fonte, e também uma cópia desta linha, destacando o caractere de forma colorida, para facilitar sua localização.

- Não havendo nenhum erro léxico será apresentada uma opção para mostrar a lista de tokens.

A lista de tokens apresenta todos os tokens e seus respectivos lexemas, assim como a linha e coluna em que se encontram, seguindo a ordem em que foram lidos do código fonte (do início ao fim). 

## Sintatic

(rascunho)
Alterei para executar da forma como descrito acima mesmo. Primeiro vai realizar a analise lexica, e caso não tenha erros lexicos faz a sintatica.
