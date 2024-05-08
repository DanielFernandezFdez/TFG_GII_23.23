from flask import Blueprint
from flask_restful import Api
from .recursosSugerencias import CrearSugerencia

sugerencias_bp = Blueprint('sugerencias', __name__)
api = Api(sugerencias_bp)

api.add_resource(CrearSugerencia, '/crear_sugerencia')