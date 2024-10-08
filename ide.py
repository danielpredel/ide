import tkinter as tk
from tkinter import filedialog
# import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    # Estado del archivo 0: guardado, 1: modificado
    ruta_archivo = ""
    estado_archivo = 0
    
    def __init__(self):
        super().__init__()

        # Configuracion de la ventana principal
        self.title("Super IDE")
        self.geometry(f"{1100}x{580}")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        
        # Menu
        # Frame del menu
        self.menu_frame = customtkinter.CTkFrame(self, height=40, corner_radius=0)
        # self.menu_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        
        # Logo
        self.logo_label = customtkinter.CTkLabel(self.menu_frame, text="IDE", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Nombre del archivo
        self.archivo_label = customtkinter.CTkTextbox(self.menu_frame, height=20)
        self.archivo_label.grid(row=0, column=1, padx=10, pady=10)
        self.archivo_label.insert("0.0", "main.py")
        self.archivo_label.configure(state="disabled")
        
        # Selector de operaciones del archivo
        self.menu_archivo = customtkinter.CTkOptionMenu(self.menu_frame, dynamic_resizing=False,
                                                        values=["Abrir", "Cerrar", "Guardar", "Guardar como"],
                                                        command=self.operacion_archivo)
        self.menu_archivo.grid(row=0, column=2, padx=10, pady=10)
        
        # Botones compilar y ejecutar
        self.boton_compilar = customtkinter.CTkButton(self.menu_frame, text='Compilar')
        self.boton_compilar.grid(row=0, column=3, padx=10, pady=10)
        self.boton_ejecutar = customtkinter.CTkButton(self.menu_frame, text='Ejecutar')
        self.boton_ejecutar.grid(row=0, column=4, padx=10, pady=10)
        
        # Editor de Codigo
        self.code_textbox = customtkinter.CTkTextbox(self, wrap='none')
        self.code_textbox.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        
        # Outputs para analizadores, errores y ejecucion
        # Frame
        self.output_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.output_frame.grid(row=0, column=1,rowspan=2, sticky="nsew")
        # self.output_frame.grid(row=1, column=1, sticky="nsew")
        self.output_frame.grid_rowconfigure((0,1), weight=1)
        self.output_frame.grid_columnconfigure(0, weight=1)
        
        # Tabview de analizadores ...
        self.analisis_tabview = customtkinter.CTkTabview(self.output_frame, width=500)
        self.analisis_tabview.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.analisis_tabview.add("Lexico")
        self.analisis_tabview.add("Sintactico")
        self.analisis_tabview.add("Semantico")
        self.analisis_tabview.add("C. Intermedio")
        self.analisis_tabview.add("T. Simbolos")
        
        # Textbox de salida para Analisis Lexico
        self.analisis_tabview.tab("Lexico").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("Lexico").grid_rowconfigure(0, weight=1)
        self.lexico_tab = customtkinter.CTkTextbox(self.analisis_tabview.tab("Lexico"), wrap='word')
        self.lexico_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.lexico_tab.insert("0.0", "Analisis Lexico " * 20)
        self.lexico_tab.configure(state="disabled")
        
        # Textbox de salida para Analisis Sintactico
        self.analisis_tabview.tab("Sintactico").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("Sintactico").grid_rowconfigure(0, weight=1)
        self.sintactico_tab = customtkinter.CTkTextbox(self.analisis_tabview.tab("Sintactico"), wrap='word')
        self.sintactico_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.sintactico_tab.insert("0.0", "Analisis Sintactico " * 20)
        self.sintactico_tab.configure(state="disabled")
        
        # Textbox de salida para Analisis Semantico
        self.analisis_tabview.tab("Semantico").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("Semantico").grid_rowconfigure(0, weight=1)
        self.semantico_tab = customtkinter.CTkTextbox(self.analisis_tabview.tab("Semantico"), wrap='word')
        self.semantico_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.semantico_tab.insert("0.0", "Analisis Semantico " * 20)
        self.semantico_tab.configure(state="disabled")
        
        # Textbox de salida para Codigo Intermedio
        self.analisis_tabview.tab("C. Intermedio").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("C. Intermedio").grid_rowconfigure(0, weight=1)
        self.cod_int_tab = customtkinter.CTkTextbox(self.analisis_tabview.tab("C. Intermedio"), wrap='word')
        self.cod_int_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.cod_int_tab.insert("0.0", "Codigo Intermedio " * 20)
        self.cod_int_tab.configure(state="disabled")
        
        # Textbox de salida para Tabla de Simbolos
        self.analisis_tabview.tab("T. Simbolos").grid_columnconfigure(0, weight=1)
        self.analisis_tabview.tab("T. Simbolos").grid_rowconfigure(0, weight=1)
        self.tabla_simb_tab = customtkinter.CTkTextbox(self.analisis_tabview.tab("T. Simbolos"), wrap='word')
        self.tabla_simb_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.tabla_simb_tab.insert("0.0", "Tabla de Simbolos " * 20)
        self.tabla_simb_tab.configure(state="disabled")
        
        
        # Tabview Errores y ejecucion
        self.err_run_tabview = customtkinter.CTkTabview(self.output_frame, width=500)
        self.err_run_tabview.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.err_run_tabview.add("Errores")
        self.err_run_tabview.add("Ejecucion")
        
        # Textbox de salida para Tabla de Simbolos
        self.err_run_tabview.tab("Errores").grid_columnconfigure(0, weight=1)
        self.err_run_tabview.tab("Errores").grid_rowconfigure(0, weight=1)
        self.errores_tab = customtkinter.CTkTextbox(self.err_run_tabview.tab("Errores"), wrap='word')
        self.errores_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.errores_tab.insert("0.0", "Errores " * 20)
        self.errores_tab.configure(state="disabled")
        
        # Textbox de salida para Tabla de Simbolos
        self.err_run_tabview.tab("Ejecucion").grid_columnconfigure(0, weight=1)
        self.err_run_tabview.tab("Ejecucion").grid_rowconfigure(0, weight=1)
        self.ejecucion_tab = customtkinter.CTkTextbox(self.err_run_tabview.tab("Ejecucion"), wrap='word')
        self.ejecucion_tab.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.ejecucion_tab.insert("0.0", "Ejecucion " * 20)
        self.ejecucion_tab.configure(state="disabled")
        
        # Indicador linea y columna del cursor en archivo
        # Label line-col
        self.line_col_label = customtkinter.CTkTextbox(self.output_frame, height=20)
        self.line_col_label.grid(row=2, column=0, padx=20, pady=(20,20), sticky="ew")
        self.line_col_label.insert("0.0", "Ln 0, Col 0")
        self.line_col_label.configure(state="disabled")


    # Metodos
    def operacion_archivo(self, operacion: str):
        # Abrir, cerrar, guardar, gurdar como segun operacion
        self.menu_archivo.set("Abrir")
        # values=["Abrir", "Cerrar", "Guardar", "Guardar como"]
        print(operacion)
        if operacion == "Abrir":
            self.nuevo_archivo(self)
        elif operacion == "Cerrar":
            self.cerrar_archivo(self)
    
    # File Operations
    def nuevo_archivo(self):
        self.code_textbox.delete("1.0", tk.END)
        self.estado_archivo = 1
    
    def cerrar_archivo(self):
        self.code_textbox.delete("1.0", tk.END)
        self.ruta_archivo = ""
        self.title("Super IDE")

    def abrir_archivo(self):
        self.ruta_archivo = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if self.ruta_archivo:
            with open(self.ruta_archivo, 'r') as file:
                content = file.read()
                self.code_textbox.delete("1.0", tk.END)
                self.code_textbox.insert(tk.END, content)
            self.title(self.ruta_archivo)
    
    def guardar_archivo(self):
        if self.ruta_archivo:
            with open(self.ruta_archivo, 'w') as file:
                content = self.code_textbox.get("1.0", tk.END)
                file.write(content)
            self.title(self.ruta_archivo)
            self.ruta_archivo = self.ruta_archivo

    def guardar_como_archivo(self):
        nueva_ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if nueva_ruta_archivo:
            with open(nueva_ruta_archivo, 'w') as file:
                content = self.code_textbox.get("1.0", tk.END)
                file.write(content)
            self.title(nueva_ruta_archivo)
            self.ruta_archivo = nueva_ruta_archivo


if __name__ == "__main__":
    app = App()
    app.mainloop()