import sys
import ply.lex as lex
from lexer import Lexer

def main():
    # Open and read file
    filename = sys.argv[1]
    print (filename)
    f = open(filename, 'r')
    f_contents = f.read()
    f.close()

    # Build the lexer and try it out
    lex = Lexer()
    lex.build()
    lex.run(f_contents)

if __name__ == '__main__':
    main()