import ply.yacc as yacc

from lexer import tokens

def p_program_statement(p):
    'program : statement'
    p[0] = p[1]
    
def p_program_funclist(p):
    'program : funclist'
    p[0] = p[1]

def p_numexpression_term(p):
    'numexpression : term'
    p[0] = p[1]
    
def p_numexpression_plus(p):
    'numexpression : term PLUS'
    p[0] = p[1]
    