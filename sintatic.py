import ply.yacc as yacc

from lexer import tokens

def p_program(p):
	'''
	program : statement
			| funclist
			| empty
	'''
	p[0] = p[1]

def p_funclist_funcdef(p):
	'''
	funclist : funcdef
	'''
	p[0] = p[1]

def p_funclist_recursive(p):
	'''
	funclist : funcdef funclist
	'''
	p[0] = ' '.join(p[1:])

def p_funcdef(p):
	'''
	funcdef : def ident '(' paramlist ')' '{' statelist '}'
	'''
	p[0] = ' '.join(p[1:])

def p_paramlist_simple(p):
	'''
	paramlist 	: int ident
				| float ident
				| string ident
				| empty 
	'''
	if len(p) == 3:
		p[0] = p[1] + p[2]
	else:
		p[0] = '' # '' to avoid creating a None object when produciton is empty

def p_paramlist_complex(p):
	'''
	paramlist 	: int ident ',' paramlist
				| float ident ',' paramlist
				| string ident ',' paramlist
	'''
	p[0] = ' '.join(p[1:])


def p_statement_vardecl(p):
	'''
	statement 	: vardecl ';'
				| atribstat ';'
				| printstat ';'
				| readstat ';'
				| returnstat ';'
				| ifstat
				| forstat
				| '{' statelist '}' 
				| break ';'
				| ';'
	'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = ' '.join(p[1:])

def p_vardecl(p):
	'''
	vardecl : int ident 
			| float ident
			| string ident
	'''
	p[0] = ' '.join(p[1:])

def p_atribstat(p):
	'''
	atribstat 	: lvalue '=' expression
				| lvalue '=' allocexpression
				| lvalue '=' funcall
	'''
	p[0] = ' '.join(p[1:])

def p_printstat(p):
	'''
	printstat : print expression
	'''
	p[0] = p[1] + p[2]

def p_readstat(p):
	'''
	readstat : read lvalue
	'''
	p[0] = p[1] + p[2]

def p_returnstat(p):
	'''
	returnstat : return
	'''
	p[0] = p[1]

def p_ifstat(p):
	'''
	ifstat : if '(' expression ')' statement
	'''
	p[0] = ' '.join(p[1:])

def p_ifstat_else(p):
	'''
	ifstat : if '(' expression ')' statement else statement
	'''
	p[0] = ' '.join(p[1:])

def p_forstat(p):
	'''
	forstat : for '(' atribstat ';' expression ';' atribstat ')' statement
	'''
	p[0] = ' '.join(p[1:])

def p_statelist_simple(p):
	'''
	statelist : statement
	'''
	p[0] = p[1]

def p_statelist(p):
	'''
	statelist : statement statelist
	'''
	p[0] = ' '.join(p[1:])

# missing ([numexpression])*
def p_lvalue(p): 
	'''
	lvalue : ident
	''' 
	p[0] = p[1]

def p_expression(p):
	'''
	expression : numexpression
	'''
	p[0] = p[1]

def p_expression_relop(p):
	'''
	expression : numexpression relop numexpression
	'''
	p[0] = p[1]

def p_funcall(p):
	'''
	funcall : ident '(' paramlistcall ')' 
	'''
	p[0] = ' '.join(p[1:])

def p_paramlistcall_recursive(p):
	'''
	paramlistcall : ident ',' paramlistcall
	'''
	p[0] = ' '.join(p[1:])

def p_paramlistcall_empty(p):
	'''
	paramlistcall : empty
	'''
	p[0] = p[1]

def p_paramlistcall_simple(p):
	'''
	paramlistcall : ident ',' ident
	'''
	p[0] = ' '.join(p[1:])

def p_error(p):
	print("Syntax error in input!")

def p_expression_relop(p):
    'expression : numexpression relop numexpression'
    p[0] = p[1]

def p_funcall(p):
    '''funcall : ident '(' paramlistcall ')' '''
    p[0] = p[1] + p[2] + p[3] + p[4]

def p_paramlistcall_recursive(p):
    '''paramlistcall : ident ',' paramlistcall'''
    p[0] = p[1] + p[2] + p[3]

def p_paramlistcall_empty(p):
    'paramlistcall : empty'
    p[0] = p[1]

def p_paramlistcall_simple(p):
    '''paramlistcall : ident ',' ident'''
    p[0] = p[1] + ',' + p[2]

def p_error(p):
    print("Syntax error in input!")

def p_numexpression_term(p):
	'''
	numexpression : term
	'''
	p[0] = p[1]
	
def p_numexpression_recursion(p):
	'''
	numexpression 	: term '+' numexpression
					| term '-' numexpression
	'''
	p[0] = ' '.join(p[1:])

def p_term(p):
	'''term : unaryexpression'''
	p[0] = p[1]

def p_term_recursion(p):
	'''
	term 	: unaryexpression '*' unaryexpression
			| unaryexpression '/' unaryexpression
			| unaryexpression '%' unaryexpression
	'''
	p[0] = ' '.join(p[1:])

def p_unaryexpression(p):
	'''
	unaryexpression : factor
	'''
	p[0] = p[1]

def p_unaryexpression_signaled(p):
	'''
	unaryexpression : '+' factor
					| '-' factor
	'''
	p[0] = p[1] + p[2]

def p_factor(p):
	'''
	factor 	: int_constant
			| float_constant
			| string_constant
			| null
			| lvalue
			| '(' numexpression ')'
	'''
	if p[1] != '(':
		p[0] = str(p[1])
	else:
		p[0] = ' '.join(p[1:])

def p_allocexpression(p):
	'''
	allocexpression : new int '[' numexpression ']' dimensions
					| new float '[' numexpression ']' dimensions
					| new string '[' numexpression ']' dimensions
	'''
	# p[0] = p[1] + p[2] + '[' + p[4] + ']' + p[6]
	p[0] = ' '.join(p[1:])

def p_dimensions_empty(p):
	'''
	dimensions : empty
	'''
	p[0] = p[1]

def p_dimensions(p):
	'''
	dimensions : '[' numexpression ']'
	'''
	# p[0] = p[1] + p[2] + p[3]
	p[0] = ' '.join(p[1:])

def p_empty(p):
	'''
	empty :
	'''
	pass

# Build yacc's LALR parsing table
# and save it at parsetab.py
def make_parser():
	parser = yacc.yacc()
	return parser

# lex = Lexer()
# parser = yacc.yacc()

# while True:
#     try:
#         s = input('sintatic>')
#         print(s)
#     except EOFError:
#         break
#     if not s: continue
#     result = parser.parse(input=s, debug=True)
#     print(result)
	
