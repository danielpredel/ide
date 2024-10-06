class Node:
    def __init__(self) -> None:
        # usar lexema
        # Datos reales
        self.child = [None,None,None]
        self.siblings = []
        self.lineno = None
        
        # node_kind:
        # 0 (Tipos de Nodo): MAIN | EXPRESION | SENTENCIA | DECLARACION
        # 1 (Tipos de exp):  OPERADOR | CONSTANTE | IDENTIFICADOR
        # 1 (Tipos de sent): SELECCION | ITERACION | REPETICION | IN | OUT | ASIGNACION
        # 1 (Tipos de dec):  INTEGER | DOUBLE
        self.node_kind = [None, None]
        
        # Lexema
        # Datos a mostrar en el arbol
        self.name = None
        self.op = None
        self.val = None
        
        # INTEGER, DOUBLE, VOID, BOOLEAN
        self.exp_type = None
    
    def preorden(self):
        print(self.name)
        for node in self.child:
            if node == None:
                break
            else:
                node.preorden()
    
    def to_dict(self):
        res = {
            "name": self.name
        }
        
        if self.node_kind[0] == 'EXPRESION':
            res["attributes"] = [{"type": str(self.exp_type), "value": str(self.val)}]
        
        if self.node_kind[0] == 'DECLARACION':
            res["attributes"] = [{"type": str(self.exp_type)}]
            
        children = []
        siblings = []
        
        for node in self.child:
            if node == None:
                break
            else:
                children.append(node.to_dict())
        
        for node in self.siblings:
            siblings.append(node.to_dict())
        
        if children != []:
            res["children"] = children
        
        if siblings != []:
            res["siblings"] = siblings
        
        return res