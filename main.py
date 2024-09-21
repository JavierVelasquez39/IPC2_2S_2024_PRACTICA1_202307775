from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename
import requests
from io import BytesIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave_secreta_super_autos_gt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///super_autos_gt.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Auto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idTipoAuto = db.Column(db.Integer, unique=True, nullable=False)
    marca = db.Column(db.String(80), nullable=False)
    modelo = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    precioUnitario = db.Column(db.Float, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(200), nullable=False)
    placa = db.Column(db.String(20), nullable=False)  # Campo placa añadido

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def is_url(string):
    return string.startswith(('http://', 'https://'))

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/registrar_auto', methods=['GET', 'POST'])
@login_required
def registrar_auto():
    if request.method == 'POST':
        idTipoAuto = request.form['idTipoAuto']
        if Auto.query.filter_by(idTipoAuto=idTipoAuto).first():
            flash('El idTipoAuto ya existe', 'error')
        else:
            imagen_url = request.form['imagen']
            
            if is_url(imagen_url):
                # Si es una URL, la usamos directamente
                imagen_path = imagen_url
            else:
                # Si no es una URL, asumimos que es un archivo subido
                imagen = request.files['imagen']
                if imagen and allowed_file(imagen.filename):
                    filename = secure_filename(imagen.filename)
                    imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    imagen.save(imagen_path)
                    imagen_path = url_for('uploaded_file', filename=filename)
                else:
                    imagen_path = url_for('static', filename='default-car.png')
            
            nuevo_auto = Auto(
                idTipoAuto=idTipoAuto,
                marca=request.form['marca'],
                modelo=request.form['modelo'],
                descripcion=request.form['descripcion'],
                precioUnitario=float(request.form['precioUnitario']),
                cantidad=int(request.form['cantidad']),
                imagen=imagen_path,
                placa=request.form['placa']  # Asignando el valor de placa
            )
            db.session.add(nuevo_auto)
            db.session.commit()
            flash('Auto registrado con éxito', 'success')
            return redirect(url_for('listar_autos'))
    return render_template('registrar_auto.html')

@app.route('/listar_autos')
@login_required
def listar_autos():
    autos = Auto.query.all()
    return render_template('listar_autos.html', autos=autos)

@app.route('/eliminar_auto/<int:id>', methods=['POST'])
@login_required
def eliminar_auto(id):
    auto = Auto.query.get_or_404(id)
    db.session.delete(auto)
    db.session.commit()
    flash('Auto eliminado con éxito', 'success')
    return redirect(url_for('listar_autos'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Usuario.query.filter_by(username='empleado').first():
            nuevo_usuario = Usuario(username='empleado', password=generate_password_hash('$uper4utos#'))
            db.session.add(nuevo_usuario)
            db.session.commit()
    app.run(debug=True)










