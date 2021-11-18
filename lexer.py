import ply.lex as lex
 
class Lexer(object):

	# Build the lexer
	def build(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)
	
	# Tokenize (execute lexical analysis)
	def run(self, data):
		self.lexer.input(data)
		print(f"{'Line':<8}{'Column':<10}{'Token':<17}{'Lexeme':>8}")
		while True:
			tok = self.lexer.token()
			if not tok or tok.type == 'error': 
				break      # No more input (end of file)
			col = self.find_column(tok)
			print('%s%s%s%s' % (str(tok.lineno).ljust(8, ' '), str(col).ljust(10, ' '), tok.type.ljust(19, ' '), tok.value))
	
	# Basic regular definitions
	digit  = r'([0-9])'
	letter = r'([A-Za-z])'

	# Regular expression rules for non-trivial terminals
	t_float_constant = digit + r'+\.' + digit + r'+'
	t_int_constant = digit + r'+'
	t_string_constant = r'\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\'' # nao entendi bem como funciona essa exp regular
	t_relop = r'<|<=|>|>=|!=|=='

	# A string containing ignored characters (spaces and tabs)
	t_ignore  = ' \t'

	# literals (1 character symbols)
	# the token type/value is the character itself
	literals = ['+', '-', '*', '/', '%', ',', ';', '=', '(', ')', '[', ']', '{', '}']

	# reserved keywords (specific cases of token 'ident')
	reserved = {
		'if' : 'if',
		'else' : 'else',
		'while' : 'while',
		'for' : 'for',
		'int' : 'int',
		'float' : 'float',
		'string' : 'string',
		'def' : 'def',
		'return' : 'return',
		'read' : 'read',
		'print' : 'print',
		'new' : 'new',
		'null' : 'null',
		'break' : 'break'
	}

	# List of token names. (This is always required)
	tokens = [
		'ident',
		'relop',
		'string_constant',
		'float_constant',
		'int_constant'
	] + list(reserved.values())


	identifier = r'(' + letter + r'(' + digit + r'|' + letter + r')*)'
	@lex.TOKEN(identifier)
	def t_ident(self, t):
		t.type = self.reserved.get(t.value,'ident')    # Check for reserved words
		return t

	# Define a rule so we can track line numbers
	def t_newline(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	# ignore comments (?)
	def t_comment(self, t):
		r'\//'
		pass
		# No return value. Token discarded

	# Error handling rule
	def t_error(self, t):
		col = self.find_column(t)
		print("Illegal character '%s' at line %s, column %s" % (t.value[0], t.lineno, col))
		t.lexer.skip(1)
		return t

	# Compute column
	def find_column(self, token):
		input = self.lexer.lexdata
		line_start = input.rfind('\n', 0, token.lexpos) + 1
		return (token.lexpos - line_start) + 1