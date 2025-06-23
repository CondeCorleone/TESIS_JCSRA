import pandas as pd

def exportar_horarios(df, filename="horario_validado.csv"):
    pivot = df.pivot_table(
        index=["Grupo", "Materia", "Profesor", "Aula"],
        columns="Día",
        values="Bloque",
        aggfunc=lambda x: ', '.join(sorted(x))
    ).reset_index()

    column_order = ["Grupo", "Materia", "Profesor", "Aula", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
    for col in column_order:
        if col not in pivot.columns:
            pivot[col] = ""
    pivot = pivot[column_order]

    pivot.to_csv(filename, index=False)
    print(f"✅ Horario exportado como '{filename}'")