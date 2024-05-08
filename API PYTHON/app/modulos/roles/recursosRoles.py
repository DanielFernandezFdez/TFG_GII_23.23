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
            return jsonify({"mensaje": "El rol ya existe"}), 400
        nuevo_rol = Roles(nombre_rol=data['nombre_rol'])
        db.session.add(nuevo_rol)
        db.session.commit()
        return jsonify({"mensaje": "Rol creado exitosamente"})

class EditarRol(Resource):
    @jwt_required()
    def put(self, rol_id):
        rol = Roles.query.get_or_404(rol_id)
        data = request.get_json()
        nombre_rol_existente = Roles.query.filter_by(nombre_rol=data['nombre_rol']).first()
        if nombre_rol_existente and nombre_rol_existente.id != rol.id:
            return jsonify({"mensaje": "El rol ya existe"}), 406
        rol.nombre_rol = data['nombre_rol']
        db.session.commit()
        return jsonify({"mensaje": "Rol modificado exitosamente"})

class BorrarRol(Resource):
    @jwt_required()
    def delete(self, rol_id):
        rol = Roles.query.get_or_404(rol_id)
        if rol.id == 1 or rol.id == 2:
            return jsonify({"mensaje": "No se puede eliminar este rol"}), 400
        db.session.delete(rol)
        db.session.commit()
        return jsonify({"mensaje": "Rol eliminado exitosamente"})
