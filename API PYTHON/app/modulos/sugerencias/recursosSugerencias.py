from flask_restful import Resource
from flask import jsonify, request
from app.modelos.modelos import EstadisticasPorMes, db
import app.Funciones_Auxiliares.automatizar_correo as ac
from datetime import datetime

class  CrearSugerencia(Resource):
    def post(self):
        data = request.get_json()
        ac.mandarCorreo(data["nombre"],data["apellidos"],data["correo"],data["titulo"],data["isbn"])
        estadistica_existente = EstadisticasPorMes.query.filter_by(mes=datetime.now().strftime("%m"), anyo=datetime.now().strftime("%Y")).first()
        if estadistica_existente:
            estadistica_existente.numero_sugerencias = estadistica_existente.numero_sugerencias + 1
        else:
            nuevaEstadistica = EstadisticasPorMes(
            mes = datetime.now().strftime("%m"),
            anyo = datetime.now().strftime("%Y"),
            numero_sugerencias = 1
            )
            db.session.add(nuevaEstadistica)
        db.session.commit()

        return jsonify({"mensaje": "Sugerencia enviada exitosamente"})