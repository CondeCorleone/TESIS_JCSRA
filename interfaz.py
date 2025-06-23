# interfaz.py
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import json

from modelo import entrenar_modelo_rf
from generador import generar_horarios
from validacion import verificar_traslapes
from exportador import exportar_horarios

# Cargar configuración
with open("config.json", "r", encoding="utf-8") as f:
    config_json = json.load(f)

# Variables globales
df_horarios = None
modelo_rf = None
codificadores = None

# Funciones de la GUI
def generar_horario():
    global df_horarios, modelo_rf, codificadores
    try:
        df_entrenamiento = generar_horarios(config_json, num_grupos=15)
        modelo_rf, codificadores = entrenar_modelo_rf(df_entrenamiento)
        df_horarios = generar_horarios(config_json, num_grupos=15, usar_modelo=True, modelo=modelo_rf, encoder_dict=codificadores)
        messagebox.showinfo("Éxito", "✅ Horario generado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar horario:\n{str(e)}")

def validar_traslapes():
    global df_horarios
    if df_horarios is None:
        messagebox.showwarning("Advertencia", "Primero genera el horario.")
        return
    verificar_traslapes(df_horarios)

def exportar():
    global df_horarios
    if df_horarios is None:
        messagebox.showwarning("Advertencia", "Primero genera el horario.")
        return
    exportar_horarios(df_horarios)
    messagebox.showinfo("Éxito", "✅ Horario exportado correctamente.")

# GUI principal
root = tk.Tk()
root.title("Sistema Automatizado de Horarios CAMCM")
root.geometry("400x300")

tk.Label(root, text="✅ Sistema Automatizado de Horarios CAMCM", font=("Arial", 16), pady=20).pack()

tk.Button(root, text="Generar Horario", command=generar_horario, font=("Arial", 12), width=25).pack(pady=10)
tk.Button(root, text="Validar Traslapes", command=validar_traslapes, font=("Arial", 12), width=25).pack(pady=10)
tk.Button(root, text="Exportar Horario", command=exportar, font=("Arial", 12), width=25).pack(pady=10)

tk.Label(root, text="Versión 1.0 | Julio César Santa Rita Ávila", font=("Arial", 10), pady=10).pack(side=tk.BOTTOM)

root.mainloop()