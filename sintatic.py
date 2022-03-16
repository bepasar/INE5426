# Grupo: Bernardo, Klaus e Tiago

from cProfile import label
from doctest import OutputChecker
import logging
from symtable import Symbol
import sys
# from turtle import left
import ply.yacc as yacc
import pprint

# data structures
class Node():
	def __init__(self, value, left, right) -> None:
		self.value = value
		self.left = left
		self.right = right

	def as_dict(self):
		left = None if self.left == None else self.left.as_dict()
		right = None if self.right == None else self.right.as_dict()

		return {
			"value": self.value,
			"right": right,
			"left": left,
		}


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
	pass

def p_funclist_recursive(p):
	'''
	funclist : funcdef funclist
	'''
	pass

def p_funcdef(p):
	'''
	funcdef : def ident '(' paramlist ')'  '{' statelist '}'
	'''
	pass
	

# New rule for passing arrays as function parameters
def p_arr_param(p):
	'''
	arrparam 	: int '[' ']'
				| float '[' ']'
				| string '[' ']'
				| arrparam '[' ']'
				| arrparam ident
	'''
	pass

# New production for 'arr_param'
def p_paramlist_simple(p):
	'''
	paramlist 	: int ident
				| float ident
				| string ident
				| arrparam
				| empty 
	'''
	pass

# New production for 'arr_param'
def p_paramlist_complex(p):
	'''
	paramlist 	: int ident ',' paramlist
				| float ident ',' paramlist
				| string ident ',' paramlist
				| arrparam ',' paramlist
	'''
	pass

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
	pass

def p_vardecl(p):
	'''
	vardecl : int ident 
			| float ident
			| string ident
			| vardecl '[' int_constant ']'
			| vardecl '[' ident ']'
	'''
	pass

def p_atribstat(p):
	'''
	atribstat 	: lvalue '=' expression
				| lvalue '=' allocexpression
				| lvalue '=' funcall
	'''
	pass

def p_printstat(p):
	'''
	printstat : print expression
	'''
	pass

def p_readstat(p):
	'''
	readstat : read lvalue
	'''
	pass

# New production to allow return values (ex 'return 2;')
def p_returnstat(p):
	'''
	returnstat 	: return
				| return factor
	'''
	pass

def p_ifstat(p):
	'''
	ifstat : if '(' expression ')' statement
	'''
	pass

def p_ifstat_else(p):
	'''
	ifstat : if '(' expression ')' statement else statement
	'''
	pass

def p_forstat(p):
	'''
	forstat : for '(' atribstat ';' expression ';' atribstat ')' statement
	'''
	pass

# New rule for while statement
def p_whilestat(p):
	'''
	whilestat : while '(' expression ')' statement
	'''
	pass

def p_statelist(p):
	'''
	statelist 	: statement
				| statement statelist
	'''
	pass

def p_lvalue(p): 
	'''
	lvalue 	: ident
			| ident arr
	''' 
	p[0] = p[1]

# New rule, to solve ([numexpression])* problem
def p_lvalue_array(p):
	'''
	arr : '[' ']' 
		| '[' numexpression ']'
		| arr '[' ']'
		| arr '[' numexpression ']'
	'''
	if len(p) == 3:
		return 
	if p[2] != '[' and p[2] != ']':
		p[0] = p[2]
	elif p[3] != ']':
		p[0] = p[3]

def p_expression(p):
	'''
	expression : numexpression
	'''
	p[0] = p[1]
	# syntax_tree_list.append((p[0], p.lineno(1)))
	if p[0].left or p[0].right:  # skip single value expressions like 'x = 4;'
		syntax_tree_list.append(p[0])

def p_expression_relop(p):
	'''
	expression : numexpression relop numexpression
	'''
	p[0] = Node(p[2], p[1], p[3])
	syntax_tree_list.append(p[0])

# New rule for boolean expressions
def p_expression_boolop(p):
	'''
	expression : expression boolop expression
	'''
	p[0] = Node(p[2], p[1], p[3])
	syntax_tree_list.append(p[0])

def p_funcall(p):
	'''
	funcall : ident '(' paramlistcall ')' 
	'''
	pass

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
	pass
		
def p_paramlistcall(p):
	'''
	paramlistcall 	: param
					| param ',' paramlistcall
	'''
	pass

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
	if len(p) == 2:
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
        p[0] = Node(p[1], None, None)

def p_allocexpression(p):
	'''
	allocexpression : new int '[' numexpression ']' dimensions
					| new float '[' numexpression ']' dimensions
					| new string '[' numexpression ']' dimensions
	'''
	pass

def p_dimensions_empty(p):
	'''
	dimensions : empty
	'''
	pass

def p_dimensions(p):
	'''
	dimensions : '[' numexpression ']'
	'''
	pass

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
	sys.exit() # stops the parsing process

# actions
#def p_new_scope(p: yacc.YaccProduction) -> None:
#    """
#    new_scope :
#    """
    #create_scope(False)

#def create_scope(is_loop):
	#top = scope_stack[-1]
	#new = Scope(top, is_loop)
	#if top:
	#	top.inner_scopes.append(new)
	#scope_stack.append(new)

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
