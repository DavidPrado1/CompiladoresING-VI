import pandas as pd
from tabulate import tabulate
import graphviz
from AnalizadorLexico import tokensLexer as tokens

dot = graphviz.Digraph(comment='The Round Table')

counter = 0
syntax_table = pd.read_csv("d3.csv", index_col=0)

class node_stack:
  def __init__(self, value, lex,line, terminal, tree):
    self.value = value
    self.lex = lex
    self.line = line
    self.terminal = terminal
    self.tree = tree # boolean

class nodo():
  
  def __init__(self,dato,
               children=[],
               father=None
               ):
    global counter
    self.children = children
    self.father = father
    self.dato = dato
    self.id = str(counter) + 'a'
    counter+=1

  def insert_arbol(self, val):
    self.children.insert(0,val)

def r_imprimir(nodoactual):
  dot.node(nodoactual.id,nodoactual.dato.value+'\n'+str(nodoactual.dato.lex))
  if(len(nodoactual.children)==0):
    return 0
  else:
    for i in nodoactual.children:
      print(i.dato.value,i.id,i.father,i.dato.terminal,i.dato.lex,i.dato.line)
      dot.node(i.id,i.dato.value+'\n'+str(i.dato.lex))

      dot.edge(i.father,i.id)
      r_imprimir(i)

stack = []
symbol_1 = node_stack('$','',0,True,'')
symbol_2 = node_stack('Program','',0,False,counter)
stack.insert(0, symbol_1)
stack.insert(0, symbol_2)

root = nodo(symbol_2,[],None)
actualn=root
def buscar(nodo,id):
  global actualn
  if(nodo.id==id):
    actualn=nodo
  else:
    for i in nodo.children:
      buscar(i,id)

def js():
  inp = ''
  iter=0
  for i in stack:
    inp = inp + ' ' + stack[iter].value
    iter=iter+1
  return inp
  
for i in tokens:
  print(i)
def jt():
  inp = ''
  iter=0
  for i in tokens:
    inp = inp + ' ' + tokens[iter]['type']
    iter=iter+1
  return inp


lstack=[]
limput=[]
laction=[]

stack[0].tree=root.id

def check_syntax_table():
  test = syntax_table.loc[stack[0].value][tokens[0]['type']]
  if str(test) == 'nan':
    return False
  return True
  

while True:
  #print("Stack",js())
  if stack[0].value == '$' and tokens[0]['type'] == '$':
    break
  else:
    if stack[0].value == tokens[0]['type']:
      stack[0].terminal = True
      stack[0].lex = tokens[0]['lexeme']
      stack[0].line = tokens[0]['line']
      #print('Action','terminal')
      #print("Imput",jt())
      stack.pop(0)
      tokens.pop(0)
    else:
      if not check_syntax_table():
        print("Error Sintactico")
        exit(1)
      if syntax_table.loc[stack[0].value][tokens[0]['type']] == 'no':
        #print("Imput",jt())
        print("Error Sintactico")
        exit(1)
      else:
        if (syntax_table.loc[stack[0].value][tokens[0]['type']] != 'e'):
          #print('Action',syntax_table.loc[stack[0].value][tokens[0]['type']])
          lista = syntax_table.loc[stack[0].value][tokens[0]['type']].split()
          anterior=stack[0].tree
          stack.pop(0)
          
          for i in reversed(lista):
            symbol = node_stack(i,'','',False,'no')
            new=nodo(dato=symbol,children=[],father=anterior)
            symbol.tree=new.id
            stack.insert(0, symbol)
            buscar(root, anterior)
            actualn.insert_arbol(new)
        
        else:
          stack.pop(0)
          #print('Action','e')
          

        #print('Input',jt())
  #print('\n')

print(tokens)
r_imprimir(root)

dot.render('doctest-output/round-table.gv').replace('\\', '/')
'doctest-output/round-table.gv.pdf'

#print(tabulate({'Stack': lstack, 'Imput': limput, 'Action': laction}, headers="keys", tablefmt='fancy_grid'))

def print_tabla(tabla):
  print("\n"+"Tabla:")
  for i in tabla:
    print(i)


