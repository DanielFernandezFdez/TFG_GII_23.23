#Imports
from flask import render_template,request,Blueprint
from app.modelos import *
from app.routes.script_adicionales.importar_exportar import exportar_csv, importar_csv

pantallas_generales = Blueprint('pantallas_generales', __name__,template_folder='templates')


@pantallas_generales.route("/", methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        busqueda = request.form.get('busqueda_inicio')
        libros = Libros.query.filter((Libros.titulo.contains(busqueda)) | (Libros.isbn.contains(busqueda))).all()   
        fecha = fecha_modificacion.query.get_or_404(1)
        return render_template('catalogo.html', libros=libros, fecha=fecha)
    else:
        return render_template("inicio.html")
 
@pantallas_generales.route("/catalogo", methods=['GET', 'POST'])   
def catalogo():
    if request.method == 'POST':
        if 'btn_exportar' in request.form:
            return exportar_csv()
        elif 'btn_buscar' in request.form:
            busqueda = request.form.get('busqueda')
            libros = Libros.query.filter((Libros.titulo.contains(busqueda)) | (Libros.isbn.contains(busqueda))).all()
        elif 'archivo_csv' in request.files:
            archivo = request.files['archivo_csv']
            print('Archivo recibido')
            return importar_csv(archivo)
    else:
        libros = Libros.query.all()
    fecha=fecha_modificacion.query.get_or_404(1)
    return render_template('catalogo.html', libros=libros, fecha=fecha)

@pantallas_generales.route('/informacion/<int:id>', methods=['GET'])
def informacion_libro(id):
    libro = Libros.query.get_or_404(id)
    return render_template('informacion_libro.html', libro=libro)