#Imports
from flask import Flask, render_template,request,redirect,url_for,Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import bcrypt
import csv
from io import StringIO
from datetime import datetime,timezone
from zoneinfo import ZoneInfo


db = SQLAlchemy()
#Modelos
class Libros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), unique=True, nullable=False)
    editorial = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    año_publicacion = db.Column(db.String(50))
    ubicacion_estudio = db.Column(db.String(300))
    url_imagen = db.Column(db.String(300))   

    def __repr__(self):
        return f'<Libros {self.title}>'
    
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(128))

class fecha_modificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ultima_modificacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Método para actualizar la fecha de última modificación
    def actualizar_fecha_modificacion(self):
        FechaUTC=datetime.now(timezone.utc)
        #zona_horaria_local = ZoneInfo("Europe/Madrid")
        #self.ultima_modificacion = FechaUTC.astimezone(zona_horaria_local)
        self.ultima_modificacion = FechaUTC
        db.session.commit()

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
    return db.session.get(Usuario, int(user_id))


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

@app.route('/create_admin')
def create_admin():
    hashed_password = bcrypt.hashpw('1234'.encode('utf-8'), bcrypt.gensalt())
    admin = Usuario(nombre_usuario='UBU', contrasena_hash=hashed_password.decode('utf-8'))
    db.session.add(admin)
    db.session.commit()
    return 'Administrador creado'


#Rutas
@app.route("/")
def inicio():
    return render_template("inicio.html")


    
@app.route("/catalogo", methods=['GET', 'POST'])   
def catalogo():
    if request.method == 'POST':
        if 'btn_exportar' in request.form:
            return exportar_csv()
        elif 'archivo_csv' in request.files:
            archivo = request.files['archivo_csv']
            print('Archivo recibido')
            return importar_csv(archivo)
        else:
            busqueda = request.form.get('busqueda')
            libros = Libros.query.filter((Libros.titulo.contains(busqueda)) | (Libros.isbn.contains(busqueda))).all()
    else:
        libros = Libros.query.all()
    fecha=fecha_modificacion.query.get_or_404(1)
    return render_template('catalogo.html', libros=libros, fecha=fecha)

#Funciones uso de la BD
@app.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar_libro():
    if request.method == 'POST':
        descripcion_defecto = "Descripción no proporcionada"
        nuevo_libro = Libros(
            titulo=request.form['titulo'],
            isbn=request.form['isbn'],
            editorial=request.form['editorial'],
            descripcion=request.form['descripcion'] if request.form['descripcion'] else descripcion_defecto,
            año_publicacion=request.form['año_publicacion'],
            ubicacion_estudio=request.form['ubicacion_estudio'],
            url_imagen=request.form['url_imagen']
        )
        db.session.add(nuevo_libro)
        # Actualizar la fecha de última modificación
        fecha = db.session.get(fecha_modificacion, 1)  # Asumiendo que solo tienes un registro para esto
        if not fecha:
            # Si no existe un registro, crea uno nuevo
            fecha = fecha_modificacion(id=1, ultima_modificacion=datetime.now(timezone.utc))
            db.session.add(fecha)
        fecha.actualizar_fecha_modificacion()
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
        libro.año_publicacion = request.form['año_publicacion']
        libro.ubicacion_estudio = request.form['ubicacion_estudio']
        libro.url_imagen = request.form['url_imagen']
        # Actualizar la fecha de última modificación
        fecha = db.session.get(fecha_modificacion, 1)  # Asumiendo que solo tienes un registro para esto
        if not fecha:
            # Si no existe un registro, crea uno nuevo
            fecha = fecha_modificacion(id=1, ultima_modificacion=datetime.now(timezone.utc))
            db.session.add(fecha)
        fecha.actualizar_fecha_modificacion()
        db.session.commit()
        return redirect(url_for('catalogo'))
    return render_template('editar_libro.html', libro=libro)

@app.route('/eliminar/<int:id>')
@login_required
def eliminar_libro(id):
    libro = Libros.query.get_or_404(id)
    db.session.delete(libro)
    # Actualizar la fecha de última modificación
    fecha = db.session.get(fecha_modificacion, 1)  # Asumiendo que solo tienes un registro para esto
    if not fecha:
        # Si no existe un registro, crea uno nuevo
        fecha = fecha_modificacion(id=1, ultima_modificacion=datetime.now(timezone.utc))
        db.session.add(fecha)
        fecha.actualizar_fecha_modificacion()
    db.session.commit()
    return redirect(url_for('catalogo'))

# Completar y hacer html para sacar toda la informacion de un libro
@app.route('/informacion/<int:id>', methods=['GET'])
def informacion_libro(id):
    libro = Libros.query.get_or_404(id)
    return render_template('informacion_libro.html', libro=libro)

#Funcion de exportar a CSV
def exportar_csv():
    si = StringIO()
    cw = csv.writer(si, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Escribe los encabezados en el archivo CSV
    cw.writerow(['ID', 'Título', 'ISBN', 'Editorial', 'Descripción', 'Año de publicación', 'Ubicación del estudio', 'URL de la imagen'])

    # Obtiene todos los libros de la base de datos
    libros = Libros.query.all()

    # Escribe los datos de cada libro en el archivo CSV
    for libro in libros:
        cw.writerow([libro.id, libro.titulo, libro.isbn, libro.editorial, libro.descripcion, libro.año_publicacion, libro.ubicacion_estudio, libro.url_imagen])

    output = si.getvalue()

    # Crea una respuesta HTTP con el archivo CSV
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=libros.csv"}
    )

def importar_csv(archivo):
    stream = StringIO(archivo.stream.read().decode("UTF-8"), newline=None)
    csv_input = csv.reader(stream)

    # Borrar los datos existentes si es necesario
    Libros.query.delete()

    # Recorrer cada fila del CSV y actualizar la base de datos
    for i, row in enumerate(csv_input):
        if i == 0:
            # Saltar la fila de encabezados
            continue

        # Crear una nueva instancia del modelo Libros por cada fila
        nuevo_libro = Libros(
            titulo=row[1],
            isbn=row[2],
            editorial=row[3],
            descripcion=row[4],
            año_publicacion=row[5],
            ubicacion_estudio=row[6],
            url_imagen=row[7]
        )

        # Agregar el nuevo libro a la sesión de la base de datos
        db.session.add(nuevo_libro)
    # Actualizar la fecha de última modificación
        fecha = db.session.get(fecha_modificacion, 1)  # Asumiendo que solo tienes un registro para esto
        print(fecha.ultima_modificacion)
        if not fecha:
            # Si no existe un registro, crea uno nuevo
            fecha = fecha_modificacion(id=1, ultima_modificacion=datetime.now(timezone.utc))
            db.session.add(fecha)
        fecha.actualizar_fecha_modificacion()

    # Confirmar los cambios en la base de datos
    db.session.commit()

    # Redireccionar o enviar una respuesta adecuada
    return redirect(url_for('catalogo'))





#Ejecución
if __name__ == "__main__":
    app.run(debug=True)