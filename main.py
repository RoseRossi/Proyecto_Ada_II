import tkinter as tk
from tkinter import filedialog
from tkinter import font
import fuerzaBruta
import voraz
import lecturaArchivo
import pDinamica
import time


class AlgoritmosApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cálculo de Algoritmos")
        self.master.geometry("800x600")
        self.master.configure(bg="#051127")  
        self.create_widgets()
        self.file_path = None
        self.buttons_frame = None

    def create_widgets(self):
        fuente = font.Font(family="Roboto", size=12)
        self.entrada = tk.Text(self.master, height=20, width=25, state="disabled", bg="#ced0ce", font=fuente)
        self.entrada.grid(column=0, row=0, padx=10, pady=10)
        self.entrada.configure(bg="#017f96", fg="white", highlightbackground="#ffffff")

        self.solucion = tk.Text(self.master, height=20, width=25, state="disabled", bg="#ced0ce", font=fuente)
        self.solucion.grid(column=1, row=0, padx=10, pady=10)
        self.solucion.configure(bg="#017f96", fg="white", highlightbackground="#ffffff")

        self.open_button = tk.Button(self.master, text="Cargar Archivo de Entrada", command=self.open_file, font=fuente)
        self.open_button.grid(column=2, row=0, padx=10, pady=1)
        self.open_button.configure(bg="#7d567e", fg="white", highlightbackground="#ffffff")

        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=10)
        self.buttons_frame.config(bg="#ced0ce")
        
        self.button_fb = tk.Button(self.buttons_frame, text="Fuerza Bruta", command=self.calculate_fb, font=fuente)
        self.button_fb.pack(side="left", padx=5, pady=5)
        self.button_fb.configure(bg="#7d567e", fg="white", highlightbackground="#051127")

        self.button_voraz = tk.Button(self.buttons_frame, text="Algoritmo Voraz", command=self.calculate_voraz, font=fuente)
        self.button_voraz.pack(side="left", padx=5, pady=5)
        self.button_voraz.configure(bg="#7d567e", fg="white", highlightbackground="#051127")

        self.button_pd = tk.Button(self.buttons_frame, text="Programación Dinámica", command=self.calculate_pd, font=fuente)
        self.button_pd.pack(side="left", padx=5, pady=5)
        self.button_pd.configure(bg="#7d567e", fg="white", highlightbackground="#051127")

        self.button_borrar = tk.Button(self.master, text="Borrar", command=self.clear_result, font=fuente)
        self.button_borrar.grid(column=2, row=1, padx=10, pady=1)  # Move it to row 3
        self.button_borrar.configure(bg="#7d567e", fg="white", highlightbackground="#051127")

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.file_path:
            if "cuadrado" in self.file_path.lower():
                print("El archivo contiene 'cuadrado' en su nombre. No se evaluará.")
                self.entrada.config(state="normal")
                self.entrada.delete("1.0", tk.END)
                self.entrada.insert(tk.END, "No se puede evaluar este archivo.")
                self.entrada.config(state="disabled")
            else:
                lecturaArchivo.lecturaArchivo(self.file_path)

                with open(self.file_path, "r") as f:
                    text = f.read()
                    self.entrada.config(state="normal")
                    self.entrada.delete("1.0", tk.END)
                    self.entrada.insert(tk.END, text)
                    self.entrada.config(state="disabled")

    def calculate_fb(self):
        start_time = time.time()
        if self.file_path:
            resultado = fuerzaBruta.rocFB(lecturaArchivo.cantidadmateriasA, lecturaArchivo.cantidadEstudiantesA, lecturaArchivo.materiasA, lecturaArchivo.solicitudesA)
            self.display_result(resultado)
        end_time = time.time()  
        elapsed_time = end_time - start_time 
        print(f"Tiempo de ejecución: {elapsed_time} segundos")

    def calculate_voraz(self):
        start_time = time.time()
        if self.file_path:
            resultado = voraz.rocV(lecturaArchivo.cantidadmateriasA, lecturaArchivo.cantidadEstudiantesA, lecturaArchivo.materiasA, lecturaArchivo.solicitudesA)
            self.display_result(resultado)
        end_time = time.time()  
        elapsed_time = end_time - start_time 
        print(f"Tiempo de ejecución: {elapsed_time} segundos")


    def calculate_pd(self):
        start_time = time.time()
        if self.file_path:
            lecturaArchivo.lecturaArchivo(self.file_path)
            materias_copy = lecturaArchivo.materiasA.copy()
            solicitudes_copy = {estudiante: solicitudes.copy() for estudiante, solicitudes in lecturaArchivo.solicitudesA.items()}
            resultado = pDinamica.rocPD(materias_copy, solicitudes_copy, {})
            self.display_result(resultado)
        end_time = time.time()  
        elapsed_time = end_time - start_time 
        print(f"Tiempo de ejecución: {elapsed_time} segundos")


    def display_result(self, resultado):
        self.solucion.config(state="normal")
        self.solucion.delete("1.0", tk.END)
        self.solucion.insert(tk.END, resultado)
        self.solucion.config(state="disabled")

    def clear_result(self):
        self.solucion.config(state="normal")
        self.solucion.delete("1.0", tk.END)
        self.solucion.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AlgoritmosApp(root)
    root.mainloop()
