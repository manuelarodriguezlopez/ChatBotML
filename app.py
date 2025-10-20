from flask import Flask, render_template, request, redirect, url_for, session
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import User, get_user,users
from urllib.parse import urlparse
from forms import LoginForm,SignupForm

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = LoginManager(app)


@app.route("/", methods=["GET", "POST"])
def index():
    # Si el usuario no está autenticado, redirigir al login (primer paso de acceso)
    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    if request.method == "POST":
        session["nombre"] = request.form.get("nombre")
        session["cedula"] = request.form.get("cedula")
        session["pais_residencia"] = request.form.get("pais_residencia")
        session["pais_destino"] = request.form.get("pais_destino")
        session["profesion"] = request.form.get("profesion")
        session["situacion"] = request.form.get("situacion")
        session["estado_civil"] = request.form.get("estado_civil")
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


@login_manager.user_loader
def load_user(user_id):
    for user in users:
        if user.id == int(user_id):
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user(form.email.data)
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login_form.html', title='Sign In', form=form)

@app.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        # Creamos el usuario y lo guardamos
        user = User(len(users) + 1, name, email, password)
        users.append(user)
        # Dejamos al usuario logueado
        login_user(user, remember=True)
        next_page = request.args.get('next', None)
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("signup_form.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