funcd=["FuncDeclaration","VoidDeclaration","MainClass"]
tabla=[]

      
def buscardecl(nombre,nodo,variables):
  if(nodo.dato.value == "Declaration1"):
    a={
    'token': "Parametro",
    'lexeme': nodo.children[1].dato.lex,
    'line': nodo.children[1].dato.line,
    'func' : nombre
    }
    
    variables.append(a)
    node = nodo.children[2]
    while(len(node.children)!=0):
      b={
    'token': "Parametro",
    'lexeme': node.children[2].dato.lex,
    'line': node.children[2].dato.line,
    'func' : nombre
    }
      
      variables.append(b)
      node = node.children[3]
  elif(nodo.dato.value == "Statement1"):
    a={
    'token': "Declaracion de Variable",
    'lexeme': nodo.children[1].dato.lex,
    'line': nodo.children[1].dato.line,
    'func' : nombre
    }
    for i in variables:
      if(i['lexeme']==nodo.children[1].dato.lex):
        print("ERROR: variable", a['lexeme'] , "ya declarada")
        exit(1)

    variables.append(a)
    if ( nodo.children[3].children[0].dato.value == "ID"):
      b=nodo.children[3]
      a={
        'token': "Uso de Variable",
        'lexeme': b.children[0].dato.lex,
        'line': b.children[0].dato.line,
        'func' : nombre
      }
      comp=1
      for i in variables:
        if (i['lexeme']==b.children[0].dato.lex):
          comp=0
      if comp == 1:
        print("ERROR: variable", a['lexeme'] , "no declarada")
        exit(1)
        
      variables.append(a)
  elif(nodo.dato.value == "Statement2"):
    a={
    'token': "Uso de Variable",
    'lexeme': nodo.children[0].dato.lex,
    'line': nodo.children[0].dato.line,
    'func' : nombre
    }
    comp=1
    for i in variables:
      if (i['lexeme']==nodo.children[0].dato.lex):
        comp=0
    if comp == 1:
      print("ERROR: variable", a['lexeme'] , "no declarada")
      exit(1)
      
    variables.append(a)
    if ( nodo.children[2].children[0].dato.value == "ID"):
      b=nodo.children[2]
      a={
        'token': "Uso de Variable",
        'lexeme': b.children[0].dato.lex,
        'line': b.children[0].dato.line,
        'func' : nombre
      }
      comp=1
      for i in variables:
        if (i['lexeme']==b.children[0].dato.lex):
          comp=0
      if comp == 1:
        print("ERROR: variable", a['lexeme'] , "no declarada")
        exit(1)
        
      variables.append(a)
  elif(nodo.dato.value == "Comparasion"): #ddd
    if ( nodo.children[0].children[0].dato.value == "ID"):
      b=nodo.children[0]
      a={
        'token': "Uso de Variable",
        'lexeme': b.children[0].dato.lex,
        'line': b.children[0].dato.line,
        'func' : nombre
      }
      comp=1
      for i in variables:
        if (i['lexeme']==b.children[0].dato.lex):
          comp=0
      if comp == 1:
        print("ERROR: variable", a['lexeme'] , "no declarada")
        exit(1)
        
      variables.append(a)
    if ( nodo.children[2].children[0].dato.value == "ID"):
      b=nodo.children[2]
      a={
        'token': "Uso de Variable",
        'lexeme': b.children[0].dato.lex,
        'line': b.children[0].dato.line,
        'func' : nombre
      }
      comp=1
      for i in variables:
        if (i['lexeme']==b.children[0].dato.lex):
          comp=0
      if comp == 1:
        print("ERROR: variable", a['lexeme'] , "no declarada")
        exit(1)
        
      variables.append(a)
  elif(nodo.dato.value == "Parameter1"): #ddd
    if ( nodo.children[0].children[0].dato.value == "ID"):
      b=nodo.children[0]
      a={
        'token': "Uso de Variable",
        'lexeme': b.children[0].dato.lex,
        'line': b.children[0].dato.line,
        'func' : nombre
      }
      comp=1
      for i in variables:
        if (i['lexeme']==b.children[0].dato.lex):
          comp=0
      if comp == 1:
        print("ERROR: variable", a['lexeme'] , "no declarada")
        exit(1)
        
      variables.append(a)
  elif(nodo.dato.value == "Parameter2"): #ddd
    if ( nodo.children[1].children[0].dato.value == "ID"):
      b=nodo.children[1]
      a={
        'token': "Uso de Variable",
        'lexeme': b.children[0].dato.lex,
        'line': b.children[0].dato.line,
        'func' : nombre
      }
      comp=1
      for i in variables:
        if (i['lexeme']==b.children[0].dato.lex):
          comp=0
      if comp == 1:
        print("ERROR: variable", a['lexeme'] , "no declarada")
        exit(1)
        
      variables.append(a)
  elif(nodo.dato.value == "Call"):
    a={
    'token': "Llamada a funcion",
    'lexeme': nodo.children[1].dato.lex,
    'line': nodo.children[1].dato.line,
    'func' : nombre
    }
    comp=1
    for i in tabla:
      if (i['lexeme']==nodo.children[1].dato.lex):
        comp=0
    if comp == 1:
      print("ERROR: variable", a['lexeme'] , "no declarada")
      exit(1)
    variables.append(a)
    if(len(nodo.children[3].children)!=0):
      h = nodo.children[3].children[0]
      a1={
    'token': "Parametro",
    'lexeme': h.children[0].dato.lex,
    'line': h.children[0].dato.line,
    'func' : nombre
      }
      comp=1
      for i in variables:
        if (i['lexeme']==h.children[0].dato.lex):
          comp=0
      if comp == 1:
        print("ERROR: variable", a['lexeme'] , "no declarada")
        exit(1)
        
      variables.append(a1)
      node1 = nodo.children[3].children[1]
      while(len(node1.children)!=0):
        b={
      'token': "Parametro",
      'lexeme': node1.children[1].children[0].dato.lex,
      'line': node1.children[1].children[0].dato.line,
      'func' : nombre
      }
        comp=1
        for i in variables:
          if (i['lexeme']==node1.children[1].children[0].dato.lex):
            comp=0
        if comp == 1:
          print("ERROR: variable", b['lexeme'] , "no declarada")
          exit(1)
        variables.append(b)
        node1 = node1.children[2]
  elif(nodo.dato.value == "Oper1"):
    if ( nodo.children[0].dato.value == "ID"):
      a={
        'token': "Uso de Variable",
        'lexeme': nodo.children[0].dato.lex,
        'line': nodo.children[0].dato.line,
        'func' : nombre
      }
      comp=1
      for i in variables:
        if (i['lexeme']==nodo.children[0].dato.lex):
          comp=0
      if comp == 1:
        print("ERROR: variable", a['lexeme'] , "no declarada")
        exit(1)
      variables.append(a)
    elif(nodo.children[0].dato.value == "Operation"):
      for i in nodo.children[0].children:
        buscardecl(nombre,i, variables)
  elif(nodo.dato.value == "Oper2"):
    if ( nodo.children[0].dato.value == "ID"):
      a={
        'token': "Uso de Variable",
        'lexeme': nodo.children[0].dato.lex,
        'line': nodo.children[0].dato.line,
        'func' : nombre
      }
      comp=1
      for i in variables:
        if (i['lexeme']==nodo.children[0].dato.lex):
          comp=0
      if comp == 1:
        print("ERROR: variable", a['lexeme'] , "no declarada")
        exit(1)
      variables.append(a)
    elif(nodo.children[0].dato.value == "Operation"):
      for i in nodo.children[0].children:
        buscardecl(nombre,i, variables)
  else:
    for i in nodo.children:
      buscardecl(nombre,i, variables)


