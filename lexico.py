import os
import sys
import re
from matriz_transicion import matriz
from tokens import *
from tabulate import tabulate

def analizador_lexico(codigo):
    codigo += '\n'
    buffer = ''
    lexema = ''
    analisis = []
    errores = []
    comentarios = []
    fila_comentario = 0
    col_comentario = 1
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
            col = get_col(caracter)
        else:
            caracter = buffer
            buffer = ''
        
        row = int(estado)
        estado = matriz[row][col]
        
        if estado.isdigit():
            if int(estado) > 0:
                lexema += caracter
                col_archivo += 1
                if row == 9:
                    fila_comentario = row_archivo
                    col_comentario = col_archivo - 2
                elif (row == 11 or row == 12) and col == 10:
                    row_archivo += 1
                    col_archivo = 1
            else:
                col_archivo += 1
                if col == 10:
                    row_archivo += 1
                    col_archivo = 1
        elif estado == "D":
            lexema += caracter
            if row == 0:
                if col == 9:
                    analisis.append([lexema,tokens[3],sub_tokens[15],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
                if col == 13:
                    analisis.append([lexema,tokens[3],sub_tokens[17],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
                if col == 14:
                    analisis.append([lexema,tokens[3],sub_tokens[18],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
                if col == 15:
                    analisis.append([lexema,tokens[6],sub_tokens[27],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
                if col == 16:
                    analisis.append([lexema,tokens[6],sub_tokens[28],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
                if col == 17:
                    analisis.append([lexema,tokens[6],sub_tokens[29],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
                if col == 18:
                    analisis.append([lexema,tokens[6],sub_tokens[30],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
                if col == 19:
                    analisis.append([lexema,tokens[6],sub_tokens[31],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
                if col == 20:
                    analisis.append([lexema,tokens[6],sub_tokens[32],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
                if col == 21:
                    analisis.append([lexema,tokens[5],sub_tokens[25],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
                if col == 22:
                    analisis.append([lexema,tokens[5],sub_tokens[26],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
            elif row == 1:
                analisis.append([lexema,tokens[3],sub_tokens[33],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
            elif row == 7:
                analisis.append([lexema,tokens[4],sub_tokens[23],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
            elif row == 8:
                analisis.append([lexema,tokens[4],sub_tokens[24],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
            elif row == 10:
                comentarios.append(['L',row_archivo,row_archivo,col_comentario,col_archivo])
                row_archivo += 1
                col_archivo = 0
            elif row == 12:
                comentarios.append(['M',fila_comentario,row_archivo,col_comentario,col_archivo+1])
            elif row == 13:
                analisis.append([lexema,tokens[3],sub_tokens[34],row_archivo,col_archivo-len(lexema)+1,col_archivo+1])
            col_archivo += 1
            lexema = ''
            estado = 0
        elif estado == "d":
            buffer = caracter
            if row == 1:
                analisis.append([lexema,tokens[3],sub_tokens[13],row_archivo,col_archivo-len(lexema),col_archivo])
            elif row == 2:
                analisis.append([lexema,tokens[0],sub_tokens[0],row_archivo,col_archivo-len(lexema),col_archivo])
            elif row == 4:
                analisis.append([lexema,tokens[0],sub_tokens[1],row_archivo,col_archivo-len(lexema),col_archivo])
            elif row == 5:
                if lexema in palabras_reservadas:
                    analisis.append([lexema,tokens[2],lexema.upper(),row_archivo,col_archivo-len(lexema),col_archivo])
                else:
                    analisis.append([lexema,tokens[1],tokens[1],row_archivo,col_archivo-len(lexema),col_archivo])
            elif row == 8:
                if lexema == "=":
                    analisis.append([lexema,tokens[7],tokens[7],row_archivo,col_archivo-len(lexema),col_archivo])
                elif lexema == "<":
                    analisis.append([lexema,tokens[4],sub_tokens[19],row_archivo,col_archivo-len(lexema),col_archivo])
                elif lexema == ">":
                    analisis.append([lexema,tokens[4],sub_tokens[21],row_archivo,col_archivo-len(lexema),col_archivo])
            if row == 9:
                analisis.append([lexema,tokens[3],sub_tokens[16],row_archivo,col_archivo-len(lexema),col_archivo])
            if row == 13:
                analisis.append([lexema,tokens[3],sub_tokens[14],row_archivo,col_archivo-len(lexema),col_archivo])
            lexema = ''
            estado = 0
        elif estado == "e":
            col_archivo += 1
            errores.append(f'Error en la linea {row_archivo}, columna {col_archivo - 1}')
            estado = 0
        elif estado == "E":
            errores.append(f'Error en la linea {row_archivo}, columna {col_archivo - 1}')
            lexema = ''
            buffer = caracter
            estado = 0
    return analisis, errores, comentarios

def get_col(c):
    simbolos_p1 = [".","_","!","<",">","=","/","*"]
    simbolos_p2 = ["+","-","%","^","(",")","{","}",",",";","&","|"," "]
    
    cod_ascii = ord(c)
    if cod_ascii >= 48 and cod_ascii <= 57:
        return 0
    
    if (cod_ascii >= 65 and cod_ascii <= 90) or (cod_ascii >= 97 and cod_ascii <= 122):
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

def escribir_archivos(tabla_analisis, errores):
    parent_directory = os.path.dirname(__file__)
    dirname = 'analisis_lexico'
    abs_dir = os.path.join(parent_directory,dirname)
    filenames = ['analisis.txt','errores.txt','comentarios.txt']

    if os.path.isdir(abs_dir):
        abs_path = os.path.join(abs_dir,filenames[0])
        with open(abs_path, "w") as archivo:
            archivo.write(tabla_analisis)
            
        abs_path = os.path.join(abs_dir,filenames[1])
        with open(abs_path, "w") as archivo:
            for error in errores:
                archivo.write(f'{error}\n')
        
    else:
        try:
            os.mkdir(abs_dir)
            abs_path = os.path.join(abs_dir,filenames[0])
            with open(abs_path, "w") as archivo:
                archivo.write(tabla_analisis)
                
            abs_path = os.path.join(abs_dir,filenames[1])
            with open(abs_path, "w") as archivo:
                for error in errores:
                    archivo.write(f'{error}\n')
        except:
            print(f'Error al trabajar en el directorio: {abs_dir}')
            pass

def leer_archivo(filepath):
    codigo = ''
    if os.path.exists(filepath):
        with open(filepath, "r") as archivo:
            codigo = archivo.read()
    else:
        print("El archivo no existe")
    
    return codigo

def ejecutar_lexico(codigo):
    analisis, errores, comentarios = analizador_lexico(codigo)
    tabla_analisis = tabulate(analisis, tablefmt="plain")
    escribir_archivos(tabla_analisis,errores)
    return analisis, errores, comentarios

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('Falta el archivo fuente')
    elif len(sys.argv) == 2:
        archivo = sys.argv[1]
        codigo = leer_archivo(archivo)
        analisis, errores, _ = analizador_lexico(codigo)
        tabla_analisis = tabulate(analisis, tablefmt="plain")
        escribir_archivos(tabla_analisis,errores)
