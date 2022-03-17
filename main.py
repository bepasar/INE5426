# Grupo: Bernardo, Klaus e Tiago

import sys
import sintatic
from pprint import pprint
from lexer import Lexer
from print_tree import printExpressionTree

def print_expressions(expressions):
    exp_dict = []
    for (root, line) in expressions:
        print(root)
        exp_dict.append({"line":line, "tree":root.as_dict()})
    pprint(exp_dict)
    return exp_dict
            
def main():
    # Open and read file
    filename = sys.argv[1]
    f = open(filename, 'r')
    f_contents = f.read()
    f.close()

    # Build the lexer and parser
    lex = Lexer()
    parser = sintatic.build_parser(lex.get_tokens())

    # Execute the lexical analysis
    lex.run(f_contents)

    print('Lexical SUCCESS! No lexical errors were found!\n')
    a = input('Show tokens list? \n\t y/n: ')
    if a == 'y':
        lex.print_token_list()

    # Execute the parsing/semantic analysis
    sintatic.run(parser, f_contents)
    print('\nParsing SUCCESS! No syntax errors were found!\n')
    
    a = input('\nShow expression trees? \n\t y/n: ')
    if a == 'y':
        for i, node in enumerate(sintatic.syntax_tree_list):
            printExpressionTree(node, i)

    a = input('\nShow the scopes? \n\t y/n: ')
    if a == 'y':
        for i in range(len(sintatic.scope_list)):
            print("{:<8} {:<15} {:<20}".format('index','outer_scope','inner_scopes'))
            formatted_inner_scopes = []
            for s in sintatic.scope_list[i].inner_scopes:
                formatted_inner_scopes.append(sintatic.scope_list.index(s))
            
            try:
                os = sintatic.scope_list.index(sintatic.scope_list[i].outer_scope)
            except ValueError:
                os = ""
            print("{:<8} {:<15} {:<20}".format(i, os, str(formatted_inner_scopes)))
            pprint(sintatic.scope_list[i].symbol_table.table)
            print()

if __name__ == '__main__':
    main()