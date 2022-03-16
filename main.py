# Grupo: Bernardo, Klaus e Tiago

import sys
import sintatic
from pprint import pprint
from lexer import Lexer
from print_tree import print_tree

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
    lex_error = lex.run(f_contents)

    if not lex_error:
        print('Lexical SUCCESS! No lexical errors were found!\n')
        # a = input('Show symbols table and tokens list? \n\t y/n: ')
        # if a == 'y':
        #     lex.print_symbols_table()
        #     lex.print_token_list()

        lex.lexer.lineno = 1 # restart line counter after lexical analysis

        # Execute the parsing
        parsing_result = sintatic.run(parser, f_contents)
        print('Parsing SUCCESS! No syntax errors were found!\n')
        
        a = input('Show expression trees? \n\t y/n: ')
        if a == 'y':
            for i, node in enumerate(sintatic.syntax_tree_list):
                print('\nExpression tree %d' % (i+1))
                print_tree(node)

        a = input('Show symbol table? \n\t y/n: ')
        if a == 'y':
            pprint(sintatic.symbol_table.table)

        a = input('Show max scopes? \n\t y/n: ')
        if a == 'y':
            print(sintatic.max_scopes)

if __name__ == '__main__':
    main()