import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
import os

# ----------------------------------------------
# MODELO SIMPLIFICADO: FRUTA + CANTIDAD
# ----------------------------------------------

# Cargar dataset de técnicas
df = pd.read_csv("techniques_datasheet.csv")

# Lista base de frutas
frutas = [
    "manzana", "pera", "uva", "mango", "fresa", "piña", "banano", "kiwi", "papaya", "melón",
    "sandía", "cereza", "maracuyá", "guayaba", "mora", "naranja", "limón", "mandarina", "coco",
    "durazno", "granadilla", "toronja", "guanábana", "pitahaya", "lulo", "arándano", "frambuesa",
    "tamarindo", "pomarrosa", "uchuva", "cacao", "aguacate", "mamey", "chontaduro", "higo",
    "ciruela", "níspero", "mangostino", "zapote", "carambola", "melocotón", "mango tommy",
    "pera de agua", "uva isabelina", "noni", "guayabo", "caimito", "pitanga", "cereza negra", "mora de castilla"
]

# Generar datos simulados coherentes
np.random.seed(42)
X = []
y = []
for fruta in frutas:
    for _ in range(10):
        cantidad = np.random.randint(100, 2000)
        tecnica = np.random.choice(df["Tecnica_recomendada"])
        X.append([fruta, cantidad])
        y.append(tecnica)

X_df = pd.DataFrame(X, columns=["Fruta", "Cantidad"])
y_df = pd.Series(y, name="Tecnica")

# Codificar fruta
encoder = OneHotEncoder(handle_unknown='ignore')
X_encoded = encoder.fit_transform(X_df[["Fruta"]]).toarray()
X_final = np.concatenate([X_encoded, X_df[["Cantidad"]].values], axis=1)

# Entrenar modelo
model = RandomForestClassifier(n_estimators=120, random_state=42)
model.fit(X_final, y_df)

# Crear carpeta y guardar modelo junto al encoder
os.makedirs("models", exist_ok=True)
with open("models/sugar_kef_model.pkl", "wb") as f:
    pickle.dump((model, encoder), f)

print("--------------------------------------------------------")
print("Modelo y codificador entrenados y guardados correctamente en: models/sugar_kef_model.pkl")
print("--------------------------------------------------------")
