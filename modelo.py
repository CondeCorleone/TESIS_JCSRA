import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def entrenar_modelo_rf(df):
    le_dict = {col: LabelEncoder() for col in ["Grupo", "Día", "Bloque", "Aula", "Profesor", "Materia"]}
    for col, le in le_dict.items():
        df[col + "_enc"] = le.fit_transform(df[col])
    df["Valido"] = 1

    # Segun entiendo, se destina un 20% del conjunto de datos para ser marcado
    # como inválido, pero no hay algo que indique el "criterio de invalidación".
    invalids = df.sample(frac=0.2).copy()
    invalids["Aula_enc"] = (invalids["Aula_enc"] + 1) % df["Aula_enc"].nunique()
    invalids["Valido"] = 0
    combined = pd.concat([df, invalids])
    X = combined[[col + "_enc" for col in le_dict]]
    y = combined["Valido"]

    # ¿Cómo se determinó el valor del parámetro n_estimators?
    # Por reproducibilidad, ciertamente random_state debe ser colocado en un
    # valor fijo pero en producción debería ser None
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, le_dict
