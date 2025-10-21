from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "clave_secreta_segura"  # Necesaria para manejar sesiones y mensajes

# Simulación de base de datos temporal
usuarios = {
    "admin@example.com": {"nombre": "Admin", "password": "1234"}
}

# ---------------- RUTA LOGIN -----------------
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = 'remember' in request.form  # Checkbox

        # Verificación del usuario
        if email in usuarios and usuarios[email]['password'] == password:
            session['usuario'] = usuarios[email]['nombre']
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')

    return render_template('login.html')

# ---------------- RUTA REGISTRO -----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        if email in usuarios:
            flash('El usuario ya existe', 'warning')
        else:
            usuarios[email] = {'nombre': nombre, 'password': password}
            flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

# ---------------- RUTA DASHBOARD -----------------
@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# ---------------- CERRAR SESIÓN -----------------
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
