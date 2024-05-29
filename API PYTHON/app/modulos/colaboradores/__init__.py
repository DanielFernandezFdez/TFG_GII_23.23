from flask import Blueprint
from flask_restful import Api

from .colaboradores import AgregarColaborador, ListarColaboradores, EditarColaborador, EliminarColaborador

colaboradores_bp = Blueprint('colaboradores', __name__)
api = Api(colaboradores_bp)

api.add_resource(AgregarColaborador, '/agregarColaborador')
api.add_resource(ListarColaboradores, '/listarColaboradores')
api.add_resource(EditarColaborador, '/editarColaborador')
api.add_resource(EliminarColaborador, '/eliminarColaborador/<int:id>')