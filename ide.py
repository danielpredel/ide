import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import subprocess
from threading import Thread
import time
from tabulate import tabulate
from tokens import tokens

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    ruta_archivo = ""
    nombre_archivo = "untitled"
    icons = ["open_file.png","close_file.png","new_file.png","save_file.png","save_as_file.png","build.png","run.png"]
    icons_dirname = "icons"
    icon_images = []
    resultado_lexico = ''
    analisis_lexico = []
    comentarios = []
    
    # Estado del archivo:
    # 0 - nuevo
    # 1 - editado
    # 2 - guardado
    estado_archivo = 0
    saltar_advertencia = False
    
    def __init__(self):
        super().__init__()

        # Configuracion de la ventana principal
        self.title("Super IDE")
        self.geometry(f"{1100}x{580}")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Menu
        # Frame del menu
        self.menu_frame = ctk.CTkFrame(self, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # Logo
        self.logo_label = ctk.CTkLabel(self.menu_frame, text="Super IDE", font=ctk.CTkFont(size=20, weight="bold"), height=30)
        self.logo_label.grid(row=0, column=0, padx=(20,5), pady=10)
        
        # Nombre del archivo
        self.archivo_label = ctk.CTkTextbox(self.menu_frame, height=36)
        self.archivo_label.grid(row=0, column=1, padx=5, pady=10)
        self.archivo_label.insert("0.0", "untitled")
        self.archivo_label.configure(state="disabled")
        
        # Selector de operaciones del archivo
        self.menu_archivo = ctk.CTkOptionMenu(self.menu_frame, dynamic_resizing=False,values=["Abrir", "Cerrar", "Nuevo", "Guardar", "Guardar como"], command=self.operacion_archivo, height=36)
        self.menu_archivo.grid(row=0, column=2, padx=5, pady=10)
        
        for i in range(0, len(self.icons)):
            absolute_path = os.path.abspath(os.path.join(self.icons_dirname, self.icons[i]))
            image = ctk.CTkImage(light_image=Image.open(absolute_path),dark_image=Image.open(absolute_path), size=(30, 30))
            self.icon_images.append(image)
        
        # Botones para operaciones sobre archivos
        self.open_file_button = ctk.CTkButton(self.menu_frame, text=None, image=self.icon_images[0], width=40, command= lambda: self.operacion_archivo(operacion="Abrir"))
        self.open_file_button.grid(row=0, column=3, padx=5, pady=10)
        self.close_file_button = ctk.CTkButton(self.menu_frame, text=None, image=self.icon_images[1], width=40, command= lambda: self.operacion_archivo(operacion="Cerrar"))
        self.close_file_button.grid(row=0, column=4, padx=5, pady=10)
        self.new_file_button = ctk.CTkButton(self.menu_frame, text=None, image=self.icon_images[2], width=40, command= lambda: self.operacion_archivo(operacion="Nuevo"))
        self.new_file_button.grid(row=0, column=5, padx=5, pady=10)
        self.save_file_button = ctk.CTkButton(self.menu_frame, text=None, image=self.icon_images[3], width=40, command= lambda: self.operacion_archivo(operacion="Guardar"))
        self.save_file_button.grid(row=0, column=6, padx=5, pady=10)
        self.save_as_file_button = ctk.CTkButton(self.menu_frame, text=None, image=self.icon_images[4],width=40, command= lambda: self.operacion_archivo(operacion="Guardar como"))
        self.save_as_file_button.grid(row=0, column=7, padx=5, pady=10)
        
        # Botones compilar y ejecutar
        self.build_button = ctk.CTkButton(self.menu_frame, text=None, image=self.icon_images[5], width=40, command=self.build_file)
        self.build_button.grid(row=0, column=8, padx=5, pady=10)
        self.run_button = ctk.CTkButton(self.menu_frame, text=None, image=self.icon_images[6], width=40)
        self.run_button.grid(row=0, column=9, padx=5, pady=10)
        
        # Editor de Codigo
        # Frame del Editor
        self.editor_frame = ctk.CTkFrame(self, corner_radius=0)
        self.editor_frame.grid(row=1, column=0, sticky="nsew")
        self.editor_frame.grid_rowconfigure(0, weight=1)
        self.editor_frame.grid_columnconfigure(1, weight=1)
        
        # Textbox para numero de linea
        self.line_textbox = ctk.CTkTextbox(self.editor_frame, width=50, wrap='word', activate_scrollbars=False,state="disabled",font=("TkDefaultFont", 15))
        self.line_textbox.grid(row=0, column=0, padx=(20,0), pady=(10,20), sticky="nsew")
        
        # Textbox para editor de codigo
        self.code_textbox = ctk.CTkTextbox(self.editor_frame, wrap='none', activate_scrollbars=False,font=("TkDefaultFont", 15), text_color="black")
        self.code_textbox.grid(row=0, column=1, padx=(10,10), pady=(10,20), sticky="nsew")
        self.code_textbox.configure(yscrollcommand=self.on_scroll)
        self.code_textbox.bind('<KeyRelease>', self.on_key_release)
        self.code_textbox.bind('<ButtonRelease-1>', self.on_click)
        
        # Outputs para analizadores, errores y ejecucion
        # Frame
        self.output_frame = ctk.CTkFrame(self, corner_radius=0)
        self.output_frame.grid(row=1, column=1, sticky="nsew")
        self.output_frame.grid_rowconfigure((0,1), weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)
        
        # Tabview de analizadores ...
        self.analisis_tabview = ctk.CTkTabview(self.output_frame, width=500)
        self.analisis_tabview.grid(row=0, column=0, padx=(10, 20), pady=0, sticky="nsew")
        self.analisis_tabview.add("Lexico")
        self.analisis_tabview.add("Sintactico")
        self.analisis_tabview.add("Semantico")
        self.analisis_tabview.add("C. Intermedio")
        self.analisis_tabview.add("T. Simbolos")
        
        # Textbox de salida para Analisis Lexico
        self.analisis_tabview.tab("Lexico").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("Lexico").grid_rowconfigure(0, weight=1)
        self.lexico_tab = ctk.CTkTextbox(self.analisis_tabview.tab("Lexico"), wrap='none')
        self.lexico_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.lexico_tab.configure(state="disabled")
        
        # Textbox de salida para Analisis Sintactico
        self.analisis_tabview.tab("Sintactico").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("Sintactico").grid_rowconfigure(0, weight=1)
        self.sintactico_tab = ctk.CTkTextbox(self.analisis_tabview.tab("Sintactico"), wrap='word')
        self.sintactico_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.sintactico_tab.configure(state="disabled")
        
        # Textbox de salida para Analisis Semantico
        self.analisis_tabview.tab("Semantico").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("Semantico").grid_rowconfigure(0, weight=1)
        self.semantico_tab = ctk.CTkTextbox(self.analisis_tabview.tab("Semantico"), wrap='word')
        self.semantico_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.semantico_tab.configure(state="disabled")
        
        # Textbox de salida para Codigo Intermedio
        self.analisis_tabview.tab("C. Intermedio").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("C. Intermedio").grid_rowconfigure(0, weight=1)
        self.cod_int_tab = ctk.CTkTextbox(self.analisis_tabview.tab("C. Intermedio"), wrap='word')
        self.cod_int_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.cod_int_tab.configure(state="disabled")
        
        # Textbox de salida para Tabla de Simbolos
        self.analisis_tabview.tab("T. Simbolos").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("T. Simbolos").grid_rowconfigure(0, weight=1)
        self.tabla_simb_tab = ctk.CTkTextbox(self.analisis_tabview.tab("T. Simbolos"), wrap='word')
        self.tabla_simb_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.tabla_simb_tab.configure(state="disabled")
        
        # Tabview Errores y ejecucion
        self.err_run_tabview = ctk.CTkTabview(self.output_frame, width=500)
        self.err_run_tabview.grid(row=1, column=0, padx=(10, 20), pady=(10, 0), sticky="nsew")
        self.err_run_tabview.add("Errores")
        self.err_run_tabview.add("Ejecucion")
        
        # Textbox de salida para Tabla de Simbolos
        self.err_run_tabview.tab("Errores").grid_columnconfigure(0, weight=1)
        self.err_run_tabview.tab("Errores").grid_rowconfigure(0, weight=1)
        self.errores_tab = ctk.CTkTextbox(self.err_run_tabview.tab("Errores"), wrap='word')
        self.errores_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.errores_tab.configure(state="disabled")
        
        # Textbox de salida para Tabla de Simbolos
        self.err_run_tabview.tab("Ejecucion").grid_columnconfigure(0, weight=1)
        self.err_run_tabview.tab("Ejecucion").grid_rowconfigure(0, weight=1)
        self.ejecucion_tab = ctk.CTkTextbox(self.err_run_tabview.tab("Ejecucion"), wrap='word')
        self.ejecucion_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.ejecucion_tab.configure(state="disabled")
        
        # Indicador linea y columna del cursor en archivo
        # Label line-col
        self.line_col_label = ctk.CTkTextbox(self.output_frame, height=20)
        self.line_col_label.grid(row=2, column=0, padx=(10,20), pady=(20,20), sticky="ew")
        self.line_col_label.insert("0.0", "Ln 1, Col 1")
        self.line_col_label.configure(state="disabled")

    def operacion_archivo(self, operacion: str):
        # Transiscion entre estados del archivo
        #           Nuevo   Abrir   Cerrar  Guardar Guardar como
        # Nuevo     O       O       O       O       O
        # Editado   X       X       X       O       O
        # Guardado  O       O       O       O       O
        matriz = [[True, True, True, False, True],
                  [False, False, False, True, False],
                  [True, True, True, True, True]]

        if operacion == "Nuevo":
            if matriz[self.estado_archivo][0]:
                self.nuevo_archivo(self)
            else:
                self.adv_op = operacion
                self.generar_confirmacion(self)
        elif operacion == "Abrir":
            if matriz[self.estado_archivo][1]:
                self.abrir_archivo(self)
            else:
                self.adv_op = operacion
                self.generar_confirmacion(self)
        elif operacion == "Cerrar":
            if matriz[self.estado_archivo][2]:
                self.cerrar_archivo(self)
            else:
                self.adv_op = operacion
                self.generar_confirmacion(self)
        elif operacion == "Guardar":
            if matriz[0][3]:
                self.guardar_como_archivo(self)
            elif matriz[1][3]:
                if self.ruta_archivo != "":
                    self.guardar_archivo(self)
                else:
                    self.guardar_como_archivo(self)
            elif matriz[2][3]:
                self.guardar_archivo(self)
        elif operacion == "Guardar como":
            self.guardar_como_archivo(self)
            
        self.menu_archivo.set("Abrir")
        self.enlazar_scroll()
        self.actualizar_posicion_cursor()
    
    # Operaciones de archivos
    def nuevo_archivo(self, *args):
        self.code_textbox.delete("1.0", tk.END)
        self.estado_archivo = 0
        self.nombre_archivo = "untitled"
        self.ruta_archivo = ""
        self.title(self.nombre_archivo)
        self.actualizar_archivo_label()
        self.actualizar_lineas()
        self.actualizar_posicion_cursor()
    
    def cerrar_archivo(self, *args):
        self.code_textbox.delete("1.0", tk.END)
        self.ruta_archivo = ""
        self.title("Super IDE")
        self.estado_archivo = 0
        self.nombre_archivo = "untitled"
        self.actualizar_archivo_label()
        self.actualizar_lineas()
        self.actualizar_posicion_cursor()

    def abrir_archivo(self, *args):
        self.ruta_archivo = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])

        if self.ruta_archivo:
            with open(self.ruta_archivo, 'r') as file:
                content = file.read()
                self.code_textbox.delete("1.0", tk.END)
                self.code_textbox.insert(tk.END, content)
                
            self.title(self.ruta_archivo)
            self.estado_archivo = 2
            self.nombre_archivo = os.path.basename(self.ruta_archivo)
            self.actualizar_archivo_label()
            self.actualizar_lineas()
            self.actualizar_posicion_cursor()
            
            # Prueba de analisis lexico en apertura de archivo
            self.hilo_lexico(self)

    def guardar_archivo(self, *args):
        if self.ruta_archivo:
            with open(self.ruta_archivo, 'w') as file:
                content = self.code_textbox.get("1.0", tk.END)
                file.write(content)
            self.estado_archivo = 2
            self.title(self.ruta_archivo)
            # self.ruta_archivo = self.ruta_archivo
            self.actualizar_archivo_label()

    def guardar_como_archivo(self, *args):
        nueva_ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if nueva_ruta_archivo:
            with open(nueva_ruta_archivo, 'w') as file:
                content = self.code_textbox.get("1.0", tk.END)
                file.write(content)
            self.estado_archivo = 2
            self.title(nueva_ruta_archivo)
            self.ruta_archivo = nueva_ruta_archivo
            self.nombre_archivo = os.path.basename(self.ruta_archivo)
            self.actualizar_archivo_label()
    
    # Eventos
    def on_scroll(self, *args):
        self.enlazar_scroll()

    def on_key_release(self, *args):
        self.enlazar_scroll()
        self.actualizar_posicion_cursor()
        self.estado_archivo = 1
        if self.ruta_archivo == "":
            self.title(f"{self.nombre_archivo} *")
        else:
            self.title(f"{self.ruta_archivo} *")
        self.actualizar_archivo_label()
        
        # Borrar esto, solo prueba de rendimiento
        # Funciona bien, pero obviamente al escribir mucho se traba
        # esto significa que un analizador lexico por casos (linea o bloque)
        # funcionara de forma optima
        # self.guardar_archivo(self)
        # self.hilo_lexico(self)

    def on_click(self, *args):
        self.actualizar_posicion_cursor()
        
    # Acciones a eventos
    def enlazar_scroll(self, *args):
        primera_posicion, *_ = self.code_textbox.yview()
        self.actualizar_lineas()
        self.line_textbox.yview_moveto(primera_posicion)
    
    def actualizar_lineas(self, *args):
        self.line_textbox.configure(state="normal")
        self.line_textbox.delete("0.0", "end")
        contenido = self.code_textbox.get("1.0", tk.END)
        
        # Contar el número de líneas divididas por el salto de línea
        n = len(contenido.split('\n')) - 1
        
        for i in range(1, n + 1):
            if i < n:
                self.line_textbox.insert(tk.END, f"{i}\n")
            else:
                self.line_textbox.insert(tk.END, f"{i}")
        
        self.line_textbox.configure(state="disabled")

    def actualizar_posicion_cursor(self, *args):
        # Obtiene la posición del cursor
        cursor_pos = self.code_textbox.index(ctk.INSERT)
        
        # Extrae la parte antes del "." para obtener el número de línea
        linea = cursor_pos.split('.')[0]
        col = int(cursor_pos.split('.')[1]) + 1
        
        # Actualiza la etiqueta con la información de la línea actual
        self.line_col_label.configure(state="normal")
        self.line_col_label.delete("0.0", "end")
        self.line_col_label.insert("0.0", f"Ln {linea}, Col {col}")
        self.line_col_label.configure(state="disabled")
    
    def actualizar_archivo_label(self, *args):
        self.archivo_label.configure(state="normal")
        self.archivo_label.delete("0.0", "end")
        
        if self.estado_archivo == 1:
            self.archivo_label.insert("0.0", f"{self.nombre_archivo} *")
        else:
            self.archivo_label.insert("0.0", f"{self.nombre_archivo}")
        
        self.archivo_label.configure(state="disabled")
    
    def generar_confirmacion(self, *args):
        # Crear la ventana de advertencia
        self.ventana_advertencia = ctk.CTkToplevel(self)
        self.ventana_advertencia.title("Super IDE")

        # Agregar el mensaje de advertencia
        mensaje = ctk.CTkLabel(self.ventana_advertencia, text="¿Deseas guardar tus cambios?\nTus cambios se perderan si no los guardas",font=("Arial", 15))
        mensaje.grid(row=0, column=0, padx=5, pady=10, columnspan=3)

        # Agregar el botón de aceptar
        boton_guardar = ctk.CTkButton(self.ventana_advertencia, text="Guardar",command=lambda: self.get_resultado_advertencia(self, "SI"))
        boton_guardar.grid(row=1, column=0, padx=5, pady=10)

        # Agregar el botón de cancelar
        boton_cancelar = ctk.CTkButton(self.ventana_advertencia, text="Cancelar",command=lambda: self.get_resultado_advertencia(self, "CANCELAR"))
        boton_cancelar.grid(row=1, column=1, padx=5, pady=10)

        boton_no_guardar = ctk.CTkButton(self.ventana_advertencia, text="No guardar",command=lambda: self.get_resultado_advertencia(self, "NO"))
        boton_no_guardar.grid(row=1, column=2, padx=5, pady=10)
    
    def get_resultado_advertencia(self, *args):
        self.ventana_advertencia.destroy()
        extra, resultado, *_ = args
        
        if resultado == "SI":
            # si no hay ruta guardar como, si la hay guardar
            if self.ruta_archivo != "":
                self.guardar_archivo(self)
            else:
                self.guardar_como_archivo(self)
        
        if resultado != "CANCELAR":
            if self.adv_op == "Abrir":
                self.abrir_archivo(self)
            elif self.adv_op == "Nuevo":
                self.nuevo_archivo(self)
            elif self.adv_op == "Cerrar":
                self.cerrar_archivo(self)

    def build_file(self, *args):
        if not self.ruta_archivo:
            self.guardar_como_archivo(self)
        else:
            self.hilo_lexico(self)
        
    def analizar_lexico(self, *args):
        proceso = subprocess.run(["python", "lexico.py", self.ruta_archivo], capture_output=True)
        self.resultado_lexico = proceso.stdout.decode("utf-8")
    
    def hilo_lexico(self, *args):
        hilo = Thread(target=self.analizar_lexico)
        hilo.start()

        while hilo.is_alive():
            time.sleep(0.1)
        
        self.mostrar_analisis_lexico(self)
        self.style_code(self)
            
    def leer_analisis_lexico(self, *args):
        analisis = []
        dirname = 'analisis_lexico'
        filename = 'analisis.txt'
        abs_path = os.path.join(dirname,filename)
        if os.path.exists(abs_path):
            with open(abs_path, "r") as archivo:
                lineas = archivo.readlines()
            for linea in lineas:
                lexema = linea.split()
                analisis.append(lexema)    
        else:
            print("El archivo {abs_path} no existe")
        
        errores = ''
        dirname = 'analisis_lexico'
        filename = 'errores.txt'
        abs_path = os.path.join(dirname,filename)
        if os.path.exists(abs_path):
            with open(abs_path, "r") as archivo:
                errores = archivo.read()   
        else:
            print("El archivo {abs_path} no existe")
            
        # 
        comentarios = []
        dirname = 'analisis_lexico'
        filename = 'comentarios.txt'
        abs_path = os.path.join(dirname,filename)
        if os.path.exists(abs_path):
            with open(abs_path, "r") as archivo:
                lineas = archivo.readlines()
            for linea in lineas:
                comentario = linea.split()
                comentarios.append(comentario)
        else:
            print("El archivo {abs_path} no existe")
        
        return analisis, errores, comentarios
     
    def mostrar_analisis_lexico(self, *args):
        if self.resultado_lexico:
            self.errores_tab.configure(state="normal")
            self.errores_tab.delete("0.0", "end")
            self.errores_tab.insert("0.0", f"{self.resultado_lexico}")
            self.errores_tab.configure(state="disabled")
        else:
            self.analisis_lexico, errores, self.comentarios = self.leer_analisis_lexico(self)
            self.lexico_tab.configure(state="normal")
            self.lexico_tab.delete("0.0", "end")
            self.lexico_tab.insert("end", "LEXEMA\t\tTOKEN\t\t\tSUBTOKEN\t\t\tFILA\tCOL_I\tCOL_F\n")
            for lexema in self.analisis_lexico:
                self.lexico_tab.insert("end", f"{lexema[0]}\t\t{lexema[1]}\t\t\t{lexema[2]}\t\t\t{lexema[3]}\t{lexema[4]}\t{lexema[5]}\n")
            self.lexico_tab.configure(state="disabled")
            
            self.errores_tab.configure(state="normal")
            self.errores_tab.delete("0.0", "end")
            self.errores_tab.insert("0.0", f"{errores}")
            self.errores_tab.configure(state="disabled")
    
    def style_code(self, *args):
        colores = ['#e5c07b','#61afef','#d55fde','red','#00ad00',
                   '#f6531c','#ffffff','#651a01','#7f848e']
        # numeros               amarillo = '#e5c07b'
        # identificadores       azul = '#61afef'
        # palabras reservadas   rosa = '#d55fde'
        # ops aritmeticos       rojo = 'red'
        # ops relacionales      verde = '#00ad00'
        # ops logicos           naranja = '#f6531c'
        # simbolos              blanco = '#ffffff'
        # asignacion            marron = '#651a01'
        # comentarios           gris = '#7f848e'
        
        for lexema in self.analisis_lexico:
            token = tokens.index(lexema[1])
            start_index = f"{lexema[3]}.{int(lexema[4])-1}"
            end_index = f"{lexema[3]}.{int(lexema[5])-1}"
            self.code_textbox.tag_add(lexema[1], start_index, end_index)
            self.code_textbox.tag_config(lexema[1], foreground=colores[token])
            
        for comentario in self.comentarios:
            # print(comentario)
            start_index = f"{comentario[1]}.{int(comentario[3])-1}"
            end_index = f"{comentario[2]}.{int(comentario[4])-1}"
            self.code_textbox.tag_add(comentario[0], start_index, end_index)
            self.code_textbox.tag_config(comentario[0], foreground=colores[8])

if __name__ == "__main__":
    app = App()
    app.mainloop()
