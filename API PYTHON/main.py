from flask import Flask, request, jsonify, send_file,Response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask_cors import CORS
import funciones_webscraping as fw
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required,JWTManager, get_jwt_identity
import json
import importar_exportar as ie
import csv
from io import StringIO

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
    disponible=db.Column(db.Boolean)
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

class GestionEstimacion(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    actividades_produccion= db.Column(db.String(255), nullable=True)
    actividades_poder = db.Column(db.String(255), nullable=True)
    actividades_mantenimiento = db.Column(db.String(255), nullable=True)
    actividades_hombre= db.Column(db.String(255), nullable=True)
    actividades_mujer= db.Column(db.String(255), nullable=True)


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
    roles_autorizados=db.Column(db.String(255), nullable=True)
    
    
class Estimacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    masculino_generico = db.Column(db.Boolean, nullable=False)
    numero_ninyas = db.Column(db.Integer, nullable=True)
    numero_ninyos = db.Column(db.Integer, nullable=True)
    numero_hombres = db.Column(db.Integer, nullable=False)
    numero_mujeres = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.Integer, nullable=False)
    res_actividades_hombre = db.Column(db.String(255), nullable=True)
    res_actividades_mujer = db.Column(db.String(255), nullable=True)
    titulo = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    institucion = db.Column(db.String(100), nullable=False)
    resultado = db.Column(db.Integer, nullable=False)
       

    


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



# componentes para este json:

# masculino generico ---> bool

# numero_ninyas -----> int opcional
# numero_ninyos -----> int opcional

# numero_hombres ----> int
# numero_mujeres ----> int 

# actividades_hombre ----> int
# actividades_mujer-----> int

# comprobacion suma de todas listas minimo 1, evitamos 0/0



class GenerarListados(Resource):
    def post(self):
        data=request.get_json()
        db.session.query(GestionEstimacion).delete()
        db.session.commit()
        listado_nuevo = GestionEstimacion(
            actividades_produccion= json.dumps(data["actividades_produccion"] if "actividades_produccion" in data else []),
            actividades_poder = json.dumps(data["actividades_poder"] if "actividades_poder" in data else []),
            actividades_mantenimiento = json.dumps(data["actividades_mantenimiento"] if "actividades_mantenimiento" in data else []),
            actividades_hombre= json.dumps(data["actividades_hombre"] if "actividades_hombre" in data else []),
            actividades_mujer= json.dumps(data["actividades_mujer"] if "actividades_mujer" in data else []),
            
        )
        db.session.add(listado_nuevo)
        db.session.commit()
        return jsonify(
            {
                "Ok":"OK"
            }
        )

class ObtenerListados(Resource):
    def get(self):
        listados=GestionEstimacion.query.get_or_404(1)
        return jsonify(
            {
                "actividades_produccion" : json.loads(listados.actividades_produccion),
                "actividades_poder" : json.loads(listados.actividades_poder),
                "actividades_mantenimiento" : json.loads(listados.actividades_mantenimiento),
                "actividades_hombre" : json.loads(listados.actividades_hombre),
                "actividades_mujer" : json.loads(listados.actividades_mujer)
            }
        )

class BorrarListados(Resource):
    def delete(self):
        db.session.delete(GestionEstimacion.query.get_or_404(1))
        db.session.commit()
        return jsonify(
            {
                "resultado":"OK"
            }
        )

