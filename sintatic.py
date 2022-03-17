# Grupo: Bernardo, Klaus e Tiago

import logging
import sys
import ply.yacc as yacc
import pprint

# data structures
class Node():

	def __init__(self, value, left, right, type, line) -> None:
		self.value = value
		self.left = left
		self.right = right
		self.type = type
		self.lineno = line

	def as_dict(self) -> None:
		left = None if self.left == None else self.left.as_dict()
		right = None if self.right == None else self.right.as_dict()

		return {
			"value": self.value,
			"right": right,
			"left": left,
		}
	
	def check_valid(self) -> bool:
		esq = self.left.type if type(self.left) == Node else self.left
		dir = self.right.type if type(self.right) == Node else self.right

		if esq == dir:
			self.type = esq
			return True

		raise SystemExit(
			f"Semantic error at (sub)expression: ´{self.left.value} {self.value} {self.right.value}´ at line {self.lineno}\n"
			f"Incompatible types of operands {self.left.value}({esq}) and {self.right.value}({dir})"
		)
		# sys.exit()

class SymbolTable():
	def __init__(self):
		self.table = {}
	
	def insert_into(self, var: dict, label: str):
		if label in self.table:
			datatype = self.table[label]["datatype"]
			line = self.table[label]["line"]
			raise SystemExit(
				f"variable ´{label}´ already declared (as {datatype} type) at line {line}"
			)
		else:
			self.table[label] = var
	
	def get_type(self, label):
		if label in self.table:
			return self.table[label]["datatype"]
		else:
			print(f"variable '{label}' not yet declared in the scope")
		return None


class Scope():
	def __init__(self, outerScope=None, loop=False) -> None:
		self.outer_scope = outerScope
		self.loop = loop
		self.symbol_table = SymbolTable()
		self.inner_scopes = []
		
	def exists(self, label) -> int:
		if label in self.symbol_table.table:
			return self.symbol_table.table[label]["line"]
		# recursive call to parents	
		if self.outer_scope:
			self.outer_scope.exists(label)
		return 0

	def as_dict(self):
		return pprint.pprint("symbol table: \n"+self.symbol_table)

	def get_type_recursively(self, label):
		if label in self.symbol_table.table:
			return self.symbol_table.get_type(label)
		
		if self.outer_scope: 
			return self.outer_scope.get_type_recursively(label)
			
		return None
	
	def add_inner_scopes(self, scope):
		self.inner_scopes.append(scope)
		if self.outer_scope:
			self.outer_scope.add_inner_scopes(scope)

# list of EXPA root nodes
syntax_tree_list = []
# scope stack 
scope_stack = []

max_scopes = 0

# store all the used scopes
scope_list = []

def p_program(p):
	'''
	program : open_scope statement close_scope
			| open_scope funclist close_scope
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
	funcdef : def ident open_scope '(' paramlist ')' '{' statelist '}' close_scope
	'''
	if scope_stack:
		if not scope_stack[-1].exists(p[2]): 
			scope_stack[-1].symbol_table.insert_into({"line": p.lineno(2), "datatype": "function", "values":[]}, p[2])
		else:
			raise SystemExit(
				f"Declaration error! Symbol {p[2]} at line {p.lineno(2)} already declared at line {scope_stack[-1].exists(p[2])}"
			)
		
def p_open_scope(p):
	'''
	open_scope : 
	'''
	if len(scope_stack) == 0:
		scope_stack.append(Scope())
	else:
		new_scope = Scope(scope_stack[-1], False)
		scope_stack.append(new_scope)
		scope_stack[-1].add_inner_scopes(new_scope)
	global max_scopes
	max_scopes = max_scopes + 1

def p_close_scope(p):
	'''
	close_scope : 
	'''
	scope_list.append(scope_stack.pop())

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
	if len(p) == 3:
		if not scope_stack[-1].exists(p[2]):
			scope_stack[-1].symbol_table.insert_into({"line": p.lineno(2), "datatype": p[1], "values":[]}, label=p[2])
		else:
			raise SystemExit(
				f"Declaration error! Symbol {p[2]} at line {p.lineno(2)} already declared at line {scope_stack[-1].exists(p[2])}"
			)


# New production for 'arr_param'
def p_paramlist_complex(p):
	'''
	paramlist 	: int ident ',' paramlist
				| float ident ',' paramlist
				| string ident ',' paramlist
				| arrparam ',' paramlist
	'''
	if len(p) == 5:
		if not scope_stack[-1].exists(p[2]):
			scope_stack[-1].symbol_table.insert_into({"line": p.lineno(2), "datatype": p[1], "values":[]}, label=p[2])
		else:	
			raise SystemExit(
				f"Declaration error! Symbol {p[2]} at line {p.lineno(2)} already declared at line {scope_stack[-1].exists(p[2])}"
			)


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
				| open_scope '{' statelist '}' close_scope
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
	if len(p) < 4:
		if not scope_stack[-1].exists(p[2]):
			scope_stack[-1].symbol_table.insert_into({"line": p.lineno(2), "datatype": p[1], "values":[]}, label=p[2])
		else:
			raise SystemExit(
				f"Declaration error! Symbol {p[2]} at line {p.lineno(2)} already declared at line {scope_stack[-1].exists(p[2])}"
			)


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
	p[0] = Node(p[1], None, None, scope_stack[-1].get_type_recursively(p[1]), p.lineno(1))

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
	p[0] = Node(p[2], p[1], p[3], None, p.lineno(2))
	syntax_tree_list.append(p[0])

# New rule for boolean expressions
def p_expression_boolop(p):
	'''
	expression : expression boolop expression
	'''
	p[0] = Node(p[2], p[1], p[3], None, p.lineno(2))
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
	p[0] = Node(p[2], p[1], p[3], None, p.lineno(2))

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
		p[0] = Node(p[2], p[1], p[3], None, p.lineno(2))
		p[0].check_valid()


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
	p[0] = Node(p[2], p[1], p[3], None, p.lineno(2))
	p[0].check_valid()

def p_factor(p):
    '''
    factor 	: null
			| lvalue
			| '(' numexpression ')'
	'''
    if p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = p[1]

def p_factor_int(p):
	'''
	factor 	: int_constant
	'''
	p[0] = Node(p[1], None, None, 'int', p.lineno(1))

def p_factor_float(p):
	'''
	factor 	: float_constant
	'''
	p[0] = Node(p[1], None, None, 'float', p.lineno(1))

def p_factor_string(p):
	'''
	factor 	: string_constant
	'''
	p[0] = Node(p[1], None, None, 'string', p.lineno(1))

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
	return parser.parse(input=file, debug=logging.getLogger(), tracking=True)
