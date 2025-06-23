import pandas as pd
import random
from collections import defaultdict

MAX_MATERIAS_POR_GRUPO = 6
MAX_BLOQUES_POR_DIA_GRUPO = 4

def generar_horarios(config, num_grupos=20, usar_modelo=False, modelo=None, encoder_dict=None):
    aulas = config["aulas"]
    modalidades = config["modalidades"]
    profesores = config["profesores"]
    materias_por_semestre = config["asignaturas_por_semestre"]

    horarios = []
    asignaciones = set()
    carga_grupo_dia = defaultdict(lambda: defaultdict(int))
    materias_por_grupo = defaultdict(set)
    profesor_ocupado = defaultdict(lambda: defaultdict(set))
    aula_ocupada = defaultdict(lambda: defaultdict(set))
    grupo_id = 1

    for semestre, materias in materias_por_semestre.items():
        for modalidad in modalidades:
            dias = modalidades[modalidad]["dias"]
            bloques = modalidades[modalidad]["bloques"]
            for _ in range(num_grupos // len(modalidades)):
                grupo = f"{semestre}{modalidad}{str(grupo_id).zfill(2)}"
                grupo_id += 1
                max_materias = min(MAX_MATERIAS_POR_GRUPO, len(materias))
                materias_asignadas = random.sample(materias, k=max_materias)
                bloques_disponibles = [(d, b) for d in dias for b in bloques]
                random.shuffle(bloques_disponibles)

                for materia in materias_asignadas:
                    profesor = random.choice(profesores[materia])
                    asignado = False
                    for dia, bloque in bloques_disponibles:
                        if carga_grupo_dia[grupo][dia] >= MAX_BLOQUES_POR_DIA_GRUPO:
                            continue
                        if materia in materias_por_grupo[grupo]:
                            continue
                        if (grupo, dia, bloque) in asignaciones:
                            continue
                        if bloque in profesor_ocupado[profesor][dia]:
                            continue
                        for aula in aulas:
                            if bloque in aula_ocupada[aula][dia]:
                                continue
                            if usar_modelo and modelo:
                                features = pd.DataFrame([{
                                    "Grupo": grupo,
                                    "Día": dia,
                                    "Bloque": bloque,
                                    "Aula": aula,
                                    "Profesor": profesor,
                                    "Materia": materia
                                }])
                                try:
                                    for col, enc in encoder_dict.items():
                                        features[col + "_enc"] = enc.transform(features[col])
                                    features = features[[col + "_enc" for col in encoder_dict]]
                                    pred = modelo.predict(features)[0]
                                    if pred == 0:
                                        continue
                                except:
                                    continue

                            horarios.append({
                                "Grupo": grupo,
                                "Materia": materia,
                                "Profesor": profesor,
                                "Aula": aula,
                                "Modalidad": modalidad,
                                "Día": dia,
                                "Bloque": bloque
                            })
                            asignaciones.add((grupo, dia, bloque))
                            carga_grupo_dia[grupo][dia] += 1
                            materias_por_grupo[grupo].add(materia)
                            profesor_ocupado[profesor][dia].add(bloque)
                            aula_ocupada[aula][dia].add(bloque)
                            asignado = True
                            break
                        if asignado:
                            break
    return pd.DataFrame(horarios)