class CalcularEstimacion(Resource):
    def post(self):
        resultado=0
        data=request.get_json();


        ponderacion_adultos=0.15
        ponderacion_ninyos = 0.15
        ponderacion_actividad=0.3

        #?Apartado de masculino generico
        masculino_generico=data["masculino_generico"]
        if masculino_generico==False:
            resultado=20
        
        #? Apartado de calculos de niños
        if data["numero_ninyos"]!=0 or data["numero_ninyas"]!=0 in data :
            numero_ninyos = data["numero_ninyos"]
            numero_ninyas = data["numero_ninyas"]
            suma=numero_ninyos+numero_ninyas
            if numero_ninyos> numero_ninyas:
                proporcion= numero_ninyas/suma
                sobre100_ninyos=proporcion*2 #50 seria lo ideal por lo tanto al hacer regla de 3 con multiplicar por 2 se saca
                resultado+=ponderacion_ninyos*sobre100_ninyos*100
            else:
                proporcion= numero_ninyos/suma
                sobre100_ninyos=proporcion*2 #50 seria lo ideal por lo tanto al hacer regla de 3 con multiplicar por 2 se saca
                resultado+=ponderacion_ninyos*sobre100_ninyos*100

        else:
            ponderacion_adultos=0.3


        #? Apartado calculos de adultos
        numero_hombres=data["numero_hombres"]
        numero_mujeres=data["numero_mujeres"]
        suma=numero_hombres+numero_mujeres
        if numero_hombres> numero_mujeres:
            proporcion= numero_mujeres/suma
            sobre100_adultos=proporcion*2 #50 seria lo ideal por lo tanto al hacer regla de 3 con multiplicar por 2 se saca
            resultado+=ponderacion_adultos*sobre100_adultos*100
        else:
            proporcion= numero_hombres/suma
            sobre100_adultos=proporcion*2 #50 seria lo ideal por lo tanto al hacer regla de 3 con multiplicar por 2 se saca
            resultado+=ponderacion_adultos*sobre100_adultos*100


        #?Apartado de listados de actividades
        res_actividades_hombre = data.get("res_actividades_hombre",[])
        res_actividades_mujer = data.get("res_actividades_mujer",[])

        actividades = GestionEstimacion.query.get_or_404(1)
        mejor_hombres = json.loads(actividades.actividades_hombre)
        mejor_mujeres = json.loads(actividades.actividades_mujer)

        contador_comun = 0
        contador_total = 0

        if len(res_actividades_hombre) != 0:
            for actividad_hombre in res_actividades_hombre:

                if actividad_hombre in mejor_hombres:
                    contador_comun += 1
                contador_total += 1

        if len(res_actividades_mujer) != 0:
            for actividad_mujer in res_actividades_mujer:

                if actividad_mujer in mejor_mujeres:
                    contador_comun += 1
                contador_total += 1

        proporcion = contador_comun / contador_total if contador_total != 0 else 0
        resultado += proporcion * ponderacion_actividad * 100


        #? Calculo de ubicacion, se pasa ya el valor correspondiente 0 a 100 

        resultado+=data["ubicacion"]*0.2


        return jsonify(
            {
                "resultado": round(resultado),
            }
        )


class guardarEstimacion(Resource):
    def post(self):
        data=request.get_json()
        estimacion = Estimacion(
            masculino_generico=data["masculino_generico"] if "masculino_generico" in data else False,
            numero_ninyas=data["numero_ninyas"] if "numero_ninyas" in data else 0,
            numero_ninyos=data["numero_ninyos"] if "numero_ninyos" in data else 0,
            numero_hombres=data["numero_hombres"] if "numero_hombres" in data else 0,
            numero_mujeres=data["numero_mujeres"] if "numero_mujeres" in data else 0,
            ubicacion=data["ubicacion"] if "ubicacion" in data else 0,
            res_actividades_hombre=json.dumps(data["res_actividades_hombre"] if "res_actividades_hombre" in data else []),
            res_actividades_mujer=json.dumps(data["res_actividades_mujer"] if "res_actividades_mujer" in data else []),
            titulo=data["titulo"] if "titulo" in data else "No disponible",
            isbn=data["isbn"] if "isbn" in data else "No disponible",
            nombre=data["nombre"] if "nombre" in data else "No disponible",
            apellido=data["apellido"] if "apellido" in data else "No disponible",
            correo=data["correo"] if "correo" in data else "No disponible",
            institucion=data["institucion"] if "institucion" in data else "No disponible",
            resultado=data["resultado"] if "resultado" in data else 0
        )
        db.session.add(estimacion)
        db.session.commit()
        return jsonify(
            {
                "Ok":"OK"
            }
        )

class listarEstimaciones(Resource):
    def get(self):
        estimaciones = Estimacion.query.all()
        return jsonify(
            [
                {
                    "id": estimacion.id,
                    "masculino_generico": estimacion.masculino_generico,
                    "numero_ninyas": estimacion.numero_ninyas,
                    "numero_ninyos": estimacion.numero_ninyos,
                    "numero_hombres": estimacion.numero_hombres,
                    "numero_mujeres": estimacion.numero_mujeres,
                    "ubicacion": estimacion.ubicacion,
                    "res_actividades_hombre": json.loads(estimacion.res_actividades_hombre),
                    "res_actividades_mujer": json.loads(estimacion.res_actividades_mujer),
                    "titulo": estimacion.titulo,
                    "isbn": estimacion.isbn,
                    "nombre": estimacion.nombre,
                    "apellido": estimacion.apellido,
                    "correo": estimacion.correo,
                    "institucion": estimacion.institucion,
                    "resultado": estimacion.resultado
                }
                for estimacion in estimaciones
            ]
        )
        
