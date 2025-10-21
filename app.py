from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from extensions import db
from models import User, get_user_by_email
from urllib.parse import urlparse
from datetime import timedelta
import os
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

    # ---------------- RUTA PRINCIPAL ----------------
    @app.route('/')
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
            payload = {
                'secret': RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
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

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
