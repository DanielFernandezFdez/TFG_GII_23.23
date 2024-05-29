from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import jsonify, request

from app.modelos import db, Colaboradores


class AgregarColaborador(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        colaborador = Colaboradores(
            nombre=data["nombre"],
            apellido=data["apellido"],
            institucionn=data["institucion"],
        )
        db.session.add(colaborador)
        db.session.commit()
        return jsonify({"mensaje": "Colaborador agregado correctamente"})


class ListarColaboradores(Resource):
    def get(self):
        db.create_all()
        colaboradores = Colaboradores.query.all()
        colaboradores = [
            {
                "id": colaborador.id,
                "nombre": colaborador.nombre,
                "apellido": colaborador.apellido,
                "institucion": colaborador.institucion,
            }
            for colaborador in colaboradores
        ]
        return jsonify(colaboradores)
    
class EditarColaborador(Resource):
    @jwt_required()
    def put(self):
        data = request.get_json()
        colaborador = Colaboradores.query.get(data.id)
        colaborador.nombre = data["nombre"]
        colaborador.apellido = data["apellido"]
        colaborador.institucion = data["institucion"]
        db.session.commit()
        return jsonify({"mensaje": "Colaborador editado correctamente"})

class EliminarColaborador(Resource):
    @jwt_required()
    def delete(self, id):
        colaborador = Colaboradores.query.get(id)
        db.session.delete(colaborador)
        db.session.commit()
        return jsonify({"mensaje": "Colaborador eliminado correctamente"})
        
    