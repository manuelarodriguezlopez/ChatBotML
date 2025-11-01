import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np
import pickle
import os

# Dataset simulado de referencia
df = pd.read_csv("techniques_datasheet.csv")

# Frutas y categorías
frutas = ["piña", "fresa", "mango", "manzana", "guayaba", "naranja", "uva", "maracuyá"]
madurez = ["verde", "media", "madura"]
metodos = ["directa", "maceración lenta", "infusionada"]

# Generar dataset artificial de entrenamiento
np.random.seed(42)
data = []
for fruta in frutas:
    for _ in range(20):
        registro = {
            "Fruta": fruta,
            "Cantidad": np.random.randint(200, 2000),
            "Concentracion_azucar": np.random.uniform(40, 100),
            "Temperatura": np.random.uniform(20, 30),
            "Tiempo_fermentacion": np.random.uniform(8, 48),
            "Grado_madurez": np.random.choice(madurez),
            "Tiempo_congelado": np.random.uniform(0, 6),
            "Metodo": np.random.choice(metodos),
            "Tecnica_recomendada": np.random.choice(df["Tecnica_recomendada"])
        }
        data.append(registro)

dataset = pd.DataFrame(data)

# Variables y salida
X = dataset.drop(columns=["Tecnica_recomendada"])
y = dataset["Tecnica_recomendada"]

# Codificación y modelo
categorical_features = ["Fruta", "Grado_madurez", "Metodo"]
numeric_features = ["Cantidad", "Concentracion_azucar", "Temperatura", "Tiempo_fermentacion", "Tiempo_congelado"]

encoder = ColumnTransformer([
    ("categorical", OneHotEncoder(handle_unknown="ignore"), categorical_features)
], remainder='passthrough')

model = Pipeline([
    ("encoder", encoder),
    ("classifier", RandomForestClassifier(n_estimators=150, random_state=42))
])

model.fit(X, y)

# Guardar modelo
os.makedirs("models", exist_ok=True)
with open("models/sugar_kef_model.pkl", "wb") as f:
    pickle.dump(model, f)

print(" Modelo actualizado con variables experimentales guardado en models/sugar_kef_model.pkl")
