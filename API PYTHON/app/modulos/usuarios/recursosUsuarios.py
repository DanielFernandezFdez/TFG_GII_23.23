from flask_restful import Resource
from flask_jwt_extended import jwt_required, create_access_token
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.modelos.modelos import Usuarios

class RegistroUsuario(Resource):
    @jwt_required()
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
        access_token = create_access_token(identity=usuario.id)
        return jsonify({
            "token": access_token,
            "nombre": usuario.usuario,
            "id": usuario.id})
    
    
class ModificarUsuario(Resource):
    @jwt_required()
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
            if repetido and repetido.id != usuario.id:
                respuesta = jsonify({"mensaje": "Ya existe un correo"})
                respuesta.status_code = 400
                return respuesta
            usuario.usuario = data['usuario']
        if 'correo' in data:
            usuario.correo=data['correo']
        
        if 'rol_id' in data and data['rol_id'] != usuario.rol:
            if usuario.id == 1  and data['rol_id'] != 1:
                
                respuesta = jsonify({"mensaje": "No se puede modificar el rol del usuario administrador"})
                respuesta.status_code = 400
                return respuesta

            usuario.rol_id = data['rol_id']
        db.session.commit()
        return jsonify({"mensaje": "Usuario modificado exitosamente"})

class EliminarUsuario(Resource):
    @jwt_required()
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
    @jwt_required()
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
    @jwt_required()
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