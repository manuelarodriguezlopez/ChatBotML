from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        session["nombre"] = request.form["nombre"]
        session["cedula"] = request.form["cedula"]
        session["pais_residencia"] = request.form["pais_residencia"]
        session["pais_destino"] = request.form["pais_destino"]
        session["profesion"] = request.form["profesion"]
        session["situacion"] = request.form["situacion"]
        session["estado_civil"] = request.form["estado_civil"]
        return redirect(url_for("chat"))
    return render_template("index.html")



@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "conversacion" not in session:
        session["conversacion"] = []

    if request.method == "POST":
        user_message = request.form["mensaje"]
        respuesta = generar_respuesta(user_message)
        session["conversacion"].append(("Usuario", user_message))
        session["conversacion"].append(("MaquinaIA", respuesta))

    return render_template("chat.html", conversacion=session["conversacion"])


def generar_respuesta(mensaje):
    nombre = session.get("nombre", "")
    edad = session.get("edad", "")
    pais_destino = session.get("pais_destino", "")
    profesion = session.get("profesion", "")
    situacion = session.get("situacion", "")
    estado_civil = session.get("estado_civil", "")

    mensaje = mensaje.lower()

 
    if "hola" in mensaje:
        return f"¡Hola {nombre}! Veo que deseas ingresar a {pais_destino}. Cuéntame, ¿qué te motiva a ir allá?"
    elif "posible" in mensaje or "puedo ingresar" in mensaje:
        return evaluar_solicitud(pais_destino, profesion, situacion)
    elif "gracias" in mensaje:
        return "¡Con gusto! Estoy aquí para ayudarte con tu proceso migratorio."
    else:
        return "Interesante... ¿quieres que te diga las probabilidades de ser aceptado en tu país destino?"


def evaluar_solicitud(pais_destino, profesion, situacion):
    if "ilegal" in situacion.lower():
        return f"Tu solicitud a {pais_destino} podría ser rechazada debido a tu situación migratoria actual."
    elif pais_destino.lower() == "canadá" and "ingeniero" in profesion.lower():
        return "Tienes altas probabilidades de ser aceptado en Canadá. Tu profesión es muy demandada allí."
    elif pais_destino.lower() == "eeuu" and "doctor" in profesion.lower():
        return "Los médicos tienen buenas oportunidades en Estados Unidos, pero asegúrate de tener licencia válida."
    else:
        return f"Tu solicitud a {pais_destino} requiere análisis adicional. Te recomiendo regularizar tu situación y tener todos tus documentos listos."


if __name__ == "__main__":
    app.run(debug=True)
