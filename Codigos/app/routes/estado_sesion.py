from flask import render_template,request,redirect,url_for,Blueprint
from flask_login import login_user, logout_user
from app.modelos import *
import bcrypt

estado_sesion = Blueprint('estado_sesion', __name__,template_folder='templates')


@estado_sesion.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        contrasena = request.form['password']
        user =  Usuario.query.filter_by(nombre_usuario=usuario).first()
        if user and bcrypt.checkpw(contrasena.encode('utf-8'), user.contrasena_hash.encode('utf-8')):
            login_user(user)
            return redirect(url_for('pantallas_generales.catalogo'))
        else:
            error = "Login fallido. Por favor, intenta de nuevo."
            return render_template('login.html', error=error)
    return render_template('login.html')


@estado_sesion.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('pantallas_generales.inicio'))





