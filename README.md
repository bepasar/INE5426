# INE5426 - Construção de Compiladores

## Trabalho 1 - Analisador Léxico

Programa que gera um analisador lexico para a linguagem CC-2021-2, utilizando o módulo lex da ferramenta PLY. As definições e expressões regulares elaboradas utilizam o módulo re, para expressões regulares em python.

- Documentaçao do PLY: https://www.dabeaz.com/ply/ply.html

- Dependencias: ply (utilizamos a versão 3.11)
    - pip install ply
    - ou tambem: pip install -r requirements.txt

- Executação:
    - Windows:  python main.py 'arquivo.lcc'
    - Linux:    python3 main.py 'arquivo.lcc'

A saída do programa consiste no resultado da análise léxica, a qual é apresentado no próprio terminal, através de prints. Dois cenários são possíveis:

- Caso um erro léxico seja identificado, a análise é interrompida, e como saída serão apresentados o    caractere que gerou o erro, a linha e a coluna onde o mesmo se encontra no código fonte, e também uma cópia desta linha, destacando o caractere de forma colorida, para facilitar sua localização.

- Não havendo nenhum erro léxico, serão apresentadas a tabela de símbolos, seguida da lista de tokens.

A tabela de símbolos lista todos os tokens identificadores encontrados, e como atributos, são mostradas a quantidade de ocorrências e uma lista contendo os números das linhas em que estão presentes.

A lista de tokens apresenta todos os tokens e seus respectivos lexemas, assim como a linha e coluna em que se encontram, seguindo a ordem em que foram lidos do código fonte (do início ao fim). 
