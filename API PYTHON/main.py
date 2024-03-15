from functools import wraps
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask_cors import CORS
import funciones_webscraping as fw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required,JWTManager
import json


db = SQLAlchemy()


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


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    contrasenya_encriptada = db.Column(db.String(128), nullable=False)
    rol = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False) #! Relacion con la tabla roles MIRAR



class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(100), unique=True, nullable=False)
    
    
class Botones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_boton = db.Column(db.String(100), unique=True, nullable=False)
    roles_autorizados=db.Column(db.String(255), nullable=True)
    def obtener_roles_autorizados(self):
        if self.roles_autorizados:
            return json.loads(self.roles_autorizados) 
        else:
            return []

    def asignar_roles_autorizados(self, roles):
        self.roles_autorizados = json.dumps(roles)
    


def creacion():
    # Instancia de Flask
    app = Flask(__name__)
    CORS(app)
    app.secret_key = 'v2s7*fp(z8WUr1hCUR({"-Q|yG5muk`?Nd|Ut@cz2E:ZJ[}0/['  #! Clave secreta para las sesiones guardar en variable de entorno
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "sqlite:///BDLibros.db"  #! Ruta de la BD guardar en variable de entorno
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['JWT_SECRET_KEY'] = '9.gbPCDn!Ufm&o-a)k-nbEcSImx+.Rkef#{s=AjFsIUeZWr!'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Token expira después de 1 hora
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


app = creacion()
api = Api(app)
jwt=JWTManager(app)



class Listadoibros(Resource):
    @jwt_required()
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

    def post(
        self, borrador
    ):  #! Borrador es un parametro que se envia para saber si se debe borrar la tabla de libros automaticos en vez de usar el de editar libros, este  se puede reutilizar. Combinar libros tb
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
        if (
            borrador == 1
        ):  #! 1 si se combinan libros auto o si se escoge solo 1, 0  si es agregar normal
            db.session.query(Libros_automaticos).delete()
        db.session.commit()
        return jsonify({"mensaje": "Libro agregado exitosamente", "id": nuevo_libro.id})


class borrarLibro(Resource):

    def delete(self, id):
        libro = Libros.query.get_or_404(id)
        db.session.delete(libro)
        fecha_modificacion.actualizar_fecha_modificacion()
        db.session.commit()
        return jsonify({"mensaje": "Libro eliminado exitosamente"})


class editarLibro(Resource):

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
                    titulo=libro[3],
                    isbn=libro[4] + "," + libro[5],
                    editorial=libro[6],
                    anyo_publicacion=libro[7],
                    descripcion=libro[8],
                    url_imagen=libro[9],
                )
                db.session.add(nuevo_libro)
                db.session.commit()
        return ListadoibrosAutomaticos.get(self)


class ListadoibrosAutomaticos(Resource):  #! Listado de libros automaticos que se manda al buscador ,para hacer una llamada

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

    def delete(self):
        Libros_automaticos.__table__.drop(db.engine)
        db.session.commit()


class listarLibrosAutomaticos(Resource):

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





