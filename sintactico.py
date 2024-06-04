"""
expresionSimple -> expresiónSimple sumaOp termino | termino
sumaOp          -> + | -
termino         -> termino multOp factor | factor
multOp          -> * | / |%
factor          -> factor potOp componente | componente
potOp           -> ^
componente      -> componente incDecOp | ( expresión ) | número | id
incDecOp        -> ++ | --  
"""
import json
import os
from node import Node

class AnalizadorSintactico:
    def __init__(self, analisis_lexico) -> None:
        self.analisis_lexico = analisis_lexico
        self.index = 0
        
        # Toda la informacion: lexema, token, subtoken, linea, col_i. col_f
        self.token_actual = self.analisis_lexico[self.index]
        
        # Solo el subtoken
        self.lexema = self.token_actual[0]
        self.token = self.token_actual[2]
        self.lineno = self.token_actual[3]
        
        self.errores = []
    
    def match(self, expected_token):
        # print(f'{self.token}:{expected_token}')
        if self.token == expected_token:
            self.token = self.get_token()
        else:
            self.error()
    
    def get_token(self):
        self.index += 1
        if self.index < len(self.analisis_lexico):
            self.token_actual = self.analisis_lexico[self.index]
            self.lineno = self.token_actual[3]
            self.lexema = self.token_actual[0]
            return self.token_actual[2]
        else:
            return 'ENDFILE'
    
    def error(self):
        print(f'\n>>> Error en linea {self.lineno}: token {self.token} -> {self.lexema}')
        exit()
    
    def error_sintaxis(self, mensaje):
        error = f'\n>>> Error de sintaxis en la linea {self.lineno}: {mensaje}'
        print(error)
        self.errores.append(error)

    def nuevo_nodo_exp(self, index):
        exp_kind = ["OP","CONST","IDENTIFICADOR"]
        kind = exp_kind[index]
        exp_node = Node()
        exp_node.node_kind = ['EXPRESION',kind]
        exp_node.lineno = self.lineno
        exp_node.name = self.lexema
        return exp_node
    
    def nuevo_nodo_sent(self, index):
        sent_kind = ["SELECCION","ITERACION","REPETICION","IN","OUT","ASIGNACION"]
        kind = sent_kind[index]
        sent_node = Node()
        sent_node.lineno = self.lineno
        sent_node.name = self.lexema
        sent_node.node_kind = ['SENTENCIA',kind]
        return sent_node
    
    def programa(self):
        self.match('MAIN')
        self.match('LLAVE_I')
        t = self.lista_declaracion()
        self.match('LLAVE_D')
        return t
    
    def lista_declaracion(self):
        t = self.declaracion()
        while self.token in ['INTEGER','DOUBLE','IF','WHILE','DO','CIN','COUT','ASIGNACION']:
            t.siblings.append(self.declaracion())
        return t
        
        # t = self.declaracion()
        # p = t
        # while self.token in ['INTEGER','DOUBLE','IF','WHILE','DO','CIN','COUT','ASIGNACION']:
        #     q = self.declaracion()
        #     if q != None:
        #         if t == None:
        #             t = p
        #             p = q
        #         else:
        #             p.sibling = q
        #             p = q
        # return t
    
    def declaracion(self):
        if self.token in ['INTEGER','DOUBLE']:
            t = self.declaracion_variable()
        elif self.token in ['IF','WHILE','DO','CIN','COUT','ASIGNACION']:
            t = self.lista_sentencias()
        else:
            t = None
        return t
    
    def declaracion_variable(self):
        if self.token in ['INTEGER','DOUBLE']:
            self.match(self.token)
        t = self.identificador()
        self.match('PUNTO_Y_COMA')
        return t
    
    def identificador(self):
        t = self.nuevo_nodo_exp(2)
        self.match('IDENTIFICADOR')
        while self.token == 'COMA':
            self.match('COMA')
            t.siblings.append(self.nuevo_nodo_exp(2))
            self.match('IDENTIFICADOR')
        return t
    
    def lista_sentencias(self):
        # La forma de implementar los nodos sibling sera con un array
        t = None
        while self.token in ["IF","WHILE","DO","CIN","COUT","IDENTIFICADOR"]:
            if t == None:
                t = self.sentencia()
            else:
                t.siblings.append(self.sentencia())
        return t
    
    def sentencia(self):
        t = None
        if self.token == 'IF':
            t = self.seleccion()
        elif self.token == 'WHILE':
            t = self.iteracion()
        elif self.token == 'DO':
            t = self.repeticion()
        elif self.token == 'CIN':
            t = self.sent_in()
        elif self.token == 'COUT':
            t = self.sent_out()
        elif self.token == 'IDENTIFICADOR':
            t = self.asignacion()
        else:
            self.error_sintaxis(f'Token inesperado {self.token}: {self.lexema}')
            self.token = self.get_token()
        return t
    
    def asignacion(self):
        # v1 con hijo, mi consideracion
        # t = self.nuevo_nodo_sent(5)
        # if t != None and self.token == 'IDENTIFICADOR':
        #     p = self.nuevo_nodo_exp(2)
        #     t.child[0] = p
        # self.match('IDENTIFICADOR')
        # self.match('ASIGNACION')
        # if t != None:
        #     t.child[1] = self.expresion()
        # return t
        
        # v2 sin hijo, implementacion tiny
        t = self.nuevo_nodo_sent(5)
        # if t != None and self.token == 'IDENTIFICADOR':
        #     t.name = self.lexema
        self.match('IDENTIFICADOR')
        self.match('ASIGNACION')
        if t != None:
            t.child[0] = self.sent_expresion()
        return t

    def sent_expresion(self):
        t = None
        if self.token != 'PUNTO_Y_COMA':
            t = self.expresion()
        self.match('PUNTO_Y_COMA')
        return t
    
    def seleccion(self):
        t = self.nuevo_nodo_sent(0)
        self.match('IF')
        if t != None:
            t.child[0] = self.expresion()
            t.child[1] = self.lista_sentencias()
        if self.token == 'ELSE':
            self.match('ELSE')
            t.child[2] = self.lista_sentencias()
        self.match('END')
        return t
    
    def iteracion(self):
        t = self.nuevo_nodo_sent(1)
        self.match('WHILE')
        if t != None:
            t.child[0] = self.expresion()
        if t != None:
            t.child[1] = self.lista_sentencias()
        self.match('END')
        return t
    
    def repeticion(self):
        t = self.nuevo_nodo_sent(2)
        self.match('DO')
        if t != None:
            t.child[0] = self.lista_sentencias()
        self.match('WHILE')
        if t != None:
            t.child[1] = self.expresion()
        return t
    
    def sent_in(self):
        # v1 con hijo, mi consideracion
        # t = self.nuevo_nodo_sent(3)
        # self.match('CIN')
        # if t != None and self.token == 'IDENTIFICADOR':
        #     p = self.nuevo_nodo_exp(2)
        #     t.child[0] = p
        # self.match('IDENTIFICADOR')
        # self.match('PUNTO_Y_COMA')
        # return t
        
        # v2 sin hijos, implementacion tiny
        t = self.nuevo_nodo_sent(3)
        self.match('CIN')
        if t != None and self.token == 'IDENTIFICADOR':
            t.name = self.lexema
        self.match('IDENTIFICADOR')
        self.match('PUNTO_Y_COMA')
        return t
    
    def sent_out(self):
        t = self.nuevo_nodo_sent(4)
        self.match('COUT')
        if t != None:
            t.child[0] = self.expresion()
        self.match('PUNTO_Y_COMA')
        return t
    
    def expresion(self):
        t = self.expresion_simple()
        if self.token in ["MENOR","MENOR_IGUAL","MAYOR","MAYOR_IGUAL","DIFERENTE","IGUAL"]:
            p = self.nuevo_nodo_exp(0)
            if p != None:
                p.child[0] = t
                p.op = self.token
                t = p
            self.match(self.token)
            if t != None:
                t.child[1] = self.expresion_simple()
        return t
    
    def expresion_simple(self):
        t = self.termino()
        while self.token in ["SUMA","RESTA"]:
            p = self.nuevo_nodo_exp(0)
            if p != None:
                p.child[0] = t
                p.op = self.token
                t = p
                self.match(self.token)
                p.child[1] = self.termino()
        return t
    
    def termino(self):
        t = self.factor()
        while self.token in ["MULTIPLICACION","DIVISION","MODULO"]:
            p = self.nuevo_nodo_exp(0)
            if p != None:
                p.child[0] = t
                p.op = self.token
                t = p
                self.match(self.token)
                p.child[1] = self.factor()
        return t
    
    def factor(self):
        t = self.componente()
        while self.token == "POTENCIA":
            p = self.nuevo_nodo_exp(0)
            if p != None:
                p.child[0] = t
                p.op = self.token
                t = p
                self.match(self.token)
                p.child[1] = self.componente()
        return t
    
    def componente(self):
        t = None
        if self.token == 'PARENTESIS_I':
            self.match('PARENTESIS_I')
            t = self.expresion()
            self.match('PARENTESIS_D')
        elif self.token == 'ENTERO':
            t = self.nuevo_nodo_exp(1)
            if t != None and self.token == 'ENTERO':
                t.val = int(self.lexema)
            self.match('ENTERO')
        elif self.token == 'REAL':
            t = self.nuevo_nodo_exp(1)
            if t != None and self.token == 'REAL':
                t.val = float(self.lexema)
            self.match('REAL')
        elif self.token == 'IDENTIFICADOR':
            t = self.nuevo_nodo_exp(2)
            # if t != None and self.token == 'IDENTIFICADOR':
            #     t.name = self.lexema
            self.match('IDENTIFICADOR')
        else:
            self.error_sintaxis(f'Token inesperado {self.token}: {self.lexema}')
            self.token = self.get_token()
        return t
    
    def analisis_sintactico(self):
        return self.programa()
    
    def arbol_prueba(self):
        root = Node()
        root.name = "Root"
        
        hijo1 = Node()
        hijo1.name = "Hijo 1"
        hijo2 = Node()
        hijo2.name = "Hijo 2"
        hijo3 = Node()
        hijo3.name = "Hijo 3"
        hijo2.child[0] = hijo3
        hijo1.child[0] = hijo2
        
        hijo4 = Node()
        hijo4.name = "Hijo 4"
        hijo5 = Node()
        hijo5.name = "Hijo 5"
        hijo6 = Node()
        hijo4.child[0] = hijo5
        
        
        hijo6.name = "Hijo 6"
        hijo7 = Node()
        hijo7.name = "Hijo 7"
        hijo8 = Node()
        hijo8.name = "Hijo 8"
        hijo6.child[0] = hijo7
        hijo6.child[1] = hijo8
        
        root.child[0] = hijo1
        root.child[1] = hijo4
        root.child[2] = hijo6
        
        self.tree_to_json(root)
        
    def tree_to_json(self,root):
        diccionario = root.to_dict()
        json_tree = json.dumps(diccionario, indent=2)
        self.escribir_json(json_tree)

    def escribir_json(self,json_tree):
        parent_directory = os.path.dirname(__file__)
        dirname = 'analisis_sintactico'
        abs_dir = os.path.join(parent_directory,dirname)
        filename = 'tree.json'

        if os.path.isdir(abs_dir):
            abs_path = os.path.join(abs_dir,filename)
            with open(abs_path, "w") as archivo:
                archivo.write(json_tree)
        else:
            try:
                os.mkdir(abs_dir)
                abs_path = os.path.join(abs_dir,filename)
                with open(abs_path, "w") as archivo:
                    archivo.write(json_tree)
            except:
                print(f'Error al trabajar en el directorio: {abs_dir}')
                pass