def buscarfunc(nodo):
  if(nodo.dato.value in funcd):
    if(nodo.dato.value == funcd[0] or nodo.dato.value == funcd[1]):
      val =""
      if(nodo.dato.value == funcd[0]):
        val = "Funcion"
      else:
        val = "Void"
      a={
    'token': val,
    'lexeme': nodo.children[1].dato.lex,
    'line': nodo.children[1].dato.line,
    'func' : "Program"
    }
      tabla.append(a)
      print_tabla(tabla)
      variablesd=[]
      buscardecl(nodo.children[1].dato.lex,nodo,variablesd)
      for i in variablesd:
        tabla.append(i)
        print_tabla(tabla)
      if(nodo.dato.value == funcd[0]):
        if(nodo.children[10].children[0].dato.value=="ID"):
          p={
            'token': "Return",
            'lexeme': nodo.children[10].children[0].dato.lex,
            'line': nodo.children[10].children[0].dato.line,
            'func' : nodo.children[1].dato.lex
          }
          comp2=1
          print(p)
          for j in variablesd:
            if (j['lexeme']==p['lexeme']):
              comp2=0
          if comp2 == 1:
            print("ERROR: variable", p['lexeme'] , "no declarada")
            exit(1)
              
          tabla.append(p)
          print_tabla(tabla)
          tabla.pop()
      for i in range(len(variablesd)):
        tabla.pop()
      print_tabla(tabla)
    elif(nodo.dato.value == funcd[2]):
      a={
    'token': "Main",
    'lexeme': nodo.children[0].dato.lex,
    'line': nodo.children[0].dato.line,
    'func' : "Program"
    }
      tabla.append(a)
      variablesd=[]
      print_tabla(tabla)
      buscardecl(nodo.children[0].dato.lex,nodo,variablesd)
      for i in variablesd:
        tabla.append(i)
        print_tabla(tabla)
      for i in range(len(variablesd)):
        tabla.pop()
      print_tabla(tabla)
    

  
  else:
    for i in nodo.children:
      buscarfunc(i)

buscarfunc(root)


