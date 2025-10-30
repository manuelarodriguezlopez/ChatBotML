import pandas as pd
import os

# ---------------------------------------------------------
# Datasheet mejorado con clasificación por tipo de fruta
# ---------------------------------------------------------

data = [
    {
        "Tecnica_recomendada": "Maceración lenta",
        "Tipo_fruta_adecuado": "blanda",
        "Rango_cantidad_ml": "100-800",
        "Descripcion": "Extracción pasiva ideal para frutas blandas o aromáticas.",
        "Implementacion_detallada": "Trocea frutas como mango, fresa o melón. Mantén el recipiente cerrado y remueve cada 2 horas. Ideal para lotes pequeños.",
        "Tiempo_estimado": "10-12 horas",
        "Temperatura_optima": "24–26 °C",
        "Herramientas": "Frascos de vidrio, espátula de silicona, colador fino.",
        "Recomendaciones_finales": "Evitar exposición al sol y exceso de movimiento."
    },
    {
        "Tecnica_recomendada": "Prensado en frío",
        "Tipo_fruta_adecuado": "fibrosa",
        "Rango_cantidad_ml": "300-1200",
        "Descripcion": "Técnica mecánica ideal para frutas fibrosas como piña o guayaba.",
        "Implementacion_detallada": "Lava, trocea y prensa la fruta a baja velocidad. Filtra inmediatamente para evitar oxidación.",
        "Tiempo_estimado": "30-45 minutos",
        "Temperatura_optima": "18–25 °C",
        "Herramientas": "Prensa lenta (<50 rpm), bandeja colectora.",
        "Recomendaciones_finales": "Evita el recalentamiento del jugo por fricción."
    },
    {
        "Tecnica_recomendada": "Difusión osmótica",
        "Tipo_fruta_adecuado": "fibrosa",
        "Rango_cantidad_ml": "500-2000",
        "Descripcion": "Método controlado para extraer azúcares de frutas densas o tropicales.",
        "Implementacion_detallada": "Corta la fruta (como papaya o piña) en cubos y colócala en agua a 38 °C durante 4 h. Agita suavemente cada 30 minutos.",
        "Tiempo_estimado": "3-5 horas",
        "Temperatura_optima": "35–40 °C",
        "Herramientas": "Baño térmico, agitador suave, termómetro.",
        "Recomendaciones_finales": "Ideal para grandes volúmenes de frutas tropicales."
    },
    {
        "Tecnica_recomendada": "Fermentación previa",
        "Tipo_fruta_adecuado": "cítrica",
        "Rango_cantidad_ml": "400-1500",
        "Descripcion": "Proceso biológico controlado que genera base fermentada para kéfir.",
        "Implementacion_detallada": "Usa naranja o maracuyá, mezcla con agua y deja fermentar 24 h. Luego añade granos de kéfir y fermenta 48 h adicionales.",
        "Tiempo_estimado": "48-72 horas",
        "Temperatura_optima": "25–28 °C",
        "Herramientas": "Frascos con válvula, termómetro.",
        "Recomendaciones_finales": "Controla el pH (3.5–4.2) durante la fermentación."
    },
    {
        "Tecnica_recomendada": "Extracción térmica",
        "Tipo_fruta_adecuado": "seca",
        "Rango_cantidad_ml": "600-2000",
        "Descripcion": "Utiliza calor controlado para liberar azúcares en frutas con baja humedad.",
        "Implementacion_detallada": "Hidrata frutas secas (como higo o uva pasa), luego calienta a 65 °C por 45 min y filtra.",
        "Tiempo_estimado": "1 hora",
        "Temperatura_optima": "60–70 °C",
        "Herramientas": "Baño maría, termómetro, filtro textil.",
        "Recomendaciones_finales": "No exceder los 70 °C para evitar caramelización."
    }
]

df = pd.DataFrame(data)
os.makedirs("data", exist_ok=True)
output_path = "data/enhanced_techniques_datasheet.csv"
df.to_csv(output_path, index=False, encoding="utf-8")

print(f"Datasheet avanzado generado en: {os.path.abspath(output_path)}")
print(df.head())
