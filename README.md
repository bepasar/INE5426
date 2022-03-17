

# INE5426 - Construção de Compiladores
## Grupo: Bernardo, Klaus e Tiago
## Trabalho 3 - Analise Semântica

Programa que gera analisadores lexico e sintatico LALR(1) - shift reduce para a linguagem CC-2021-2, utilizando os módulos lex e yacc da ferramenta PLY, respectivamente. As definições e expressões regulares elaboradas utilizam o módulo re, para expressões regulares em python, já as regras da gramática seguem um formato específico da ferramenta (explicado em detalhes no relatório) que pode ser conferido na documentação do PLY

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

## Parte Léxica
A saída do programa consiste primeiramente do resultado da análise léxica, a qual é apresentado no próprio terminal, através de prints.

Caso um erro léxico seja identificado, a análise é interrompida, e como saída serão apresentados o    caractere que gerou o erro, a linha e a coluna onde o mesmo se encontra no código fonte, e também uma cópia desta linha, destacando o caractere de forma colorida, para facilitar sua localização.

Não havendo nenhum erro léxico, o usuário será solicitado para digitar uma entrada se desejar visualizar a lista de tokens geradas.

A lista de tokens apresenta todos os tokens e seus respectivos lexemas, assim como a linha e coluna em que se encontram, seguindo a ordem em que foram lidos do código fonte (do início ao fim).

## Parte Sintatica

Não havendo erros léxicos, a aplicação irá realizar na sequência a analise sintática do codigo fonte.
Esse processo irá gerar três arquivos, no diretório principal do projeto:
    - 'parsetab.py': contém a tabela de parsing gerada, utilizada para fazer a análise. Nota-se que aessa tabela só será gerada novamente se houverem modificaçoes nas regras definidas para a gramatica no código.

    - 'parser.out': é um arquivo para auxílio na depuração do processamento do analisador. Contém todas as regras da gramática, assim como uma lista dos estados e das ações (shift, reduce) que o analisador utiliza durante seu processamento dependendo do que possui na pilha.

    - 'parselog.txt': arquivo que é gerado à cada análise realizada. Mostra todos os passos realizados pelo analisador, indicando o conteudo da pilha, token corrente, estado de parsing utilizado e qual ação foi tomada, durante a analise do codigo fonte.

Se ocorrerem erros sintaticos, serão printados os tokens causadores do erro assim como sua linha no código.
Caso contrário uma mensagem de sucesso será apresentada no terminal.


## Parte Semântica

Na parte semantica geramos as arvores de derivação para as expressões aritméticas e as tabelas de símbolos por contexto
A tabela de símbolos lista todos os tokens identificadores encontrados, e como atributos, são mostrados os tipos e as linhas em que se encontram.