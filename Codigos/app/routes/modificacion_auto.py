#Imports
from flask import render_template,request,redirect,url_for,Blueprint
from app.modelos import *
from app.__init__ import*
from flask_login import login_required
import app.routes.script_adicionales.funciones_webscraping as fw


modificacion_auto = Blueprint('modificacion_auto', __name__,template_folder='templates')

@modificacion_auto.route('/agregar_auto', methods=['GET', 'POST'])
@login_required
def agregar_auto():
    db.session.query(Libros_automaticos).delete()
    db.session.commit()
    if request.method == 'POST':
        if 'btn_buscar_web' in request.form:
            busqueda = request.form.get('busqueda_web')
            libros = fw.buscar_libro(busqueda)
            for libro in libros:
                if libro[2]==True:
                    nuevo_libro = Libros_automaticos(
                    auto_id=libro[0],
                    titulo=libro[3],
                    isbn=libro[4]+','+libro[5],
                    editorial=libro[6],
                    año_publicacion=libro[7],
                    descripcion=libro[8],
                    url_imagen=libro[9]
                    )
                    db.session.add(nuevo_libro)
                    db.session.commit()
        return render_template('agregar_auto.html', libros=libros)
    return render_template('agregar_auto.html')
    
    
@modificacion_auto.route('/edicion_auto/<string:auto_id>', methods=['GET', 'POST'])
@login_required
def editar_libro_auto(auto_id):
    libro = Libros_automaticos.query.get_or_404(auto_id)
    if request.method == 'POST':
        descripcion_defecto = "Descripción no proporcionada"
        estudio_defecto = ""
        nuevo_libro = Libros(
            titulo=request.form['titulo'],
            isbn=request.form['isbn'],
            editorial=request.form['editorial'],
            descripcion=request.form['descripcion'] if request.form['descripcion'] else descripcion_defecto,
            año_publicacion=request.form['año_publicacion'],
            puntuacion=request.form['puntuacion'],
            ubicacion_estudio=request.form['ubicacion_estudio'] if request.form['ubicacion_estudio'] else estudio_defecto,
            url_imagen=request.form['url_imagen']
        )
        db.session.add(nuevo_libro)
        db.session.query(Libros_automaticos).delete()
        fecha_modificacion.actualizar_fecha_modificacion()
        db.session.commit()
        return redirect(url_for('pantallas_generales.catalogo'))
    return render_template('editar_libro.html', libro=libro)


@modificacion_auto.route('/combinacion_auto', methods=['GET', 'POST'])
@login_required
def combinacion_auto():
    libros = Libros_automaticos.query.all()
    titulo=[]
    isbn=[]
    editorial=[]
    descripcion=[]
    año_publicacion=[]
    url_imagen=[]
    for libro in libros:
        titulo.append(libro.titulo)
        isbn.append(libro.isbn)
        editorial.append(libro.editorial)
        descripcion.append(libro.descripcion)
        año_publicacion.append(libro.año_publicacion)
        url_imagen.append(libro.url_imagen)
        
    if request.method == 'POST':
        descripcion_defecto = "Descripción no proporcionada"
        estudio_defecto = ""
        nuevo_libro = Libros(
            titulo=request.form['titulo'],
            isbn=request.form['isbn'],
            editorial=request.form['editorial'],
            descripcion=request.form['descripcion'] if request.form['descripcion'] else descripcion_defecto,
            año_publicacion=request.form['año_publicacion'],
            puntuacion=request.form['puntuacion'],
            ubicacion_estudio=request.form['ubicacion_estudio'] if request.form['ubicacion_estudio'] else estudio_defecto,
            url_imagen=request.form['url_imagen']
        )
        db.session.add(nuevo_libro)
        db.session.query(Libros_automaticos).delete()
        fecha_modificacion.actualizar_fecha_modificacion()
        db.session.commit()
        return redirect(url_for('pantallas_generales.catalogo'))
    return render_template('combinacion_auto.html', titulo=titulo, isbn=isbn, editorial=editorial, descripcion=descripcion, año_publicacion=año_publicacion, url_imagen=url_imagen)