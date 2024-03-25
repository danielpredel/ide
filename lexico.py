import re

# Orden de la matriz de transicion:
# dig|letra| . | _ | ! | < | > | = | / | * | \n | + | - | % | ^ | ( | ) | { | } | , | ; | & | "|" | " " | \t | otro    
matriz = [
    ["2","5","e","6","7","8","8","8","9","D","0","1","13","D","D","D","D","D","D","D","D","D","D","0","0","e"],
    ["2","d","d","d","d","d","d","d","d","d","d","D","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],
    ["2","d","3","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],
    ["4","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E"],
    ["4","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],
    ["5","5","d","5","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],
    ["5","5","E","5","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E"],
    ["E","E","E","E","E","E","E","D","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E","E"],
    ["d","d","d","d","d","d","d","D","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],
    ["d","d","d","d","d","d","d","d","10","11","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d","d"],
    ["10","10","10","10","10","10","10","10","10","10","D","10","10","10","10","10","10","10","10","10","10","10","10","10","10","10"],
    ["11","11","11","11","11","11","11","11","11","12","11","11","11","11","11","11","11","11","11","11","11","11","11","11","11","11"],
    ["11","11","11","11","11","11","11","11","D","12","11","11","11","11","11","11","11","11","11","11","11","11","11","11","11","11"],
    ["2","d","d","d","d","d","d","d","d","d","d","d","D","d","d","d","d","d","d","d","d","d","d","d","d","d"]
]

tokens = ["NUMERO","IDENTIFICADOR","PALABRA_RESERVADA","OP_ARITMETICO","OP_RELACIONAL","OP_LOGICO","SIMBOLO",
          "ASIGNACION","INCREMENTO","DECREMENTO"]

palabras_reservadas = ["if","else","do","while","switch","case","integer","double","main","cin","cout"]

def analizador_lexico(codigo):
    codigo += '\n'
    buffer = ''
    lexema = ''
    analisis = []
    estado = 0
    col_archivo = 1
    row_archivo = 1
    index = 0
    col = 0
    row = 0
    
    while index < len(codigo):
        if buffer == '':
            caracter = codigo[index]
            index += 1
            col_archivo += 1
            
            col = get_col(caracter)
            if col == 10:
                row_archivo += 1
                col_archivo = 1
        else:
            caracter = buffer
            buffer = ''
        
        row = int(estado)
        estado = matriz[row][col]
        
        if estado.isdigit():
            if int(estado) > 0:
                lexema += caracter
        elif estado == "D":
            lexema += caracter
            if row == 0:
                if col < 15:
                    analisis.append([lexema,tokens[3]])
                elif col >= 15 and col <= 20:
                    analisis.append([lexema,tokens[6]])
                else:
                    analisis.append([lexema,tokens[5]])
            elif row == 1:
                analisis.append([lexema,tokens[8]])
            elif row == 7 or row == 8:
                analisis.append([lexema,tokens[4]])
            elif row == 13:
                analisis.append([lexema,tokens[9]])
            lexema = ''
            estado = 0
        elif estado == "d":
            buffer = caracter
            if row == 1 or row == 9 or row == 13:
                analisis.append([lexema,tokens[3]])
            elif row == 2:
                analisis.append([lexema,tokens[0]])
            elif row == 4:
                analisis.append([lexema,tokens[0]])
            elif row == 5:
                if lexema in palabras_reservadas:
                    analisis.append([lexema,tokens[2]])
                else:
                    analisis.append([lexema,tokens[1]])
            elif row == 8:
                if lexema == "=":
                    analisis.append([lexema,tokens[7]])
                else:
                    analisis.append([lexema,tokens[4]])
            lexema = ''
            estado = 0
        elif estado == "e":
            print(f'Error en la linea {row_archivo}, columna {col_archivo - 1}')
            estado = 0
        elif estado == "E":
            print(f'Error en la linea {row_archivo}, columna {col_archivo - 1}')
            lexema = lexema[:-1]
            if lexema:
                analisis.append([lexema,tokens[0]])
                lexema = ''
            buffer = caracter
            estado = 0
    
    return analisis

def get_col(c):
    simbolos_p1 = [".","_","!","<",">","=","/","*"]
    simbolos_p2 = ["+","-","%","^","(",")","{","}",",",";","&","|"," "]
    
    cod_ascii = ord(c)
    if cod_ascii >= 48 and cod_ascii <= 57:
        return 0
    
    if c.isalpha():
        return 1
    
    try:
        col = simbolos_p1.index(c) + 2
    except:
        pass
    else:
        return col
    
    if re.search("\n",c):
        return 10
    
    try:
        col = simbolos_p2.index(c) + 11
    except:
        pass
    else:
        return col
    
    if re.search("\t",c):
        return 24
    return 25

# codigo = """//inicio del codigo
# var = 12.12;

# if(var >= 10){
#     mayus();
# }
# else {
#     minus();  
# }

# my_id = 12345.

# _ = error

# int an@lizador

# var = 123
# var++
# var--

# /*
# comentario 
# multilinea
# ****/

# if (!true){
#     exit()
# }"""

codigo = """main sum@r 3.14+main)if{32.algo
34.34.34.34
{
int x,y,z;
real a,b,c;
 suma=45;
x=32.32;
x=23;
y=2+3-1;
z=y+7;
y=y+1;
a=24.0+4-1/3*2+34-1;
x=(5-3)*(8/2);
y=5+3-2*4/7-9;
z=8/2+15*4;
y=14.54;
if(2>3)then
        y=a+3;
  else
      if(4>2 & )then
             b=3.2;
       else
           b=5.0;
       end;
       y=y+1;
end;
a+

+;
c--;
x=3+4;
do
   y=(y+1)*2+1;
   while(x>7){x=6+8/9*8/3;   
    cin x; 
   mas=36/7; 
   };

 until(y=


=



5);
 while(y==0){
    cin mas;
    cout x;
};
}"""

analisis = analizador_lexico(codigo)
for lexema in analisis:
    print(f"{lexema[0]}\t{lexema[1]}")