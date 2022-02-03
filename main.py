# Grupo: Bernardo, Klaus e Tiago

import sys
import sintatic
from lexer import Lexer

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

    # Execute the parsing
    if not lex_error:
        result = sintatic.run(parser, f_contents)
        print(result)


if __name__ == '__main__':
    main()