import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import os

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    ruta_archivo = ""
    nombre_archivo = "untitled"
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
        self.menu_frame = ctk.CTkFrame(self, height=40, corner_radius=0)
        self.menu_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        
        # Logo
        self.logo_label = ctk.CTkLabel(self.menu_frame, text="IDE", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Nombre del archivo
        self.archivo_label = ctk.CTkTextbox(self.menu_frame, height=20)
        self.archivo_label.grid(row=0, column=1, padx=10, pady=10)
        self.archivo_label.insert("0.0", "untitled")
        self.archivo_label.configure(state="disabled")
        
        # Selector de operaciones del archivo
        self.menu_archivo = ctk.CTkOptionMenu(self.menu_frame, dynamic_resizing=False,
                                                        values=["Abrir", "Cerrar", "Nuevo", "Guardar", "Guardar como"],
                                                        command=self.operacion_archivo)
        self.menu_archivo.grid(row=0, column=2, padx=10, pady=10)
        
        # Botones compilar y ejecutar
        self.boton_compilar = ctk.CTkButton(self.menu_frame, text='Compilar')
        self.boton_compilar.grid(row=0, column=3, padx=10, pady=10)
        self.boton_ejecutar = ctk.CTkButton(self.menu_frame, text='Ejecutar')
        self.boton_ejecutar.grid(row=0, column=4, padx=10, pady=10)
        
        # Editor de Codigo
        # Frame del Editor
        self.editor_frame = ctk.CTkFrame(self, corner_radius=0)
        self.editor_frame.grid(row=1, column=0, sticky="nsew")
        self.editor_frame.grid_rowconfigure(0, weight=1)
        self.editor_frame.grid_columnconfigure(1, weight=1)
        
        # Textbox para numero de linea
        self.line_textbox = ctk.CTkTextbox(self.editor_frame, width=50, wrap='word', activate_scrollbars=False,
                                           state="disabled")
        self.line_textbox.grid(row=0, column=0, padx=(20,0), pady=(20,20), sticky="nsew")
        
        # Textbox para editor de codigo
        self.code_textbox = ctk.CTkTextbox(self.editor_frame, wrap='none', activate_scrollbars=False)
        self.code_textbox.grid(row=0, column=1, padx=(10,10), pady=20, sticky="nsew")
        self.code_textbox.configure(yscrollcommand=self.on_scroll)
        self.code_textbox.bind('<KeyRelease>', self.on_key_release)
        
        # Outputs para analizadores, errores y ejecucion
        # Frame
        self.output_frame = ctk.CTkFrame(self, corner_radius=0)
        self.output_frame.grid(row=1, column=1, sticky="nsew")
        self.output_frame.grid_rowconfigure((0,1), weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)
        
        # Tabview de analizadores ...
        self.analisis_tabview = ctk.CTkTabview(self.output_frame, width=500)
        self.analisis_tabview.grid(row=0, column=0, padx=(10, 20), pady=(10, 0), sticky="nsew")
        self.analisis_tabview.add("Lexico")
        self.analisis_tabview.add("Sintactico")
        self.analisis_tabview.add("Semantico")
        self.analisis_tabview.add("C. Intermedio")
        self.analisis_tabview.add("T. Simbolos")
        
        # Textbox de salida para Analisis Lexico
        self.analisis_tabview.tab("Lexico").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("Lexico").grid_rowconfigure(0, weight=1)
        self.lexico_tab = ctk.CTkTextbox(self.analisis_tabview.tab("Lexico"), wrap='word')
        self.lexico_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.lexico_tab.insert("0.0", "Analisis Lexico " * 20)
        self.lexico_tab.configure(state="disabled")
        
        # Textbox de salida para Analisis Sintactico
        self.analisis_tabview.tab("Sintactico").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("Sintactico").grid_rowconfigure(0, weight=1)
        self.sintactico_tab = ctk.CTkTextbox(self.analisis_tabview.tab("Sintactico"), wrap='word')
        self.sintactico_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.sintactico_tab.insert("0.0", "Analisis Sintactico " * 20)
        self.sintactico_tab.configure(state="disabled")
        
        # Textbox de salida para Analisis Semantico
        self.analisis_tabview.tab("Semantico").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("Semantico").grid_rowconfigure(0, weight=1)
        self.semantico_tab = ctk.CTkTextbox(self.analisis_tabview.tab("Semantico"), wrap='word')
        self.semantico_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.semantico_tab.insert("0.0", "Analisis Semantico " * 20)
        self.semantico_tab.configure(state="disabled")
        
        # Textbox de salida para Codigo Intermedio
        self.analisis_tabview.tab("C. Intermedio").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("C. Intermedio").grid_rowconfigure(0, weight=1)
        self.cod_int_tab = ctk.CTkTextbox(self.analisis_tabview.tab("C. Intermedio"), wrap='word')
        self.cod_int_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.cod_int_tab.insert("0.0", "Codigo Intermedio " * 20)
        self.cod_int_tab.configure(state="disabled")
        
        # Textbox de salida para Tabla de Simbolos
        self.analisis_tabview.tab("T. Simbolos").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("T. Simbolos").grid_rowconfigure(0, weight=1)
        self.tabla_simb_tab = ctk.CTkTextbox(self.analisis_tabview.tab("T. Simbolos"), wrap='word')
        self.tabla_simb_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.tabla_simb_tab.insert("0.0", "Tabla de Simbolos " * 20)
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
        self.errores_tab.insert("0.0", "Errores " * 20)
        self.errores_tab.configure(state="disabled")
        
        # Textbox de salida para Tabla de Simbolos
        self.err_run_tabview.tab("Ejecucion").grid_columnconfigure(0, weight=1)
        self.err_run_tabview.tab("Ejecucion").grid_rowconfigure(0, weight=1)
        self.ejecucion_tab = ctk.CTkTextbox(self.err_run_tabview.tab("Ejecucion"), wrap='word')
        self.ejecucion_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.ejecucion_tab.insert("0.0", "Ejecucion " * 20)
        self.ejecucion_tab.configure(state="disabled")
        
        # Indicador linea y columna del cursor en archivo
        # Label line-col
        self.line_col_label = ctk.CTkTextbox(self.output_frame, height=20)
        self.line_col_label.grid(row=2, column=0, padx=(10,20), pady=(20,20), sticky="ew")
        self.line_col_label.insert("0.0", "Ln 1, Col 0")
        self.line_col_label.configure(state="disabled")

    # Transiscion entre estados del archivo
    #           Nuevo   Abrir   Cerrar  Guardar Guardar como
    # Nuevo     O       O       O       O       O
    # Editado   X       X       X       O       O
    # Guardado  O       O       O       O       O
    
    # Transiscion entre estados del archivo
    #           Nuevo   Abrir   Cerrar  Guardar     Guardar como
    # Nuevo     OK      OK      OK      OK          OK
    # Editado   OK      OK      OK      OK(N)       OK
    # Guardado  O       O       O       O           O
    # Si no hay ruta llamar automaticamente guardar como
    def operacion_archivo(self, operacion: str):
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

    def guardar_archivo(self, *args):
        if self.ruta_archivo:
            with open(self.ruta_archivo, 'w') as file:
                content = self.code_textbox.get("1.0", tk.END)
                file.write(content)
            self.estado_archivo = 2
            self.title(self.ruta_archivo)
            self.ruta_archivo = self.ruta_archivo
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
        col = cursor_pos.split('.')[1]
        
        # Actualiza la etiqueta con la información de la línea actual
        self.line_col_label.configure(state="normal")
        self.line_col_label.delete("0.0", "end")
        self.line_col_label.insert("0.0", f"Ln {linea}, Col {col}")
        self.line_col_label.configure(state="disabled")
    
    def actualizar_archivo_label(self, *args):
        self.archivo_label.configure(state="normal")
        self.archivo_label.delete("0.0", "end")
        # if self.estado_archivo == 0:
        #     self.archivo_label.insert("0.0", "untitled")
        # elif self.estado_archivo == 1:
        #     self.archivo_label.insert("0.0", f"{self.nombre_archivo} *")
        # elif self.estado_archivo == 2:
        #     self.archivo_label.insert("0.0", f"{self.nombre_archivo}")
        
        if self.estado_archivo == 1:
            self.archivo_label.insert("0.0", f"{self.nombre_archivo} *")
        else:
            self.archivo_label.insert("0.0", f"{self.nombre_archivo}")
            
        self.archivo_label.configure(state="disabled")
    
    def generar_confirmacion(self, *args):
        # Crear la ventana de advertencia
        self.ventana_advertencia = tk.Toplevel(self)
        self.ventana_advertencia.geometry("400x150")
        self.ventana_advertencia.title("Super IDE")
        # Agregar el mensaje de advertencia
        mensaje1 = tk.Label(self.ventana_advertencia, text="¿Deseas guardar tus cambios?",
                                    font=("Arial", 15))
        mensaje1.pack()
        
        mensaje2 = tk.Label(self.ventana_advertencia, text="Tus cambios se perderan si no los guardas",
                                    font=("Arial", 12))
        mensaje2.pack()
        
        # Agregar el botón de aceptar
        boton_guardar = tk.Button(self.ventana_advertencia, text="Guardar",
                                  command=lambda: self.get_resultado_advertencia(self, "SI"))
        boton_guardar.config(borderwidth=5, relief="groove", font=("Arial", 12))
        boton_guardar.pack(side=tk.LEFT, padx=(20,0))
        
        boton_no_guardar = tk.Button(self.ventana_advertencia, text="No guardar",
                                  command=lambda: self.get_resultado_advertencia(self, "NO"))
        boton_no_guardar.config(borderwidth=5, relief="groove", font=("Arial", 12))
        boton_no_guardar.pack(side=tk.RIGHT, padx=(0,20))

        # Agregar el botón de cancelar
        boton_cancelar = tk.Button(self.ventana_advertencia, text="Cancelar",
                                  command=lambda: self.get_resultado_advertencia(self, "CANCELAR"))
        boton_cancelar.config(borderwidth=5, relief="groove", font=("Arial", 12))
        boton_cancelar.pack(side=tk.BOTTOM, padx=(10,10))
    
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
        
if __name__ == "__main__":
    app = App()
    app.mainloop()