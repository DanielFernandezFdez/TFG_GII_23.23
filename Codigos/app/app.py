#Imports
from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt

db = SQLAlchemy()
#Modelos
class Libros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), unique=True, nullable=False)
    editorial = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    genero = db.Column(db.String(50))
    portada = db.Column(db.String(100))  # URL de la imagen de portada

    def __repr__(self):
        return f'<Libros {self.title}>'
    
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(128))

def creacion():
    #Instancia de Flask
    app=Flask(__name__)
    app.secret_key = 'v2s7*fp(z8WUr1hCUR({"-Q|yG5muk`?Nd|Ut@cz2E:ZJ[}0/['  # Clave secreta para las sesiones
    #Configuración de la BD
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Libros.db' #Ruta de la BD
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = creacion()

#Operaciones de Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # La ruta que redirige para el login




@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        contrasena = request.form['password']
        user = Usuario.query.filter_by(nombre_usuario=usuario).first()
        if user and bcrypt.checkpw(contrasena.encode('utf-8'), user.contrasena_hash.encode('utf-8')):
            login_user(user)
            return redirect(url_for('catalogo'))
        else:
            error = "Login fallido. Por favor, intenta de nuevo."
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('inicio'))

#@app.route('/create_admin')
#def create_admin():
 #   hashed_password = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt())
  #  admin = Usuario(nombre_usuario='UBU', contrasena_hash=hashed_password.decode('utf-8'))
   # db.session.add(admin)
    #db.session.commit()
    #return 'Administrador creado'


#Rutas
@app.route("/")
def inicio():
    return render_template("inicio.html")
    
@app.route("/catalogo", methods=['GET', 'POST'])   
def catalogo():
    if request.method == 'POST':
        busqueda = request.form.get('busqueda')
        libros = Libros.query.filter((Libros.titulo.contains(busqueda)) | (Libros.isbn.contains(busqueda))).all()
    else:
        libros = Libros.query.all()
    return render_template('catalogo.html', libros=libros)

    

#Funciones uso de la BD
@app.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar_libro():
    if request.method == 'POST':
        nuevo_libro = Libros(
            titulo=request.form['titulo'],
            isbn=request.form['isbn'],
            editorial=request.form['editorial'],
            descripcion=request.form['descripcion'],
            genero=request.form['genero'],
            portada=request.form['portada']
        )
        db.session.add(nuevo_libro)
        db.session.commit()
        return redirect(url_for('catalogo'))
    return render_template('agregar_libro.html')

@app.route('/edicion/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_libro(id):
    libro = Libros.query.get_or_404(id)
    if request.method == 'POST':
        libro.titulo = request.form['titulo']
        libro.isbn = request.form['isbn']
        libro.editorial = request.form['editorial']
        libro.descripcion = request.form['descripcion']
        libro.genero = request.form['genero']
        libro.portada = request.form['portada']
        db.session.commit()
        return redirect(url_for('catalogo'))
    return render_template('editar_libro.html', libro=libro)

@app.route('/eliminar/<int:id>')
@login_required
def eliminar_libro(id):
    libro = Libros.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()
    return redirect(url_for('catalogo'))


#@app.route('/informacion/<int:id>', methods=['GET'])
#def masinfo_libro(id):
#    libro = Libros.query.get_or_404(id)
#    
#    return render_template('informacion_libro.html', libro=libro)




#Ejecución
if __name__ == "__main__":
    app.run(debug=True)