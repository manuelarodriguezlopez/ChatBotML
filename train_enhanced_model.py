import pandas as pd
import numpy as np
import pickle
import os
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# Cargar datos
df = pd.read_csv("data/enhanced_techniques_datasheet.csv")

# Simular frutas por categoría
categorias = {
    "blanda": ["mango", "fresa", "melón", "sandía", "durazno"],
    "fibrosa": ["piña", "guayaba", "papaya", "chontaduro", "zapote"],
    "cítrica": ["naranja", "limón", "mandarina", "toronja", "maracuyá"],
    "seca": ["higo", "uva pasa", "coco", "mamey", "níspero"]
}

X, y = [], []
for _, row in df.iterrows():
    tipo = row["Tipo_fruta_adecuado"]
    frutas_tipo = categorias[tipo]
    rango = row["Rango_cantidad_ml"].split("-")
    min_ml, max_ml = int(rango[0]), int(rango[1])
    for fruta in frutas_tipo:
        for _ in range(15):
            cantidad = np.random.randint(min_ml, max_ml)
            X.append([fruta, cantidad])
            y.append(row["Tecnica_recomendada"])

X_df = pd.DataFrame(X, columns=["Fruta", "Cantidad"])
y_df = pd.Series(y, name="Tecnica")

# Codificador y modelo
encoder = OneHotEncoder(handle_unknown='ignore')
X_encoded = encoder.fit_transform(X_df[["Fruta"]]).toarray()
X_final = np.concatenate([X_encoded, X_df[["Cantidad"]].values], axis=1)

model = RandomForestClassifier(n_estimators=150, random_state=42)
model.fit(X_final, y_df)

os.makedirs("models", exist_ok=True)
with open("models/sugar_kef_model.pkl", "wb") as f:
    pickle.dump((model, encoder), f)

print("Modelo mejorado entrenado y guardado correctamente.")
