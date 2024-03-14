from functools import wraps
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask_cors import CORS
import funciones_webscraping as fw


db = SQLAlchemy()


X_API_KEY = 'clave'  #! Clave API secreta  necesario exportar a variable de entorno


def requerir_api_key(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        api_key = request.headers.get("X_API_KEY")
        if api_key and api_key == X_API_KEY:
            return f(*args, **kwargs)
        else:
            #return jsonify({"error": "Acceso denegado: clave API inválida",
             #               "valor obtenido": request.headers.get("X_API_KEY")})
             return f(*args, **kwargs)

    return decorada


# Modelos
class Libros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), unique=True, nullable=False)
    editorial = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    anyo_publicacion = db.Column(db.String(50))
    puntuacion = db.Column(db.Integer, nullable=True)
    ubicacion_estudio = db.Column(db.String(300))
    url_imagen = db.Column(db.String(300))

    def __repr__(self):
        return f"<Libros {self.titulo}>"


class Libros_automaticos(db.Model):
    auto_id = db.Column(db.String(100), primary_key=True)
    logo = db.Column(db.String(300))
    titulo = db.Column(db.String(100))
    isbn = db.Column(db.String(100))
    editorial = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    anyo_publicacion = db.Column(db.String(50))
    url_imagen = db.Column(db.String(300))

    def __repr__(self):
        return f"<Libros {self.titulo}>"


class fecha_modificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ultima_modificacion = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    @classmethod
    def actualizar_fecha_modificacion(cls):
        fecha = db.session.get(cls, 1)
        if not fecha:
            fecha = cls()
            db.session.add(fecha)
        FechaUTC = datetime.now(timezone.utc)
        zona_horaria_local = ZoneInfo("Europe/Berlin")
        fecha.ultima_modificacion = FechaUTC.astimezone(zona_horaria_local)

    def __repr__(self):
        return f"<Fecha Modificación: {self.ultima_modificacion}>"


def creacion():
    # Instancia de Flask
    app = Flask(__name__)
    CORS(app)
    app.secret_key = 'v2s7*fp(z8WUr1hCUR({"-Q|yG5muk`?Nd|Ut@cz2E:ZJ[}0/['  #! Clave secreta para las sesiones guardar en variable de entorno
    # Configuración de la BD
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///BDLibros.db"  #! Ruta de la BD guardar en variable de entorno
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


app = creacion()
api = Api(app)


class Listadoibros(Resource):
    @requerir_api_key
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
    @requerir_api_key
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
    @requerir_api_key
    def get(self, id):
        libro = Libros.query.get_or_404(id)
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
            }
        )


class AgregarLibro(Resource):
    @requerir_api_key
    def post(self,borrador): #! Borrador es un parametro que se envia para saber si se debe borrar la tabla de libros automaticos en vez de usar el de editar libros, este  se puede reutilizar. Combinar libros tb
                                #! esto se debe a que en el front ya guardo los libros disponibles, y si los necesito, los muevo ya alli
        data = request.get_json()
        nuevo_libro = Libros(
            titulo=data["titulo"],
            isbn=data["isbn"],
            editorial=data["editorial"],
            descripcion=data["descripcion"],
            anyo_publicacion=data["anyo_publicacion"],
            puntuacion=data["puntuacion"],
            ubicacion_estudio=data["ubicacion_estudio"],
            url_imagen=data["url_imagen"],
        )
        db.session.add(nuevo_libro)
        fecha_modificacion.actualizar_fecha_modificacion()
        if borrador==1: #! 1 si se combinan libros auto o si se escoge solo 1, 0  si es agregar normal
            db.session.query(Libros_automaticos).delete()
        db.session.commit()
        return jsonify({"mensaje": "Libro agregado exitosamente", "id": nuevo_libro.id})
    
    
class borrarLibro(Resource):
    @requerir_api_key
    def delete(self, id):
        libro = Libros.query.get_or_404(id)
        db.session.delete(libro)
        fecha_modificacion.actualizar_fecha_modificacion()
        db.session.commit()
        return jsonify({"mensaje": "Libro eliminado exitosamente"})
    
    
    
