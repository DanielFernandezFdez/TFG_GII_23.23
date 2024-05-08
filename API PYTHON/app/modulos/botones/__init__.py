from flask import Blueprint
from flask_restful import Api
from .recursosBotones import buscarBotones, consultarBoton, CrearBoton, EditarBoton, BorrarBoton

botones_bp = Blueprint('botones', __name__)
api = Api(botones_bp)

api.add_resource(buscarBotones, '/buscar_botones')
api.add_resource(consultarBoton, '/consultar_boton/<int:id_usuario>')
api.add_resource(CrearBoton, '/crear_boton')
api.add_resource(EditarBoton, '/editar_boton')
api.add_resource(BorrarBoton, '/borrar_boton/<int:boton_id>')
