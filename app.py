from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from extensions import db
from models import User, get_user_by_email
from urllib.parse import urlparse
from datetime import timedelta
import os
import pickle
import pandas as pd
import numpy as np
import requests

def create_app():
    app = Flask(__name__)

    # ---------------- CONFIGURACIÓN GENERAL ----------------
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbotml.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_PERMANENT'] = False
    app.permanent_session_lifetime = timedelta(minutes=30)

    # ---------------- CONFIGURAR reCAPTCHA ----------------
    RECAPTCHA_SITE_KEY = "6LcGqvErAAAAAKvvIVRi44w63x6oMf67AQb8aS4o"
    RECAPTCHA_SECRET_KEY = "6LcGqvErAAAAAKn3xmx5Yh1FENn3D8Tbko65m2xq"

    # ---------------- INICIALIZAR BASE Y LOGIN ----------------
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # =========================================================
    # CARGA DEL MODELO DE MACHINE LEARNING
    # =========================================================
    MODEL_PATH = "models/sugar_kef_model.pkl"
    DATASET_PATH = "techniques_datasheet.csv"

    sugar_model = None
    encoder = None
    tech_df = pd.DataFrame()

    try:
        with open(MODEL_PATH, "rb") as f:
            sugar_model, encoder = pickle.load(f)
        tech_df = pd.read_csv(DATASET_PATH)
        print("✅ Modelo ML y datasheet cargados correctamente.")
    except Exception as e:
        print(f"⚠️ Error cargando modelo o datasheet: {e}")

    # =========================================================
    # RUTAS DEL SISTEMA
    # =========================================================

    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('login'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')

    # ---------------- LOGIN ----------------
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            # Validar reCAPTCHA
            recaptcha_response = request.form.get('g-recaptcha-response')
            payload = {'secret': RECAPTCHA_SECRET_KEY, 'response': recaptcha_response}
            result = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload).json()

            if not result.get('success'):
                flash('Verificación reCAPTCHA fallida. Intenta nuevamente.', 'danger')
                return redirect(url_for('login'))

            # Verificar usuario
            user = get_user_by_email(email)
            if user is None or not user.check_password(password):
                flash('Correo o contraseña incorrectos', 'danger')
                return redirect(url_for('login'))

            login_user(user, remember=False)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('dashboard')
            return redirect(next_page)

        return render_template('login.html', site_key=RECAPTCHA_SITE_KEY)

    # ---------------- REGISTRO ----------------
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            name = request.form.get('nombre')
            email = request.form.get('email')
            password = request.form.get('password')

            if get_user_by_email(email):
                flash('Ya existe una cuenta con ese email.', 'warning')
                return redirect(url_for('register'))

            user = User(name=name, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=False)
            return redirect(url_for('dashboard'))

        return render_template('register.html')

    # ---------------- LOGOUT ----------------
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Sesión cerrada correctamente', 'info')
        return redirect(url_for('login'))

    # ---------------- EMPRESA ----------------
    @app.route('/empresa')
    @login_required
    def empresa():
        return render_template('empresa.html')

    # ---------------- PEDIDO ----------------
    @app.route('/pedido', methods=['GET', 'POST'])
    @login_required
    def pedido():
        if request.method == 'POST':
            nombre = request.form['nombre']
            correo = request.form['correo']
            producto = request.form['producto']
            cantidad = request.form['cantidad']
            direccion = request.form['direccion']
            flash('Pedido registrado con éxito', 'success')
            return redirect(url_for('dashboard'))
        return render_template('pedido.html')

    # =========================================================
    # PREDICCIÓN DE CALIDAD Y TÉCNICA
    # =========================================================
    @app.route('/predict', methods=['GET', 'POST'])
    @login_required
    def predict():
        frutas = [
            "manzana", "pera", "uva", "mango", "fresa", "piña", "banano", "kiwi", "papaya", "melón",
            "sandía", "cereza", "maracuyá", "guayaba", "mora", "naranja", "limón", "mandarina", "coco",
            "durazno", "granadilla", "toronja", "guanábana", "pitahaya", "lulo", "arándano", "frambuesa",
            "tamarindo", "pomarrosa", "uchuva", "cacao", "aguacate", "mamey", "chontaduro", "higo",
            "ciruela", "níspero", "mangostino", "zapote", "carambola", "melocotón", "mango tommy",
            "pera de agua", "uva isabelina", "noni", "guayabo", "caimito", "pitanga", "cereza negra", "mora de castilla"
        ]

        if request.method == 'POST':
            fruta = request.form['fruta']
            cantidad = float(request.form['cantidad'])
            azucar = float(request.form.get('azucar', 0))
            temperatura = float(request.form.get('temperatura', 25))
            tiempo = float(request.form.get('tiempo', 12))
            madurez = request.form.get('madurez', 'maduro')
            congelado = request.form.get('congelado', 'no')
            metodo = request.form.get('metodo', 'manual')

            # ====== MAPEAR MADUREZ A VALOR NUMÉRICO ======
            madurez_map = {"verde": 0, "maduro": 1, "muy_maduro": 2}
            madurez_val = madurez_map.get(madurez, 1)

            # ====== SIMULACIÓN DE CALIDAD ======
            calidad = 100
            calidad -= abs(temperatura - 26) * 2
            calidad -= abs(tiempo - 12) * 3
            calidad -= abs(azucar - 10) * 1.5
            if madurez_val < 1:
                calidad -= 10
            if congelado.lower() in ["sí", "si"]:
                calidad -= 10

            calidad = max(0, min(100, calidad))

            # ====== RECOMENDACIÓN DE TÉCNICA ======
            tecnica_predicha = None
            tecnica_info = None
            if calidad < 70:
                df = pd.read_csv('techniques_datasheet.csv')
                tecnica_predicha = np.random.choice(df["Tecnica_recomendada"])
                tecnica_info = df[df["Tecnica_recomendada"] == tecnica_predicha].iloc[0].to_dict()

            # ====== RENDERIZAR RESULTADO ======
            return render_template(
                'result.html',
                fruta=fruta,
                cantidad=cantidad,
                azucar=azucar,
                temperatura=temperatura,
                tiempo=tiempo,
                madurez=madurez,
                congelado=congelado,
                metodo=metodo,
                calidad=calidad,
                tecnica_predicha=tecnica_predicha,
                tecnica_info=tecnica_info
            )

        return render_template('predict.html', frutas=frutas)
    
    return app


# =========================================================
# EJECUCIÓN
# =========================================================
app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
