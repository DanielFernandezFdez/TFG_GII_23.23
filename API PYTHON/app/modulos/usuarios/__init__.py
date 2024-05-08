from flask import Blueprint
from flask_restful import Api
from .recursosUsuarios import RegistroUsuario, Login, ModificarUsuario, EliminarUsuario, ListarUsuarios, InfoUsuario

usuarios_bp = Blueprint('usuarios', __name__)
api = Api(usuarios_bp)


api.add_resource(RegistroUsuario, '/registro')
api.add_resource(Login, '/login')
api.add_resource(ModificarUsuario, '/modificar_usuario/<int:user_id>')
api.add_resource(EliminarUsuario, '/eliminar_usuario/<int:user_id>')
api.add_resource(ListarUsuarios, '/usuarios')
api.add_resource(InfoUsuario, '/info_usuario/<int:user_id>')