class editarLibro(Resource):
    @requerir_api_key
    def put(self, id):
        libro = Libros.query.get_or_404(id)
        data = request.get_json()
        libro.titulo = data.get("titulo", libro.titulo)
        libro.isbn = data.get("isbn", libro.isbn)
        libro.editorial = data.get("editorial", libro.editorial)
        libro.descripcion = data.get("descripcion", libro.descripcion)
        libro.anyo_publicacion = data.get("anyo_publicacion", libro.anyo_publicacion)
        libro.puntuacion = data.get("puntuacion", libro.puntuacion)
        libro.ubicacion_estudio =data.get("ubicacion_estudio", libro.ubicacion_estudio)
        libro.url_imagen = data.get("url_imagen", libro.url_imagen)
        fecha_modificacion.actualizar_fecha_modificacion()
        db.session.commit()
        return jsonify({"mensaje": "Libro editado exitosamente"})    
    
    
    

class Fecha(Resource):
    @requerir_api_key
    def get(self):
        fechas = fecha_modificacion.query.all()
        return jsonify(
            [
                {
                    "id": fecha.id,
                    "dato": fecha.ultima_modificacion,
                }
                for fecha in fechas
            ]
        )

class buscarLibroAutomatico(Resource):
    @requerir_api_key
    def post(self):
        db.session.query(Libros_automaticos).delete()
        db.session.commit()
        data = request.get_json()
        libros=fw.buscar_libro(data["elemento"])
        for libro in libros:
            if libro[2]==True:
                nuevo_libro = Libros_automaticos(
                    auto_id=libro[0],
                    logo=libro[1],
                    titulo=libro[3],
                    isbn=libro[4]+','+libro[5],
                    editorial=libro[6],
                    anyo_publicacion=libro[7],
                    descripcion=libro[8],
                    url_imagen=libro[9]
                    )
                db.session.add(nuevo_libro)
                db.session.commit()
        return ListadoibrosAutomaticos.get(self)

class ListadoibrosAutomaticos(Resource): #! Listado de libros automaticos que se manda al buscador ,para hacer una llamada
    @requerir_api_key
    def get(self):
        libros = Libros_automaticos.query.all()
        return jsonify(
            [
                {
                    "auto_id": libro.auto_id,
                    "logo": libro.logo,
                    "titulo": libro.titulo,
                    "isbn": libro.isbn,
                    "editorial": libro.editorial,
                    "descripcion": libro.descripcion,
                    "anyo_publicacion": libro.anyo_publicacion,
                    "url_imagen": libro.url_imagen,
                }
                for libro in libros
            ]
        )


class borrarTablaLibrosAutomaticos(Resource):
    @requerir_api_key
    def delete(self):
        Libros_automaticos.__table__.drop(db.engine)
        db.session.commit()

class listarLibrosAutomaticos(Resource):
    @requerir_api_key
    def get(self):
        libros = Libros_automaticos.query.all()
        return jsonify(
            [
                {
                    "auto_id": libro.auto_id,
                    "logo": libro.logo,
                    "titulo": libro.titulo,
                    "isbn": libro.isbn,
                    "editorial": libro.editorial,
                    "descripcion": libro.descripcion,
                    "anyo_publicacion": libro.anyo_publicacion,
                    "url_imagen": libro.url_imagen,
                }
                for libro in libros
            ]
        )
        
        
            
#TODO: Crear un endpoint tanto para importar como para exportar los datos de la BD
    
api.add_resource(AgregarLibro, "/agregar_libro/<int:borrador>")
api.add_resource(Listadoibros, "/libros")
api.add_resource(BusquedaLibro, "/busqueda/<string:busqueda>") 
api.add_resource(InfoLibroID, "/infoLibro/<int:id>")
api.add_resource(borrarLibro, "/borrarLibro/<int:id>")
api.add_resource(editarLibro, "/editarLibro/<int:id>")
api.add_resource(buscarLibroAutomatico, "/buscar_libro_automatico")
api.add_resource(borrarTablaLibrosAutomaticos, "/borrar")
api.add_resource(listarLibrosAutomaticos, "/listar_libros_automaticos")
api.add_resource(Fecha, "/fecha")



if __name__ == "__main__":
    app.run(debug=True)
