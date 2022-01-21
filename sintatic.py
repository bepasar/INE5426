import ply.yacc as yacc

from lexer import tokens, Lexer

def p_program_statement(p):
    'program : statement'
    p[0] = p[1]

def p_statement_ident(p):
    'statement : ident'
    p[0] = p[1]

def p_error(p):
    print("Syntax error in input!")

'''    
def p_program_funclist(p):
    'program : funclist'
    p[0] = p[1]

def p_numexpression_term(p):
    'numexpression : term'
    p[0] = p[1]
    
def p_numexpression_plus(p):
    'numexpression : term PLUS'
    p[0] = p[1]
'''
lex = Lexer()
parser = yacc.yacc()

while True:
    try:
        s = input('sintatic>')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(input=s, debug=True)
    print(result)
    