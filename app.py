
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'hj-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hj_extension_db_user:pwjDHoky6jii4xZHVJAgLHyw2sl0N3bt@dpg-cvulnovgi27c73agva80-a/hj_extension_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    licencia = db.Column(db.String(64), unique=True, nullable=False)
    estado = db.Column(db.String(10), nullable=False, default='activo')

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']
        if usuario == 'hjadmin333' and clave == 'hernan2003':
            session['admin'] = True
            return redirect(url_for('panel'))
        else:
            return render_template('login.html', error='Credenciales inválidas')
    return render_template('login.html')

@app.route('/admin')
def panel():
    if not session.get('admin'):
        return redirect('/')
    usuarios = Usuario.query.all()
    return render_template('panel.html', usuarios=usuarios)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

@app.route('/cambiar_estado/<int:id>')
def cambiar_estado(id):
    if not session.get('admin'):
        return redirect('/')
    usuario = Usuario.query.get(id)
    if usuario:
        usuario.estado = 'activo' if usuario.estado == 'inactivo' else 'inactivo'
        db.session.commit()
    return redirect('/admin')

@app.route('/eliminar_usuario/<int:id>')
def eliminar_usuario(id):
    if not session.get('admin'):
        return redirect('/')
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
    return redirect('/admin')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

