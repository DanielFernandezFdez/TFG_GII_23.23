from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from flask import jsonify
from app.modelos.modelos import Roles, db

class ObtenerRoles(Resource):
    def get(self):
        roles = Roles.query.all()
        return jsonify([
            {
                "id": rol.id,
                "nombre_rol": rol.nombre_rol
            } for rol in roles
        ])

class ConsultarRol(Resource):
    def post(self, id):
        rol = Roles.query.get_or_404(id)
        return jsonify({
            "id": rol.id,
            "nombre_rol": rol.nombre_rol
        })

class CrearRol(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        rol = Roles.query.filter_by(nombre_rol=data['nombre_rol']).first()
        if rol:
            return {"mensaje": "El rol ya existe"}, 400
        nuevo_rol = Roles(nombre_rol=data['nombre_rol'])
        db.session.add(nuevo_rol)
        db.session.commit()
        return {"id": nuevo_rol.id, "mensaje": "Rol creado exitosamente"},200

class EditarRol(Resource):
    @jwt_required()
    def put(self, id):
        rol = Roles.query.get_or_404(id)
        data = request.get_json()
        nombre_rol_existente = Roles.query.filter_by(nombre_rol=data['nombre_rol']).first()
        if nombre_rol_existente and nombre_rol_existente.id != rol.id:
            return {"mensaje": "El rol ya existe"}, 406
        rol.nombre_rol = data['nombre_rol']
        db.session.commit()
        return {"mensaje": "Rol modificado exitosamente"},200

class BorrarRol(Resource):
    @jwt_required()
    def delete(self, id):
        rol = Roles.query.get_or_404(id)
        if rol.id == 1 or rol.id == 2:
            return {"mensaje": "No se puede eliminar este rol"}, 400
        db.session.delete(rol)
        db.session.commit()
        return {"mensaje": "Rol eliminado exitosamente"},200
