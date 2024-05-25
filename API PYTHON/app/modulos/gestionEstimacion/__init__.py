
from flask import Blueprint
from flask_restful import Api

from .recursosEstimacion import ObtenerEstadisticasGraficosGenerales, GenerarListados, ObtenerListados, BorrarListados, CalcularEstimacion, guardarEstimacion, listarEstimaciones, BorrarEstimacion, DescargarEstimacionCSV

gestion_estimacion_bp = Blueprint('gestion_estimacion', __name__)
api = Api(gestion_estimacion_bp)



api.add_resource(ObtenerEstadisticasGraficosGenerales, '/obtenerEstadisticasGraficosGenerales')
api.add_resource(GenerarListados, '/generarListados')
api.add_resource(ObtenerListados, '/obtenerListados')
api.add_resource(BorrarListados, '/borrarListados')
api.add_resource(CalcularEstimacion, '/calcularEstimacion')
api.add_resource(guardarEstimacion, '/guardarEstimacion')
api.add_resource(listarEstimaciones, '/listarEstimaciones')
api.add_resource(BorrarEstimacion, '/borrarEstimacion/<int:id>')
api.add_resource(DescargarEstimacionCSV, '/descargarEstimacionCSV/<int:id>')