class RegistroUsuario(Resource):
    def post(self):
        data = request.get_json()
        nuevo_usuario = Usuarios(
            usuario=data['usuario'],
            contrasenya_encriptada=generate_password_hash(data['contrasenya']),
            rol=data['rol'] if 'rol' in data else 1
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario registrado exitosamente"})

class Login(Resource):
    def post(self):
        data = request.get_json()
        usuario = Usuarios.query.filter_by(usuario=data['usuario']).first()
        if not usuario or not check_password_hash(usuario.contrasenya_encriptada, data['contrasenya']):
            return jsonify({"mensaje": "Usuario o contraseña incorrectos"}), 401
        access_token = create_access_token(identity=usuario.id)
        return jsonify(access_token=access_token)
    
    
class ModificarUsuario(Resource):
    def put(self, user_id):
        usuario = Usuarios.query.get_or_404(user_id)
        data = request.get_json()
        if 'contrasenya' in data:
            usuario.contrasenya_encriptada = generate_password_hash(data['contrasenya'])
        if 'usuario' in data:
            usuario.usuario = data['usuario']
        if 'rol' in data:
            usuario.rol = data['rol']
        db.session.commit()
        return jsonify({"mensaje": "Usuario modificado exitosamente"})

class EliminarUsuario(Resource):
    def delete(self, user_id):
        usuario = Usuarios.query.get_or_404(user_id)
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario eliminado exitosamente"})   
    

class ListarUsuarios(Resource):
    def get(self):
        usuarios = Usuarios.query.all()
        return jsonify(
            [
                {
                    "id": usuario.id,
                    "usuario": usuario.usuario,
                    "rol": usuario.rol.nombre if usuario.rol else None
                }
                for usuario in usuarios
            ]
        )


class ObtenerRoles(Resource):
    def get(self):
        roles = Roles.query.all()
        return jsonify(
            [
                {
                    "id": rol.id,
                    "nombre_rol": rol.nombre_rol,
                }
                for rol in roles
            ]
        )
        
class CrearRol(Resource):
    def post(self):
        data = request.get_json()
        nuevo_rol = Roles(
            nombre_rol=data['nombre_rol'],
        )
        db.session.add(nuevo_rol)
        db.session.commit()
        return jsonify({"mensaje": "Rol creado exitosamente"})


class EditarRol(Resource):
    def put(self, rol):
        rol = Roles.query.get_or_404(rol)
        data = request.get_json()
        if 'nombre_rol' in data:
            rol.nombre_rol = data['nombre_rol']
        db.session.commit()
        return jsonify({"mensaje": "Rol modificado exitosamente"})


class BorrarRol(Resource):
    def delete(self, rol):
        rol = Roles.query.get_or_404(rol)
        db.session.delete(rol)
        db.session.commit()
        return jsonify({"mensaje": "Rol eliminado exitosamente"}) 
    
    
class buscarBotones(Resource): #!Solo durante pruebas
    def get(self):
        botones = Botones.query.all()
        return jsonify(
            [
                {
                    "id": boton.id,
                    "nombre": boton.nombre_boton,
                    "roles": boton.roles_autorizados
                }
                for boton in botones
            ]
        )

class CrearBoton(Resource): #!Solo durante pruebas
    def post(self):
        data = request.get_json()
        nuevo_boton = Botones(
            nombre_boton=data['nombre_boton'],
            roles_autorizados=data['roles_autorizados']
        )
        db.session.add(nuevo_boton)
        db.session.commit()
        return jsonify({"mensaje": "Boton creado exitosamente"})

class EditarBoton(Resource):
    def put(self, boton_id):
        boton = Botones.query.get_or_404(boton_id)
        data = request.get_json()
        for key in data:
            if key == 'nombre_boton':
                boton.nombre_boton = data['nombre_boton']
            if key == 'roles_autorizados':
                roles=boton.obtener_roles_autorizados()
                if (data['roles_autorizados'] == ""):
                    if(roles.contains(data['roles_autorizados'])):
                        roles.remove(data['roles_autorizados'])
                        boton.asignar_roles_autorizados(roles)
                else:
                    roles.append(data['roles_autorizados'])
                    boton.asignar_roles_autorizados(roles)
        db.session.commit()
        return jsonify({"mensaje": "Preferencias modificadas exitosamente"})
    
# TODO: Crear un endpoint tanto para importar como para exportar los datos de la BD

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


api.add_resource(RegistroUsuario, '/registro')
api.add_resource(Login, '/login')
api.add_resource(ModificarUsuario, '/modificar_usuario/<int:user_id>')
api.add_resource(EliminarUsuario, '/eliminar_usuario/<int:user_id>') 
api.add_resource(ListarUsuarios, '/usuarios')
api.add_resource(ObtenerRoles, '/roles')
api.add_resource(CrearRol, '/crear_rol')
api.add_resource(EditarRol, '/editar_rol/<int:rol>')
api.add_resource(BorrarRol, '/borrar_rol/<int:rol>')



api.add_resource(buscarBotones, '/botones')
api.add_resource(CrearBoton, '/crear_boton')
api.add_resource(EditarBoton, '/editar_boton/<int:boton_id>')




if __name__ == "__main__":
    app.run(debug=True)
