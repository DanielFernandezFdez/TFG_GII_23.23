from functools import wraps
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask_cors import CORS
import funciones_webscraping as fw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required,JWTManager, get_jwt_identity
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


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(100), unique=True, nullable=False)
    usuarios = db.relationship('Usuarios', backref='rol', lazy='joined')

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasenya_encriptada = db.Column(db.String(128), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    
class Botones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_boton = db.Column(db.String(100), unique=True, nullable=False)
    alias = db.Column(db.String(255), nullable=True)
    descripcion = db.Column(db.String(255), nullable=True)
    roles_autorizados=db.Column(db.String(255), nullable=True)
       

    


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
        usuario = Usuarios.query.filter_by(correo=data['correo']).first()
        if usuario:
            respuesta = jsonify({"mensaje": "El correo ya está registrado"})
            respuesta.status_code = 400
            return respuesta
        nuevo_usuario = Usuarios(
            usuario=data['usuario'],
            correo=data['correo'],
            contrasenya_encriptada=generate_password_hash(data['contrasenya']),
            rol_id=data['rol'] if 'rol' in data else 1
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario registrado exitosamente"})

class Login(Resource):
    def post(self):
        data = request.get_json()
        usuario = Usuarios.query.filter_by(correo=data['correo']).first()
        if not usuario or not check_password_hash(usuario.contrasenya_encriptada, data['contrasenya']):
            respuesta = jsonify({"mensaje": "Usuario o contraseña incorrectos"})
            respuesta.status_code = 401
            return respuesta
        access_token = create_access_token(identity=usuario.id) #Con esto puedo obtener el id de  ususario ya que se contiene en el jwt
        return jsonify({
            "token": access_token,
            "nombre": usuario.usuario,
            "id": usuario.id})
    
    
class ModificarUsuario(Resource):
    def put(self, user_id):
        usuario = Usuarios.query.get_or_404(user_id)
        data = request.get_json()
        if 'contrasenya_nueva' in data:
            if not check_password_hash(usuario.contrasenya_encriptada, data['contrasenya_actual']):
                respuesta = jsonify({"mensaje": "Contraseña actual incorrecta"})
                respuesta.status_code = 400
                return respuesta
            usuario.contrasenya_encriptada = generate_password_hash(data['contrasenya_nueva'])
        if 'usuario' in data:
            usuario.usuario = data['usuario']
        if 'rol' in data:
            if usuario.id == 1:
                respuesta = jsonify({"mensaje": "No se puede modificar el rol del usuario administrador"})
                respuesta.status_code = 400
                return respuesta

            usuario.rol_id = data['rol']
        db.session.commit()
        return jsonify({"mensaje": "Usuario modificado exitosamente"})

class EliminarUsuario(Resource):
    def delete(self, user_id):
        usuario = Usuarios.query.get_or_404(user_id)
        if usuario.id == 1:
            respuesta = jsonify({"mensaje": "No se puede eliminar el usuario administrador"})
            respuesta.status_code = 400
            return respuesta
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
                    "correo": usuario.correo,
                    "rol": usuario.rol.nombre_rol if usuario.rol else None,
                }
                for usuario in usuarios
            ]
        )

class InfoUsuario(Resource):
    def get(self, user_id):
        usuario = Usuarios.query.get_or_404(user_id)
        return jsonify(
            {
                "id": usuario.id,
                "usuario": usuario.usuario,
                "correo": usuario.correo,
                "rol": usuario.rol.nombre_rol if usuario.rol else None,
            }
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
        rol = Roles.query.filter_by(nombre_rol=data['nombre_rol']).first()
        if rol:
            respuesta = jsonify({"mensaje": "El rol ya existe"})
            respuesta.status_code = 400
            return respuesta
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
        nombre_rol_existente = Roles.query.filter_by(nombre_rol=data['nombre_rol']).first()
        if nombre_rol_existente:
            json = jsonify({"mensaje": "El rol ya existe"})
            json.status_code = 400
            return json
        if 'nombre_rol' in data:
            rol.nombre_rol = data['nombre_rol']
        db.session.commit()
        return jsonify({"mensaje": "Rol modificado exitosamente"})


class BorrarRol(Resource):
    def delete(self, rol):
        rol = Roles.query.get_or_404(rol)
        if rol.id == 1:
            respuesta = jsonify({"mensaje": "No se puede eliminar el rol de administrador"})
            respuesta.status_code = 400
            return respuesta
        if rol.id == 2:
            respuesta = jsonify({"mensaje": "No se puede eliminar el rol de usuario"})
            respuesta.status_code = 400
            return respuesta
        #Actualizacion de usuarios a usuario
        usuarios = Usuarios.query.filter_by(rol_id=rol.id).all()
        for usuario in usuarios:
            usuario.rol_id = 2
            
        db.session.commit()
        
        #Actualizacion de botones
        botones = Botones.query.all()
        for boton in botones:
            roles_actuales = json.loads(boton.roles_autorizados)
            if rol.nombre_rol in roles_actuales:
                roles_actuales.remove(rol.nombre_rol)
                boton.roles_autorizados = json.dumps(roles_actuales)
        
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
                    "alias": boton.alias,
                    "descripcion": boton.descripcion,
                    "roles": json.loads(boton.roles_autorizados if boton.roles_autorizados else []) 
                }
                for boton in botones
            ]
        )

