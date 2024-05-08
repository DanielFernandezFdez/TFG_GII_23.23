from flask import Blueprint
from flask_restful import Api
from .recursosImportExport import ExportarCSV, ExportarExcel, ImportarArchivo

import_export_bp = Blueprint('import_export', __name__)
api = Api(import_export_bp)

api.add_resource(ExportarCSV, '/exportar_csv')
api.add_resource(ExportarExcel, '/exportar_excel')
api.add_resource(ImportarArchivo, '/importar_archivo')