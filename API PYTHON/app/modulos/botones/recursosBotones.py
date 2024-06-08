from flask_restful import Resource, request
from flask_jwt_extended import jwt_required
from flask import jsonify
from app.modelos.modelos import Botones, Usuarios, db
import json


class buscarBotones(Resource):
    def get(self):
        botones = Botones.query.all()
        return jsonify(
            [
                {
                    "id": boton.id,
                    "nombre": boton.nombre_boton,
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

        for nombre_boton in data['nombre_botones']: 
            boton = Botones.query.filter_by(nombre_boton=nombre_boton).first()
            if boton:
                roles_autorizados = json.loads(boton.roles_autorizados if boton.roles_autorizados else '[]')
                if roles_autorizados==[]:
                    autorizado = 1
                autorizado = 1 if rol_usuario in roles_autorizados else 0
            else:
                autorizado = 0  
            botones_respuesta.append(
                {
                "nombre": nombre_boton,
                "autorizado": autorizado
                })

        return jsonify(botones_respuesta)

class CrearBoton(Resource): #!Solo durante pruebas
    @jwt_required()
    def post(self):
        data = request.get_json()
        boton_existente=Botones.query.filter_by(nombre_boton=data['nombre_boton']).first()
        if boton_existente:
            respuesta = jsonify({"mensaje": "El boton ya existe"})
            respuesta.status_code = 400
            return respuesta
        nuevo_boton = Botones(
            nombre_boton=data['nombre_boton'],
            roles_autorizados=json.dumps(data['roles_autorizados'] if 'roles_autorizados' in data else []) 
        )
        db.session.add(nuevo_boton)
        db.session.commit()
        return jsonify({"mensaje": "Boton creado exitosamente"})



class EditarBoton(Resource):
    @jwt_required()
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
    @jwt_required()
    def delete(self, boton_id):
        boton = Botones.query.get_or_404(boton_id)
        db.session.delete(boton)
        db.session.commit()
        return jsonify({"mensaje": "Boton eliminado exitosamente"})   