class consultarBoton(Resource):
    def post(self, id_usuario):
        data = request.get_json()
        usuario = Usuarios.query.get_or_404(id_usuario)
        rol_usuario = usuario.rol.nombre_rol

        botones_respuesta = []

        for nombre_boton in data['nombre_botones']:
            boton = Botones.query.filter_by(nombre_boton=nombre_boton).first()
            if boton:
                alias = boton.alias
                descripcion = boton.descripcion
                roles_autorizados = json.loads(boton.roles_autorizados if boton.roles_autorizados else '[]')
                autorizado = 1 if rol_usuario in roles_autorizados else 0
            else:
                autorizado = 0  
            botones_respuesta.append(
                {
                "nombre": nombre_boton,
                "alias":alias,
                "descripcion":descripcion, 
                "autorizado": autorizado
                })

        return jsonify(botones_respuesta)

class CrearBoton(Resource): #!Solo durante pruebas
    def post(self):
        data = request.get_json()
        boton_existente=Botones.query.filter_by(nombre_boton=data['nombre_boton']).first()
        if boton_existente:
            respuesta = jsonify({"mensaje": "El boton ya existe"})
            respuesta.status_code = 400
            return respuesta
        nuevo_boton = Botones(
            nombre_boton=data['nombre_boton'],
            alias=data['alias'] if 'alias' in data else "Sin nombre",
            descripcion=data['descripcion'] if 'descripcion' in data else "Sin descripcion",
            roles_autorizados=json.dumps(data['roles_autorizados'] if 'roles_autorizados' in data else []) 
        )
        db.session.add(nuevo_boton)
        db.session.commit()
        return jsonify({"mensaje": "Boton creado exitosamente"})



class EditarBoton(Resource):
    def put(self):
        data = request.get_json()
        for boton_data in data['botones']:
            boton = Botones.query.filter_by(nombre_boton=boton_data['nombre_boton']).first()
            
            roles_actuales = json.loads(boton.roles_autorizados)

            if 'roles_autorizados' in boton_data:
                rol = boton_data['roles_autorizados']
                if rol not in roles_actuales:
                    roles_actuales.append(rol)
            
            else:
                rol_solicitado = boton_data['rol_solicitado']
                if rol_solicitado in roles_actuales:
                    roles_actuales.remove(rol_solicitado)

            boton.roles_autorizados = json.dumps(roles_actuales)
            
            db.session.commit()

        return jsonify({"mensaje": "Botones actualizados exitosamente"})
    
    
class BorrarBoton(Resource):
    def delete(self, boton_id):
        boton = Botones.query.get_or_404(boton_id)
        db.session.delete(boton)
        db.session.commit()
        return jsonify({"mensaje": "Boton eliminado exitosamente"})   
    
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
api.add_resource(InfoUsuario, '/info_usuario/<int:user_id>')
api.add_resource(ObtenerRoles, '/roles')
api.add_resource(CrearRol, '/crear_rol')
api.add_resource(EditarRol, '/editar_rol/<int:rol>')
api.add_resource(BorrarRol, '/borrar_rol/<int:rol>')



api.add_resource(buscarBotones, '/botones')
api.add_resource(consultarBoton, '/consultar_boton/<int:id_usuario>')
api.add_resource(CrearBoton, '/crear_boton')
api.add_resource(EditarBoton, '/editar_boton')
api.add_resource(BorrarBoton, '/borrar_boton/<int:boton_id>')




if __name__ == "__main__":
    app.run(debug=True)



# "botones": [
#         {
#             "nombre_boton": "nombre_boton1",
#             "rol_solicitado": Admin    Quiero trabajar con el rol de admin
#             "roles_autorizados": "Admin" Añadir el rol de admin
#               "alias": "alias",
#               "descripcion": "descripcion"
#         },
#         {
#             "nombre_boton": "nombre_boton2",
#             "rol_solicitado": Admin   Quiero trabajar con el rol de admin
#                                       No quiero trabajar con el rol de usuario
#         },
#         {
#             "nombre_boton": "nombre_boton3",
#             "rol_solicitado": Admin
#             "roles_autorizados": Admin
#         }
#     ]