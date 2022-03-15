# Grupo: Bernardo, Klaus e Tiago

import sys
import sintatic
from pprint import pprint
from lexer import Lexer

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
        print('Lexical SUCCESS! No lexical errors were found!')
        lex.lexer.lineno = 1 # restart line counter after lexical analysis

        # Execute the parsing
        parsing_result = sintatic.run(parser, f_contents)
        print(type(parsing_result))
        print(type(f_contents))
        #print(parsing_result[-1], f_contents[-1])
        if parsing_result is not None and parsing_result[-1] == f_contents[-1]: # TODO: ver uma forma melhor de validar esse teste
            print('Parsing SUCCESS! No syntax errors were found!')
        print_expressions(sintatic.syntax_tree_list)
            
        #print(sintatic.syntax_tree_list)
            
if __name__ == '__main__':
    main()