from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from flask import jsonify
import app.Funciones_Auxiliares.funciones_webscraping as fw
from app.modelos import db, Libros, fecha_modificacion, Libros_automaticos, EstadisticasPorMes

class ListadoLibros(Resource):
    
    def get(self):
        libros = Libros.query.all()
        return jsonify(
            [
                {
                    "id": libro.id,
                    "titulo": libro.titulo,
                    "isbn": libro.isbn,
                    "editorial": libro.editorial,
                    "descripcion": libro.descripcion,
                    "anyo_publicacion": libro.anyo_publicacion,
                    "puntuacion": libro.puntuacion,
                    "ubicacion_estudio": libro.ubicacion_estudio,
                    "url_imagen": libro.url_imagen,
                }
                for libro in libros
            ]
        )


class BusquedaLibro(Resource):

    def get(self, busqueda):
        libros = Libros.query.filter(
            (Libros.titulo.contains(busqueda)) | (Libros.isbn.contains(busqueda))
        ).all()
        return jsonify(
            [
                {
                    "id": libro.id,
                    "titulo": libro.titulo,
                    "isbn": libro.isbn,
                    "editorial": libro.editorial,
                    "descripcion": libro.descripcion,
                    "anyo_publicacion": libro.anyo_publicacion,
                    "puntuacion": libro.puntuacion,
                    "ubicacion_estudio": libro.ubicacion_estudio,
                    "url_imagen": libro.url_imagen,
                }
                for libro in libros
            ]
        )


class InfoLibroID(Resource):

    def get(self, id):
        libro = Libros.query.get_or_404(id)
        libro.visitas_mensuales = libro.visitas_mensuales + 1
        libro.visitas_totales = libro.visitas_totales + 1
        db.session.commit()
        return jsonify(
            {
                "id": libro.id,
                "titulo": libro.titulo,
                "isbn": libro.isbn,
                "editorial": libro.editorial,
                "descripcion": libro.descripcion,
                "anyo_publicacion": libro.anyo_publicacion,
                "puntuacion": libro.puntuacion,
                "ubicacion_estudio": libro.ubicacion_estudio,
                "url_imagen": libro.url_imagen,
                "puntuacion_masculino_generico": libro.puntuacion_masculino_generico,
                "puntuacion_menores": libro.puntuacion_menores,
                "puntuacion_adultos": libro.puntuacion_adultos,
                "puntuacion_ubicacion": libro.puntuacion_ubicacion,
                "puntuacion_actividades": libro.puntuacion_actividades
            }
        )


class AgregarLibro(Resource):
    @jwt_required()
    def post(self): 
        data = request.get_json()
        nuevo_libro = Libros(
            titulo=data["titulo"],
            isbn=data["isbn"],
            editorial=data["editorial"],
            descripcion=data["descripcion"],
            anyo_publicacion=data["anyo_publicacion"] ,
            puntuacion=data["puntuacion"] ,
            ubicacion_estudio=data["ubicacion_estudio"],
            url_imagen=data["url_imagen"],
            puntuacion_masculino_generico=data["puntuacion_masculino_generico"],
            puntuacion_menores=data["puntuacion_menores"],
            puntuacion_adultos=data["puntuacion_adultos"],
            puntuacion_ubicacion=data["puntuacion_ubicacion"],
            puntuacion_actividades=data["puntuacion_actividades"]
            
        )
        db.session.add(nuevo_libro)
        fecha_modificacion.actualizar_fecha_modificacion()
        db.session.commit()
        return jsonify({"mensaje": "Libro agregado exitosamente", "id": nuevo_libro.id})


class borrarLibro(Resource):
    @jwt_required()
    def delete(self, id):
        libro = Libros.query.get_or_404(id)
        db.session.delete(libro)
        fecha_modificacion.actualizar_fecha_modificacion()
        db.session.commit()
        return jsonify({"mensaje": "Libro eliminado exitosamente"})


class editarLibro(Resource):
    @jwt_required()
    def put(self, id):
        libro = Libros.query.get_or_404(id)
        data = request.get_json()
        libro.titulo = data.get("titulo", libro.titulo)
        libro.isbn = data.get("isbn", libro.isbn)
        libro.editorial = data.get("editorial", libro.editorial)
        libro.descripcion = data.get("descripcion", libro.descripcion)
        libro.anyo_publicacion = data.get("anyo_publicacion", libro.anyo_publicacion)
        libro.puntuacion = data.get("puntuacion", libro.puntuacion)
        libro.ubicacion_estudio = data.get("ubicacion_estudio", libro.ubicacion_estudio)
        libro.url_imagen = data.get("url_imagen", libro.url_imagen)
        libro.puntuacion_masculino_generico = data.get("puntuacion_masculino_generico", libro.puntuacion_masculino_generico)
        libro.puntuacion_menores = data.get("puntuacion_menores", libro.puntuacion_menores)
        libro.puntuacion_adultos = data.get("puntuacion_adultos", libro.puntuacion_adultos)
        libro.puntuacion_ubicacion = data.get("puntuacion_ubicacion", libro.puntuacion_ubicacion)
        libro.puntuacion_actividades = data.get("puntuacion_actividades", libro.puntuacion_actividades)
        fecha_modificacion.actualizar_fecha_modificacion()
        db.session.commit()
        return jsonify({"mensaje": "Libro editado exitosamente"})


class Fecha(Resource):

    def get(self):
        fechas = fecha_modificacion.query.get_or_404(1)
        return jsonify(
            {
                "id": fechas.id,
                "dato": fechas.ultima_modificacion,
            }
        )


class buscarLibroAutomatico(Resource):
    @jwt_required()
    def post(self):
        db.session.query(Libros_automaticos).delete()
        db.session.commit()
        data = request.get_json()
        libros = fw.buscar_libro(data["elemento"])
        for libro in libros:
            if libro[2] == True:
                nuevo_libro = Libros_automaticos(
                    auto_id=libro[0],
                    logo=libro[1],
                    disponible=libro[2],
                    titulo=libro[3],
                    isbn=libro[4] + "," + libro[5],
                    editorial=libro[6],
                    anyo_publicacion=libro[7],
                    descripcion=libro[8],
                    url_imagen=libro[9],
                )
            else:
                if libro[2] == True:
                    nuevo_libro = Libros_automaticos(
                        auto_id=libro[0],
                        logo=libro[1],
                        disponible=libro[2],
                )
            db.session.add(nuevo_libro)
            db.session.commit()
        return listarLibrosAutomaticos.get(self)



class borrarTabla(Resource):
    @jwt_required()
    def delete(self):
        print("No tan rápido")
        #EstadisticasPorMes.__table__.drop(db.engine)
        #db.session.commit()


class listarLibrosAutomaticos(Resource):
        @jwt_required()
        def get(self):
            libros = Libros_automaticos.query.all()
            return jsonify(
                [
                    {
                        "auto_id": libro.auto_id,
                        "logo": libro.logo,
                        "titulo": libro.titulo,
                        "disponible": libro.disponible,
                        "isbn": libro.isbn,
                        "editorial": libro.editorial,
                        "descripcion": libro.descripcion,
                        "anyo_publicacion": libro.anyo_publicacion,
                        "url_imagen": libro.url_imagen,
                    }
                    for libro in libros
                ]
            )