from flask import Blueprint
from flask_restful import Api
from .recursosRoles import ObtenerRoles, ConsultarRol, CrearRol, EditarRol, BorrarRol

roles_bp = Blueprint('roles', __name__)
api = Api(roles_bp)

api.add_resource(ObtenerRoles, '/roles')
api.add_resource(ConsultarRol, '/consultar_rol/<int:id>')
api.add_resource(CrearRol, '/crear_rol')
api.add_resource(EditarRol, '/editar_rol/<int:rol>')
api.add_resource(BorrarRol, '/borrar_rol/<int:rol>')
