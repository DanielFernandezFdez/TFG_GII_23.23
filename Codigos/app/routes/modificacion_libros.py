from flask import render_template,request,redirect,url_for,Blueprint
from flask_login import login_required
from app.modelos import *
from app.__init__ import *

modificacion_libros = Blueprint('modificacion_libros', __name__,template_folder='templates')


@modificacion_libros.route('/agregar', methods=['GET', 'POST'])
@login_required
def agregar_libro():
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
        fecha_modificacion.actualizar_fecha_modificacion()
        db.session.commit()
        return redirect(url_for('pantallas_generales.catalogo'))
    return render_template('agregar_libro.html')


@modificacion_libros.route('/edicion/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_libro(id):
    libro = Libros.query.get_or_404(id)
    if request.method == 'POST':
        libro.titulo = request.form['titulo']
        libro.isbn = request.form['isbn']
        libro.editorial = request.form['editorial']
        libro.descripcion = request.form['descripcion']
        libro.año_publicacion = request.form['año_publicacion']
        libro.puntuacion = request.form['puntuacion']
        libro.ubicacion_estudio = request.form['ubicacion_estudio']
        libro.url_imagen = request.form['url_imagen']
        
        fecha_modificacion.actualizar_fecha_modificacion()
        db.session.commit()
        return redirect(url_for('pantallas_generales.catalogo'))
    return render_template('editar_libro.html', libro=libro)

@modificacion_libros.route('/eliminar/<int:id>')
@login_required
def eliminar_libro(id):
    libro = Libros.query.get_or_404(id)
    db.session.delete(libro)
    
    fecha_modificacion.actualizar_fecha_modificacion()
    db.session.commit()
    return redirect(url_for('pantallas_generales.catalogo'))