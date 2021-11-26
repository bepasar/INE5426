import sys
import ply.lex as lex
from lexer import Lexer

def main():
    # Open and read file
    filename = sys.argv[1]
    f = open(filename, 'r')
    f_contents = f.read()
    f.close()

    # Build the lexer
    lex = Lexer()

    # Execute the lexical analysis
    lex.run(f_contents)

if __name__ == '__main__':
    main()