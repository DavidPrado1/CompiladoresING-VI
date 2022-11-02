# ------------------------------------------------------------
# calclex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import ply.lex as lex

# r'atring' -> r significa que la cadena es tradada sin caracteres de escape,
# es decir r'\n' seria un \ seguido de n (no se interpretaria como salto de linea)
 # List of token names.   This is always required
reserved = {
    'if' : 'IF',
    'elif' : 'ELIF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'int' : 'T_INTEGER',
    'float' : 'T_FLOAT',
    'string' : 'T_STRING',
    'char' : 'T_CHARACTER',
    'bool' : 'T_BOOLEAN',
    'return' : 'RETURN',
    'void' : 'void',
    'op' : 'OP',
    'main' : 'MAIN',
    'call' : 'CALL'
}
it= 1

tokens = [
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LCORCH',
    'RCORCH',
    'LLLAVE',
    'RLLAVE', 
    'CONDICIONAL',
    'ID',
    'COMMENT',
    'FLOAT',
    'STRING',
    'newline',
    'CARACTER',
    'ASIGNACION',
    'MAYOR',
    'MENOR',
    'IGUAL',
    'DIFERENTE',
    'MAYORIGUAL',
    'MENORIGUAL',
    'PLUSPLUS',
    'MINUSMINUS',
    'COMA',
    'FIN'
] + list(reserved.values())

 
 # Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LCORCH  = r'\['
t_RCORCH  = r'\]'
t_LLLAVE  = r'\{'
t_RLLAVE  = r'\}'
t_ASIGNACION  = r'='
t_MAYOR  = r'>'
t_MENOR  = r'<'
t_IGUAL  = r'=='
t_DIFERENTE = r'!='
t_MAYORIGUAL  = r'>='
t_MENORIGUAL  = r'<='
t_PLUSPLUS  = r'\+\+'
t_MINUSMINUS  = r'\-\-'
t_COMA = r','
t_FIN = r';'
#t_NUMBER  = r'\d+'
 
 # A regular expression rule with some action code

def t_COMMENT(t):
     r'v\-:.*'
     t.value = str(t.value)
     return t

def t_FLOAT(t):
     r'\d+\.\d+'
     t.value = float(t.value)
     return t

def t_STRING(t):
     r'\".*\"'
     t.value = str(t.value)
     return t

def t_CARACTER(t):
     r'\'.\''
     t.value = str(t.value)
     return t


def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value,'ID')
     return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # guardamos el valor del lexema  
    #print("se reconocio el numero")
    return t
 
 # Define a rule so we can track line numbers
def t_newline(t):
    r'\n'
    t.value = str('new line')
    return t
 
 # A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
 # Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
 
# Build the lexer

lexer = lex.lex()


f = open('test1.txt', 'r')
data = f.read()

# Give the lexer some input
lexer.input(data)
tokensLexer = []
# Test it out
 
# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
  tok = lexer.token()
  if not tok:
    break  # No more input
  #print(tok)
  tokensLexer.append({
    'type': tok.type,
    'lexeme': tok.value,
    'line': it
  })
  if tok.type == 'newline':
    it += 1
f.close()

tokensLexer.append({'type': '$', 'lexeme': '$', 'line': "-"})