class BorrarEstimacion(Resource):
    def delete(self, id):
        estimacion = Estimacion.query.get_or_404(id)
        db.session.delete(estimacion)
        db.session.commit()
        return jsonify({"mensaje": "Estimación eliminada exitosamente"})



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
            url_imagen=data["url_imagen"] ,
        )
        db.session.add(nuevo_libro)
        fecha_modificacion.actualizar_fecha_modificacion()
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

    def delete(self):
        Estimacion.__table__.drop(db.engine)
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
            contrasenya_encriptada=generate_password_hash("12345678"),
            rol_id=data['rol'] if 'rol' in data else 2 #!Aqui hay que crear el rol usuario base, para que por defecto tenga permisos limitados
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
            repetido=Usuarios.query.filter_by(correo=data['correo']).first()
            if repetido.id != usuario.id:
                respuesta = jsonify({"mensaje": "Ya existe un correo"})
                respuesta.status_code = 400
                return respuesta
            usuario.usuario = data['usuario']
        if 'correo' in data:
            usuario.correo=data['correo']
        
        if 'rol_id' in data and data['rol_id'] != usuario.rol:
            if usuario.id == 1:
                respuesta = jsonify({"mensaje": "No se puede modificar el rol del usuario administrador"})
                respuesta.status_code = 400
                return respuesta

            usuario.rol_id = data['rol_id']
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
                    "rol_id": usuario.rol_id if usuario.rol else None
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
                    "nombre_rol": rol.nombre_rol
                }
                for rol in roles
            ]
        )
        
