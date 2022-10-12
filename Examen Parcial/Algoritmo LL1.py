import pandas as pd
from tabulate import tabulate
import graphviz

dot = graphviz.Digraph(comment='The Round Table')


counter = 0
syntax_table = pd.read_csv("syntax_table.csv", index_col=0)

class node_stack:
  def __init__(self, value, tree):
    global counter
    self.id = counter
    self.value = value
    self.tree = tree # boolean

    counter += 1

stack = []
symbol_1 = node_stack('$', '')
symbol_2 = node_stack('Program', '')
stack.insert(0, symbol_1)
stack.insert(0, symbol_2)

def js():
  inp = ''
  iter=0
  for i in stack:
    inp = inp + ' ' + stack[iter].value
    iter=iter+1
  return inp
  
tokens = []
#archivo = open("test1.txt", "r", encoding='utf-8')
#archivo = open("test2.txt", "r", encoding='utf-8')
archivo = open("test1.txt", "r", encoding='utf-8')
it = 1
for linea in archivo:
  lista = []
  t = linea.strip()
  lista= linea.split()
  for i in lista:
    ex = {'type':i, 'lexeme':'ss', 'line':it}
    tokens.append(ex)
  it = it + 1
archivo.close
print(tokens)
def jt():
  inp = ''
  iter=0
  for i in tokens:
    inp = inp + ' ' + tokens[iter]['type']
    iter=iter+1
  return inp

tokens.append({'type': '$', 'lexeme': '$', 'line': 'last'})

lstack=[]
limput=[]
laction=[]

nods=['0','1','2','3','4','5','6','7','8','9','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

print(len(nods))
dot.node(nods[0],stack[0].value)
stack[0].tree=nods[0]
g=0

while True:
  lstack.append(js())
  if stack[0].value == '$' and tokens[0]['type'] == '$':
    break
  else:
    if stack[0].value == tokens[0]['type']:
      laction.append('terminal')
      limput.append(jt())
      stack.pop(0)
      tokens.pop(0)
    else:
      if syntax_table.loc[stack[0].value][tokens[0]['type']] == 'no':
        limput.append(jt())
        laction.append("Error Sintactico")
        break
      else:
        if (syntax_table.loc[stack[0].value][tokens[0]['type']] != 'e'):
          laction.append(syntax_table.loc[stack[0].value][tokens[0]['type']])
          lista = syntax_table.loc[stack[0].value][tokens[0]['type']].split()
          anterior=stack[0].tree
          stack.pop(0)
          m=0
          
          for i in reversed(lista):
            symbol = node_stack(i, anterior)
            stack.insert(0, symbol)
          
          for i in lista:
            g=g+1
            
            dot.node(nods[g],i)
            
            dot.edges([anterior+nods[g]])
            
            stack[m].tree=nods[g]
            m=m+1
        else:
          stack.pop(0)
          laction.append('e')
          

        limput.append(jt())




dot.render('doctest-output/round-table.gv').replace('\\', '/')
'doctest-output/round-table.gv.pdf'


print(tabulate({'Stack': lstack, 'Imput': limput, 'Action': laction}, headers="keys", tablefmt='fancy_grid'))

  
