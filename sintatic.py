# Grupo: Bernardo, Klaus e Tiago

from cProfile import label
from doctest import OutputChecker
import logging
from symtable import Symbol
from turtle import left
import ply.yacc as yacc
import pprint

# data structures
class Node():
	def __init__(self, label, left, right) -> None:
		self.label = label
		self.left = left
		self.right = right

class Scope():
	def __init__(self, outerScope=None, loop=False) -> None:
		self.outer_scope = outerScope
		self.loop = loop
		self.symbol_table = dict()
		self.inner_scopes = []
	
	def add_symbol(self, label, type, values, lineno):
		if not label in self.symbol_table.keys:
			self.symbol_table[label] = (type, values, lineno)
		else:
			lineno_contained = self.symbol_table[label](3)
			# variable already in scope
			raise Exception(
				f"variable {label} declared in line {lineno} already in {lineno_contained}"
			)
		
	def as_dict(self):
		return pprint.pprint("symbol table: \n"+self.symbol_table)


# lista de nodos raiz das EXPA
syntax_tree_list = []
# stack de escopos 
scope_stack = []

def p_program(p):
	'''
	program : statement
			| funclist
			| empty
	'''
	pass


def p_funclist_funcdef(p):
	'''
	funclist : funcdef
	'''
	p[0] = p[1]

def p_funclist_recursive(p):
	'''
	funclist : funcdef funclist
	'''
	pass

def p_funcdef(p):
	'''
	funcdef : def ident '(' paramlist ')' new_scope '{' statelist '}'
	'''
	

# New rule for passing arrays as function parameters
def p_arr_param(p):
	'''
	arrparam 	: int '[' ']'
				| float '[' ']'
				| string '[' ']'
				| arrparam '[' ']'
				| arrparam ident
	'''
	p[0] = ' '.join(p[1:])

# New production for 'arr_param'
def p_paramlist_simple(p):
	'''
	paramlist 	: int ident
				| float ident
				| string ident
				| arrparam
				| empty 
	'''
	if p[1] is None:
		p[0] = ' ' # empty
	else:
		p[0] = ' '.join(p[1:])

# New production for 'arr_param'
def p_paramlist_complex(p):
	'''
	paramlist 	: int ident ',' paramlist
				| float ident ',' paramlist
				| string ident ',' paramlist
				| arrparam ',' paramlist
	'''
	p[0] = ' '.join(p[1:])

# New productions
# funcall ';' --> enable function calling without return. ex: heapsort(x,y)
# | whilestat --> addition of 'while' statement to the language
# removed '| ;' production because it enable ';;;;'... to be valid
def p_statement_vardecl(p):
	'''
	statement 	: vardecl ';'
				| funcall ';'
				| atribstat ';'
				| printstat ';'
				| readstat ';'
				| returnstat ';'
				| ifstat
				| forstat
				| whilestat
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
			| vardecl '[' int_constant ']'
			| vardecl '[' ident ']'
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

# New production to allow return values (ex 'return 2;')
def p_returnstat(p):
	'''
	returnstat 	: return
				| return factor
	'''
	p[0] = ' '.join(p[1:])

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

# New rule for while statement
def p_whilestat(p):
	'''
	whilestat : while '(' expression ')' statement
	'''
	p[0] = ' '.join(p[1:])

def p_statelist(p):
	'''
	statelist 	: statement
				| statement statelist
	'''
	p[0] = ' '.join(p[1:])

def p_lvalue(p): 
	'''
	lvalue 	: ident
			| ident arr
	''' 
	p[0] = ' '.join(p[1:])
	p[0] = Node('id', None, None)

# New rule, to solve ([numexpression])* problem
def p_lvalue_array(p):
	'''
	arr : '[' ']' 
		| '[' numexpression ']'
		| arr '[' ']'
		| arr '[' numexpression ']'
	'''
	p[0] = ' '.join(p[1:])

def p_expression(p):
	'''
	expression : numexpression
	'''
	p[0] = p[1]

def p_expression_relop(p):
	'''
	expression : numexpression relop numexpression
	'''
	p[0] = ' '.join(p[1:])

# New rule for boolean expressions
def p_expression_boolop(p):
	'''
	expression : expression boolop expression
	'''
	p[0] = ' '.join(p[1:])

def p_funcall(p):
	'''
	funcall : ident '(' paramlistcall ')' 
	'''
	p[0] = ' '.join(p[1:])

# Separate rule for single parameters, for better organization
# New productions: 
# 	float/int constant and funcall now can be used as parameters.
# 	ex: a = func(a, 2.5, 'acc', mult(5), 2)
def p_param(p):
	'''
	param 	: empty
			| ident
			| int_constant
			| float_constant
			| string_constant
			| funcall
	'''
	if p[1] is None: # empty
		p[0] = ' '
	else:
		p[0] = ' '.join(p[1:])
		
def p_paramlistcall(p):
	'''
	paramlistcall 	: param
					| param ',' paramlistcall
	'''
	p[0] = ' '.join(p[1:])

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
	p[0] = Node(p[2], p[1], p[3])

def p_term(p):
    '''
    term 	: unaryexpression
    		| unaryexpression '*' unaryexpression
    		| unaryexpression '/' unaryexpression
    		| unaryexpression '%' unaryexpression
    '''
    if len(p) == 1:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], p[1], p[3])


def p_unaryexpression(p):
	'''
	unaryexpression : factor
	'''
	p[0] = p[1]

def p_unaryexpression_signaled(p):
	'''
	unaryexpression : factor '+' factor
					| factor '-' factor
	'''
	p[0] = Node(p[2], p[1], p[3])

def p_factor(p):
    '''
    factor 	: int_constant
			| float_constant
			| string_constant
			| null
			| lvalue
			| '(' numexpression ')'
	'''
    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_allocexpression(p):
	'''
	allocexpression : new int '[' numexpression ']' dimensions
					| new float '[' numexpression ']' dimensions
					| new string '[' numexpression ']' dimensions
	'''
	p[0] = ' '.join(p[1:])

def p_dimensions_empty(p):
	'''
	dimensions : empty
	'''
	p[0] = ' '

def p_dimensions(p):
	'''
	dimensions : '[' numexpression ']'
	'''
	p[0] = ' '.join(p[1:])

def p_empty(p):
	'''
	empty :
	'''
	pass

def p_error(p):
	if p:
		print("Syntax error at token '" + p.value + "' at line", p.lineno)
	else:
		print("Syntax error at EOF. Please check parselog.txt file to pinpoint the error")

# actions
def p_new_scope(p: yacc.YaccProduction) -> None:
    """
    new_scope :
    """
    create_scope(False)

def create_scope(is_loop):
	top = scope_stack[-1]
	new = Scope(top, is_loop)
	if top:
		top.inner_scopes.append(new)
	scope_stack.append(new)

# Build yacc's LALR parsing table
# and save it at parsetab.py
def build_parser(tokens): # DONT REMOVE tokens
	parser = yacc.yacc()
	return parser

# Config logfile for debugging info output
logging.basicConfig(
	level = logging.DEBUG,
	filename = "parselog.txt",
	filemode = "w",
	format = "%(message)s"
)

# Parse code from a file
def run(parser, file):
	return parser.parse(input=file, debug=logging.getLogger())
