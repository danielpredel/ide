'''
componente      -> ( expresion ) | número | id | id inc_dec_op
inc_dec_op        -> ++ | --

o

sentencia       -> selección | iteración | repetición | sentIn | sentOut | asignación | in_dec_exp
inc_dec_exp     -> id inc_dec_op ;
inc_dec_op        -> ++ | --
'''
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
            # self.error()
            self.error_sintaxis(f'token -> {self.lexema}, se espera -> {expected_token}')
    
    def get_token(self):
        self.index += 1
        if self.index < len(self.analisis_lexico):
            self.token_actual = self.analisis_lexico[self.index]
            self.lineno = self.token_actual[3]
            self.lexema = self.token_actual[0]
            return self.token_actual[2]
        else:
            return 'ENDFILE'
    
    def get_lookahead(self):
        ahead_index = self.index + 1
        if ahead_index < len(self.analisis_lexico):
            lookahead = self.analisis_lexico[ahead_index]
            return lookahead[2]
        else:
            return 'ENDFILE'
        
    def error(self):
        error = f'\n>>> Error en linea {self.lineno}: token {self.token} -> {self.lexema}'
        # print(error)
        self.errores.append(error)
    
    def error_sintaxis(self, mensaje):
        error = f'\n>>> Error de sintaxis en la linea {self.lineno}: {mensaje}'
        # print(error)
        self.errores.append(error)

    def nuevo_nodo_main(self):
        main_node = Node()
        main_node.node_kind = ['MAIN','MAIN']
        main_node.name = 'main'
        return main_node

    def nuevo_nodo_exp(self, index):
        exp_kind = ['OPERADOR','CONSTANTE','IDENTIFICADOR']
        kind = exp_kind[index]
        exp_node = Node()
        exp_node.node_kind = ['EXPRESION',kind]
        exp_node.lineno = self.lineno
        exp_node.name = self.lexema
        return exp_node
    
    def nuevo_nodo_sent(self, index):
        sent_kind = ['SELECCION','ITERACION','REPETICION','IN','OUT','ASIGNACION']
        kind = sent_kind[index]
        sent_node = Node()
        sent_node.node_kind = ['SENTENCIA',kind]
        sent_node.lineno = self.lineno
        sent_node.name = self.lexema
        return sent_node
    
    def nuevo_nodo_declaracion_variable(self, index):
        exp_kind = ['INTEGER','DOUBLE']
        kind = exp_kind[index]
        exp_node = Node()
        exp_node.node_kind = ['DECLARACION_VARIABLE',kind]
        exp_node.lineno = self.lineno
        exp_node.name = self.lexema
        return exp_node
    
    def nuevo_nodo_lista_sentencias(self,index):
        exp_kind = ['THEN','ELSE']
        kind = exp_kind[index]
        exp_node = Node()
        exp_node.node_kind = ['LISTA_SENTENCIAS',kind]
        exp_node.lineno = self.lineno
        exp_node.name = kind.lower()
        return exp_node

    def nuevo_nodo_inc_dec(self,index):
        exp_kind = ['INCREMENTO','DECREMENTO']
        kind = exp_kind[index]
        exp_node = Node()
        exp_node.node_kind = ['EXPRESION',kind]
        exp_node.lineno = self.lineno
        if index == 0:
            exp_node.name = '+'
            exp_node.op = '+'
        else:
            exp_node.name = '-'
            exp_node.op = '-'
        
        id_child = Node()
        id_child.node_kind = ['EXPRESION','IDENTIFICADOR']
        id_child.lineno = self.lineno
        id_child.name = self.lexema
        exp_node.child[0] = id_child
        
        one_child = Node()
        one_child.node_kind = ['EXPRESION','CONSTANTE']
        one_child.lineno = self.lineno
        one_child.name = '1'
        one_child.val = 1
        exp_node.child[1] = one_child
        
        return exp_node

    def programa(self):
        self.match('MAIN')
        self.match('LLAVE_I')
        t = self.lista_declaracion()
        self.match('LLAVE_D')
        return t
    
    def lista_declaracion(self):
        t = self.nuevo_nodo_main()
        declaraciones = self.declaracion()
        
        if declaraciones != None:
            if len(declaraciones) > 1:
                t.child[0] = declaraciones.pop(0)
                t.siblings = declaraciones
            else:
                t.child[0] = declaraciones.pop(0)
        
        while self.token in ['INTEGER','DOUBLE','IF','WHILE','DO','CIN','COUT','IDENTIFICADOR']:
                t.siblings += self.declaracion()
        
        return t
    
    def declaracion(self):
        if self.token in ['INTEGER','DOUBLE']:
            t = [self.declaracion_variable()]
        elif self.token in ['IF','WHILE','DO','CIN','COUT','IDENTIFICADOR']:
            t = self.lista_sentencias(2)
        else:
            t = None
        return t
    
    def declaracion_variable(self):
        if self.token == 'INTEGER':
            t = self.nuevo_nodo_declaracion_variable(0)
            self.match(self.token)
        elif self.token == 'DOUBLE':
            t = self.nuevo_nodo_declaracion_variable(1)
            self.match(self.token)
        
        t.child[0], t.siblings = self.identificador()
        self.match('PUNTO_Y_COMA')
        return t
    
    def identificador(self):
        t = self.nuevo_nodo_exp(2)
        # print(f'Token: {self.token}, Lexema: {self.lexema}, t.name {t.name}')
        siblings = []
        self.match('IDENTIFICADOR')
        while self.token == 'COMA':
            self.match('COMA')
            siblings.append(self.nuevo_nodo_exp(2))
            self.match('IDENTIFICADOR')
        return t, siblings
    
    def lista_sentencias(self,tipo):
        t = None
        if tipo == 2:
            t = []
            while self.token in ['IF','WHILE','DO','CIN','COUT','IDENTIFICADOR']:
                t.append(self.sentencia())
        else:
            while self.token in ['IF','WHILE','DO','CIN','COUT','IDENTIFICADOR']:
                if t == None:
                    t = self.nuevo_nodo_lista_sentencias(tipo)
                    t.child[0] = self.sentencia()
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
            lookahead = self.get_lookahead()
            if lookahead == 'INCREMENTO':
                t = self.nuevo_nodo_inc_dec(0)
                self.match('IDENTIFICADOR')
                self.match('INCREMENTO')
                self.match('PUNTO_Y_COMA')
            elif lookahead == 'DECREMENTO':
                t = self.nuevo_nodo_inc_dec(1)
                self.match('IDENTIFICADOR')
                self.match('DECREMENTO')
                self.match('PUNTO_Y_COMA')
            else:
                t = self.asignacion()
        else:
            self.error_sintaxis(f'Token inesperado {self.token}: {self.lexema}')
            self.token = self.get_token()
        return t
    
    def asignacion(self):
        t = self.nuevo_nodo_exp(2)
        if t != None and self.token == 'IDENTIFICADOR':
            self.match('IDENTIFICADOR')
            p = self.nuevo_nodo_sent(5)
            p.child[0] = t
        self.match('ASIGNACION')
        if p != None:
            p.child[1] = self.sent_expresion()
        return p

    def sent_expresion(self):
        t = None
        if self.token != 'PUNTO_Y_COMA':
            t = self.expresion()
        self.match('PUNTO_Y_COMA')
        return t
    
    def seleccion(self):
        t = self.nuevo_nodo_sent(0)
        self.match('IF')
        self.match('PARENTESIS_I')
        if t != None:
            t.child[0] = self.expresion()
            self.match('PARENTESIS_D')
            self.match('LLAVE_I')
            t.child[1] = self.lista_sentencias(0)
            self.match('LLAVE_D')
        if self.token == 'ELSE':
            self.match('ELSE')
            self.match('LLAVE_I')
            t.child[2] = self.lista_sentencias(1)
            self.match('LLAVE_D')
        return t
    
    def iteracion(self):
        t = self.nuevo_nodo_sent(1)
        self.match('WHILE')
        self.match('PARENTESIS_I')
        if t != None:
            t.child[0] = self.expresion()
            self.match('PARENTESIS_D')
            self.match('LLAVE_I')
            t.child[1] = self.lista_sentencias(0)
            self.match('LLAVE_D')
        return t
    
    def repeticion(self):
        t = self.nuevo_nodo_sent(2)
        self.match('DO')
        self.match('LLAVE_I')
        if t != None:
            t.child[0] = self.lista_sentencias(0)
        self.match('LLAVE_D')
        self.match('WHILE')
        self.match('PARENTESIS_I')
        if t != None:
            t.child[1] = self.expresion()
        self.match('PARENTESIS_D')
        self.match('PUNTO_Y_COMA')
        return t
    
    def sent_in(self):
        t = self.nuevo_nodo_sent(3)
        self.match('CIN')
        if t != None and self.token == 'IDENTIFICADOR':
            p = self.nuevo_nodo_exp(2)
            t.child[0] = p
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
        t = self.expresion_relacional()
        if self.token in ['AND','OR']:
            p = self.nuevo_nodo_exp(0)
            if p != None:
                p.child[0] = t
                p.op = self.token
                t = p
            self.match(self.token)
            if t != None:
                t.child[1] = self.expresion_relacional()
        return t
    
    def expresion_relacional(self):
        t = self.expresion_simple()
        if self.token in ['MENOR','MENOR_IGUAL','MAYOR','MAYOR_IGUAL','DIFERENTE','IGUAL']:
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
        while self.token in ['SUMA','RESTA']:
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
        while self.token in ['MULTIPLICACION','DIVISION','MODULO']:
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
        while self.token == 'POTENCIA':
            p = self.nuevo_nodo_exp(0)
            if p != None:
                p.child[0] = t
                p.op = self.token
                t = p
                self.match(self.token)
                p.child[1] = self.componente()
        return t
    
    # def componente(self):
    #     t = None
    #     if self.token == 'PARENTESIS_I':
    #         self.match('PARENTESIS_I')
    #         t = self.expresion()
    #         self.match('PARENTESIS_D')
    #     elif self.token == 'ENTERO':
    #         t = self.nuevo_nodo_exp(1)
    #         if t != None and self.token == 'ENTERO':
    #             t.val = int(self.lexema)
    #         self.match('ENTERO')
    #     elif self.token == 'REAL':
    #         t = self.nuevo_nodo_exp(1)
    #         if t != None and self.token == 'REAL':
    #             t.val = float(self.lexema)
    #         self.match('REAL')
    #     elif self.token == 'ENTERO_NEG':
    #         t = self.nuevo_nodo_exp(1)
    #         if t != None and self.token == 'ENTERO_NEG':
    #             t.val = int(self.lexema)
    #         self.match('ENTERO_NEG')
    #     elif self.token == 'REAL_NEG':
    #         t = self.nuevo_nodo_exp(1)
    #         if t != None and self.token == 'REAL_NEG':
    #             t.val = float(self.lexema)
    #         self.match('REAL_NEG')
    #     elif self.token == 'IDENTIFICADOR':
    #         lookahead = self.get_lookahead()
    #         if lookahead == 'INCREMENTO':
    #             t = self.nuevo_nodo_inc_dec(0)
    #             self.match('IDENTIFICADOR')
    #             self.match('INCREMENTO')
    #         elif lookahead == 'DECREMENTO':
    #             t = self.nuevo_nodo_inc_dec(1)
    #             self.match('IDENTIFICADOR')
    #             self.match('DECREMENTO')
    #         else:
    #             t = self.nuevo_nodo_exp(2)
    #             self.match('IDENTIFICADOR')
    #     else:
    #         self.error_sintaxis(f'Token inesperado {self.token}: {self.lexema}')
    #         self.token = self.get_token()
    #     return t
    
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
        elif self.token == 'ENTERO_NEG':
            t = self.nuevo_nodo_exp(1)
            if t != None and self.token == 'ENTERO_NEG':
                t.val = int(self.lexema)
            self.match('ENTERO_NEG')
        elif self.token == 'REAL_NEG':
            t = self.nuevo_nodo_exp(1)
            if t != None and self.token == 'REAL_NEG':
                t.val = float(self.lexema)
            self.match('REAL_NEG')
        # Separar inc_dec
        elif self.token == 'IDENTIFICADOR':
            t = self.nuevo_nodo_exp(2)
            self.match('IDENTIFICADOR')
        else:
            self.error_sintaxis(f'Token inesperado {self.token}: {self.lexema}')
            self.token = self.get_token()
        return t
       
    def analisis_sintactico(self):
        return self.programa()
        
    def tree_to_json(self,root):
        # Agregar root y array
        diccionario = {
            'main': [root.to_dict()]
        }
        # diccionario = root.to_dict()
        
        json_tree = json.dumps(diccionario, indent=2)
        self.escribir_json(json_tree)

    def escribir_json(self,json_tree):
        parent_directory = os.path.dirname(__file__)
        dirname = 'analisis_sintactico'
        abs_dir = os.path.join(parent_directory,dirname)
        filename = 'tree.json'

        if os.path.isdir(abs_dir):
            abs_path = os.path.join(abs_dir,filename)
            with open(abs_path, 'w') as archivo:
                archivo.write(json_tree)
        else:
            try:
                os.mkdir(abs_dir)
                abs_path = os.path.join(abs_dir,filename)
                with open(abs_path, 'w') as archivo:
                    archivo.write(json_tree)
            except:
                print(f'Error al trabajar en el directorio: {abs_dir}')
                pass
    
    def get_errores(self):
        return self.errores