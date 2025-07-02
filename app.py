#! /usr/bin/env python
# app.py
from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import json

from modelo import entrenar_modelo_rf
from generador import generar_horarios
from validacion import verificar_traslapes
from exportador import exportar_horarios

app = Flask(__name__)

# Cargar configuración
with open("config.json", "r", encoding="utf-8") as f:
    config_json = json.load(f)

# Variables globales
df_horarios = None
modelo_rf = None
codificadores = None
traslapes_output = ""

@app.route("/")
def index():
    return render_template("index.html", traslapes=traslapes_output)

@app.route("/generar", methods=["POST"])
def generar():
    global df_horarios, modelo_rf, codificadores
    df_entrenamiento = generar_horarios(config_json, num_grupos=15)
    modelo_rf, codificadores = entrenar_modelo_rf(df_entrenamiento)
    df_horarios = generar_horarios(config_json, num_grupos=15, usar_modelo=True, modelo=modelo_rf, encoder_dict=codificadores)
    return redirect(url_for("index"))

@app.route("/validar", methods=["POST"])
def validar():
    global df_horarios, traslapes_output
    if df_horarios is None:
        traslapes_output = "Primero genere el horario."
    else:
        traslapes_output = verificar_traslapes(df_horarios, modo_web=True)
    return redirect(url_for("index"))

@app.route("/exportar", methods=["POST"])
def exportar():
    global df_horarios
    if df_horarios is not None:
        exportar_horarios(df_horarios)
        return send_file("horario_validado.csv", as_attachment=True)
    else:
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