class ConsultarRol(Resource):
    def post(self, id):
        rol = Roles.query.get_or_404(id)
        return jsonify(
            {
                "id": rol.id,
                "nombre_rol": rol.nombre_rol
            }
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
        
        # Verifica si el rol existe y no es el mismo que se está editando
        if nombre_rol_existente and nombre_rol_existente.id != rol.id:
            response = jsonify({"mensaje": "El rol ya existe"})
            response.status_code = 406
            return response
        
        # Actualizar el nombre del rol si se proporciona
        if 'nombre_rol' in data:
            rol.nombre_rol = data['nombre_rol']
        
        db.session.commit()
        
        # Actualización de botones
        botones = Botones.query.all()
        for boton in botones:
            roles_actuales = json.loads(boton.roles_autorizados)
            if rol.nombre_rol in roles_actuales:
                roles_actuales.remove(rol.nombre_rol)
                roles_actuales.append(data['nombre_rol'])
                boton.roles_autorizados = json.dumps(roles_actuales)
        
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
            roles_actuales=[]
            roles_actuales = json.loads(boton.roles_autorizados)
            if rol.nombre_rol in roles_actuales:
                roles_actuales.remove(rol.nombre_rol)
                boton.roles_autorizados = json.dumps(roles_actuales)
        
        db.session.delete(rol)
        db.session.commit()
        return jsonify({"mensaje": "Rol eliminado exitosamente"}) 
    
    
class buscarBotones(Resource):
    def get(self):
        botones = Botones.query.all()
        return jsonify(
            [
                {
                    "id": boton.id,
                    "nombre": boton.nombre_boton,
                    "alias": boton.alias,
                    "roles_asociados": json.loads(boton.roles_autorizados if boton.roles_autorizados else []) 
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

        for nombre_boton in data['nombre_botones']: #! En teoria solo viene 1
            boton = Botones.query.filter_by(nombre_boton=nombre_boton).first()
            if boton:
                alias = boton.alias if boton.alias else "Sin nombre"
                roles_autorizados = json.loads(boton.roles_autorizados if boton.roles_autorizados else '[]')
                if roles_autorizados==[]:
                    autorizado = 1
                autorizado = 1 if rol_usuario in roles_autorizados else 0
            else:
                autorizado = 0  
            botones_respuesta.append(
                {
                "nombre": nombre_boton,
                "alias":alias if alias else "Sin alias",
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
            print(boton.nombre_boton)
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
    
#!Solo durante las pruebas. No es necesario cuando ya esten creados todos los botones
class BorrarBoton(Resource):
    def delete(self, boton_id):
        boton = Botones.query.get_or_404(boton_id)
        db.session.delete(boton)
        db.session.commit()
        return jsonify({"mensaje": "Boton eliminado exitosamente"})   
    


#Funcion de exportar a CSV
class ExportarCSV(Resource):
    def get(self):
        si = StringIO()
        cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Escribe los encabezados en el archivo CSV
        cw.writerow(['ID', 'Título', 'ISBN', 'Editorial', 'Descripción', 'Año de publicación',"Puntuación", 'Ubicación del estudio', 'URL de la imagen'])

        # Obtiene todos los libros de la base de datos
        libros = Libros.query.all()

        # Escribe los datos de cada libro en el archivo CSV
        for libro in libros:
            cw.writerow([libro.id, libro.titulo, libro.isbn, libro.editorial, libro.descripcion, libro.anyo_publicacion,libro.puntuacion, libro.ubicacion_estudio, libro.url_imagen])

        output = si.getvalue()

        # Crea una respuesta HTTP con el archivo CSV
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=libros.csv"}
        )

class ImportarCSV(Resource):
    def post(self):
        if 'archivo' not in request.files:
            return {"mensaje": "No se envió el archivo."}, 400

        archivo = request.files['archivo']
        stream = StringIO(archivo.stream.read().decode("UTF-8"), newline=None)
        csv_input = csv.reader(stream,delimiter=';')

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
                anyo_publicacion=row[5],
                puntuacion=row[6],
                ubicacion_estudio=row[7],
                url_imagen=row[8]
            )


            db.session.add(nuevo_libro)
            
        fecha_modificacion.actualizar_fecha_modificacion()

        db.session.commit()
        # Redireccionar o enviar una respuesta adecuada
        return jsonify({"mensaje": "Datos importados exitosamente"})

api.add_resource(GenerarListados, "/generarListados")
api.add_resource(ObtenerListados, "/obtenerListados")
api.add_resource(CalcularEstimacion, "/estimacion")
api.add_resource(BorrarListados,"/borrarListados")
api.add_resource(guardarEstimacion, "/guardarEstimacion")
api.add_resource(listarEstimaciones, "/listarEstimaciones")
api.add_resource(BorrarEstimacion, "/borrarEstimacion/<int:id>")


api.add_resource(AgregarLibro, "/agregar_libro")
api.add_resource(ListadoLibros, "/libros")
api.add_resource(BusquedaLibro, "/busqueda/<string:busqueda>")
api.add_resource(InfoLibroID, "/infoLibro/<int:id>")
api.add_resource(borrarLibro, "/borrarLibro/<int:id>")
api.add_resource(editarLibro, "/editarLibro/<int:id>")
api.add_resource(buscarLibroAutomatico, "/buscar_libro_automatico")
api.add_resource(borrarTabla, "/borrar")
api.add_resource(listarLibrosAutomaticos, "/listar_libros_automaticos")
api.add_resource(Fecha, "/fecha")




api.add_resource(RegistroUsuario, '/registro')
api.add_resource(Login, '/login')
api.add_resource(ModificarUsuario, '/modificar_usuario/<int:user_id>')
api.add_resource(EliminarUsuario, '/eliminar_usuario/<int:user_id>') 
api.add_resource(ListarUsuarios, '/usuarios')
api.add_resource(InfoUsuario, '/info_usuario/<int:user_id>')
api.add_resource(ObtenerRoles, '/roles')
api.add_resource(ConsultarRol, '/consultar_rol/<int:id>')
api.add_resource(CrearRol, '/crear_rol')
api.add_resource(EditarRol, '/editar_rol/<int:rol>')
api.add_resource(BorrarRol, '/borrar_rol/<int:rol>')



api.add_resource(buscarBotones, '/botones')
api.add_resource(consultarBoton, '/consultar_boton/<int:id_usuario>')
api.add_resource(CrearBoton, '/crear_boton')
api.add_resource(EditarBoton, '/editar_boton')
api.add_resource(BorrarBoton, '/borrar_boton/<int:boton_id>')


api.add_resource(ExportarCSV, '/exportar_csv')
api.add_resource(ImportarCSV, '/importar_csv')

if __name__ == "__main__":
    app.run(debug=True)




    




# "botones": [
#         {
#             "nombre_boton": "nombre_boton1",
#             "roles_autorizados": "Admin"
#         },
#         {
#             "nombre_boton": "nombre_boton2",
#             "rol_solicitado": Admin 
#         },
#     ]
    




#  {
#      "actividades_produccion": ["Cazar","Pescar","Producir herramientas", "Producir bienes inmuebles", "Transformar materias primas", "Recolectar", "Producir arte","Sembrar","Cosechar","Hacer fuego",
#      "Usar herramientas"],
#      "actividades_poder":["Controlar","Mandar","Luchar","Dominar","Deliberar"],
#      "actividades_mantenimiento":["Limpiar","Cuidar","Cocinar","Curar","Remendar","Consolar","Criar","Aconsejar","Mantener el fuego","Coser","Curtir","Enseñar","Ayudar"],
#      "actividades_hombre":["Recolectar","Sembrar","Cosechar","Limpiar","Cuidar","Cocinar","Curar","Remendar","Consolar","Criar","Aconsejar","Mantener el fuego","Coser","Curtir","Enseñar","Ayudar"],
#      "actividades_mujer":["Cazar","Pescar","Producir herramientas", "Producir bienes inmuebles", "Transformar materias primas","Producir arte","Hacer fuego",
#      "Usar herramientas","Controlar","Mandar","Luchar","Dominar","Deliberar"]

#  }