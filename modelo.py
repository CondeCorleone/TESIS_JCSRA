import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

def entrenar_modelo_rf(df):
    le_dict = {col: LabelEncoder() for col in ["Grupo", "Día", "Bloque", "Aula", "Profesor", "Materia"]}
    for col, le in le_dict.items():
        df[col + "_enc"] = le.fit_transform(df[col])
    df["Valido"] = 1
    invalids = df.sample(frac=0.2).copy()
    invalids["Aula_enc"] = (invalids["Aula_enc"] + 1) % df["Aula_enc"].nunique()
    invalids["Valido"] = 0
    combined = pd.concat([df, invalids])
    X = combined[[col + "_enc" for col in le_dict]]
    y = combined["Valido"]
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model, le_dict