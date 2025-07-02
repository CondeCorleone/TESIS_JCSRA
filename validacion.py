# validacion.py
def verificar_traslapes(df=None, modo_web=False):
    import pandas as pd
    from tkinter import messagebox

    if df is None:
        return "No hay horario generado."

    # Verificar traslapes por grupo, día y bloque
    traslapes_grupo = df.groupby(['Grupo', 'Día', 'Bloque']).size()
    conflictos_grupo = traslapes_grupo[traslapes_grupo > 1]

    # Verificar traslapes por aula, día y bloque
    traslapes_aula = df.groupby(['Aula', 'Día', 'Bloque']).size()
    conflictos_aula = traslapes_aula[traslapes_aula > 1]

    # Verificar traslapes por profesor, día y bloque
    traslapes_profesor = df.groupby(['Profesor', 'Día', 'Bloque']).size()
    conflictos_profesor = traslapes_profesor[traslapes_profesor > 1]

    # Verificar traslapes por grupo, materia y día
    traslapes_materia = df.groupby(['Grupo', 'Materia', 'Día']).size()
    conflictos_materia = traslapes_materia[traslapes_materia > 1]

    # Preparar reporte
    reporte = ""
    if not conflictos_grupo.empty or not conflictos_aula.empty or not conflictos_profesor.empty or not conflictos_materia.empty:
        reporte += "❌ Conflictos encontrados:\n"
        if not conflictos_grupo.empty:
            reporte += f"\n🔸 Grupo/Día/Bloque:\n{conflictos_grupo}\n"
        if not conflictos_aula.empty:
            reporte += f"\n🔸 Aula/Día/Bloque:\n{conflictos_aula}\n"
        if not conflictos_profesor.empty:
            reporte += f"\n🔸 Profesor/Día/Bloque:\n{conflictos_profesor}\n"
        if not conflictos_materia.empty:
            reporte += f"\n🔸 Grupo/Materia/Día:\n{conflictos_materia}\n"
    else:
        reporte = "✅ No se encontraron conflictos."

    if modo_web:
        # Devolver reporte como texto
        return reporte
    else:
        # Mostrar reporte en tkinter
        if "No se encontraron conflictos" in reporte:
            messagebox.showinfo("Validación exitosa", reporte)
        else:
            messagebox.showwarning("Conflictos de Horario", reporte)
        return None
