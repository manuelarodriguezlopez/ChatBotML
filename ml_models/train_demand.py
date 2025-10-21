import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import os

def train_model():
    # Cargar el dataset
    data_path = os.path.join("data", "produccion_kefir.csv")
    df = pd.read_csv(data_path)

    # Variables predictoras y objetivo
    X = df[['cantidad_producida', 'precio_unitario', 'costo_produccion', 'campaña_marketing']]
    y = df['cantidad_vendida']

    # Dividir los datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Entrenar modelo
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Guardar modelo entrenado
    model_path = os.path.join("ml_models", "demand_model.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)

    print("✅ Modelo entrenado y guardado correctamente en:", model_path)

# Si se ejecuta directamente desde la terminal
if __name__ == "__main__":
    train_model()
