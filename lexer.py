import ply.lex as lex
 
class Lexer(object):
	def __init__(self, **kwargs):
		self.symbols_table = dict()
		self.tokens_list = list()
		self.lexer = lex.lex(module=self, **kwargs)
	
	# Tokenize (execute lexical analysis)
	# on some data.
	# 'data' (string containing the whole
	# source code from a .lcc file)
	def run(self, data):
		self.lexer.input(data)
		lexical_error = False

		# Tokenize the next lexeme until EOF
		# or until an lexical error is found.
		tok = self.lexer.token()
		while tok:
			# Lexical error identified
			if tok.type == 'error':
				lexical_error = True
				break

			col = self.find_column(tok)

			# Insert token instance in the tokens list
			self.tokens_list.append((tok, col))

			# Initialize/update the symbols table
			if tok.type == 'ident':
				if tok.value in self.symbols_table:
					self.symbols_table[tok.value][0] += 1				# token occurrences counter
					self.symbols_table[tok.value][1].add(tok.lineno)	# set of lines where token is present 
				else:
					self.symbols_table[tok.value] = [1, {tok.lineno}]

			# Get next token
			tok = self.lexer.token()

		if not lexical_error:
			self.print_symbols_table()
			self.print_token_list()
	

	def print_token_list(self):
		print("_______________________________TOKENS LIST________________________________")
		print('Line'.ljust(8, ' ') + 'Column'.ljust(10, ' ') + 'Token'.ljust(19, ' ') + 'Lexeme'.ljust(8, ' '))
		for (tok, col) in self.tokens_list:
			print('%s%s%s%s' % (str(tok.lineno).ljust(8, ' '), str(col).ljust(10, ' '), tok.type.ljust(19, ' '), tok.value))
		print("__________________________________________________________________________")

	def print_symbols_table(self):
		print("_______________________________SYMBOLS TABLE______________________________")
		print('Identifier'.ljust(20, ' ') + 'Occurrences'.ljust(16, ' ') + 'Lines')
		for token, attrib in self.symbols_table.items():
			lines = sorted(attrib[1])
			print('%s%s' % (token.ljust(20, ' '), str(attrib[0]).ljust(16, ' ')) + str(lines[:10]))
			i = 10
			while i < (len(lines)):
				print(''.ljust(36, ' ') + str(lines[i:i+10]))
				i += 10
			print('')
		print("__________________________________________________________________________")


	# Basic regular definitions
	digit  = r'([0-9])'
	letter = r'([A-Za-z])'

	# Regular expression rules for non-trivial terminals
	t_float_constant = digit + r'+\.' + digit + r'+'
	t_int_constant = digit + r'+'
	t_string_constant = r'".*" | \'.*\'' # '.' represents any character
	
	t_relop = r'<|<=|>|>=|!=|=='
	t_boolop = r'!|&&|[||]'

	# A string containing ignored characters (spaces and tabs)
	t_ignore  = ' \t'

	# literals (1 character symbols)
	# the token type/value is the character itself
	literals = ['+', '-', '*', '/', '%', ',', ';', '=', '(', ')', '[', ']', '{', '}']

	# reserved keywords (specific cases of token 'ident')
	reserved = {
		'main' : 'main',
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
		'boolop',
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

	# ignore single line comments
	def t_comment(self, t):
		r'//.*'
		pass # No return value -> Token discarded

	# Error handling rule
	def t_error(self, t):
		col = self.find_column(t)
		line = self.lexer.lexdata.split('\n')[t.lineno - 1]
		print("Lexical error! Unexpected character '%s' at line %s, column %s:" % (t.value[0], t.lineno, col))
		print(line[:col-1] + '\x1b[6;30;42m' + t.value[0] + '\x1b[0m' + line[col:]) # higlight the error
		t.lexer.skip(1)
		return t

	# Compute column
	def find_column(self, token):
		input = self.lexer.lexdata
		line_start = input.rfind('\n', 0, token.lexpos) + 1
		return (token.lexpos - line_start) + 1