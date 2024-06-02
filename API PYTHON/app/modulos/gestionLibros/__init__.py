from flask import Blueprint
from flask_restful import Api

from .recursosLibros import ListadoLibros, BusquedaLibro, InfoLibroID, AgregarLibro, borrarLibro, editarLibro, Fecha, buscarLibroAutomatico, borrarTabla, listarLibrosAutomaticos, crearFecha

gestion_libros_bp = Blueprint('gestion_libros', __name__)
api = Api(gestion_libros_bp)


api.add_resource(ListadoLibros, '/listadoLibros')
api.add_resource(BusquedaLibro, '/busquedaLibro/<string:busqueda>')
api.add_resource(InfoLibroID, '/infoLibro/<int:id>')
api.add_resource(AgregarLibro, '/agregarLibro')
api.add_resource(borrarLibro, '/borrarLibro/<int:id>')
api.add_resource(editarLibro, '/editarLibro/<int:id>')
api.add_resource(Fecha, '/fecha')
api.add_resource(buscarLibroAutomatico, '/buscarLibroAutomatico')
api.add_resource(borrarTabla, '/borrarTabla')
api.add_resource(listarLibrosAutomaticos, '/listarLibrosAutomaticos')
api.add_resource(crearFecha, '/crearFecha')
