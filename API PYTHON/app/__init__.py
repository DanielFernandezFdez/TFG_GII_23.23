from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from .modelos import db
from .config import Config

def creacionApp():
    app = Flask(__name__)
    app.config.from_object(Config)


    db.init_app(app)
    JWTManager(app)
    CORS(app)
    api = Api(app)

    from .modulos.botones import botones_bp
    from .modulos.gestionEstimacion import gestion_estimacion_bp
    from .modulos.gestionLibros import gestion_libros_bp
    from .modulos.importacionExportacion import import_export_bp
    from .modulos.roles import roles_bp
    from .modulos.sugerencias import sugerencias_bp
    from .modulos.usuarios import usuarios_bp
    
    app.register_blueprint(botones_bp, url_prefix='/botones')
    app.register_blueprint(gestion_estimacion_bp, url_prefix='/gestion-estimacion')
    app.register_blueprint(gestion_libros_bp, url_prefix='/gestion-libros')
    app.register_blueprint(import_export_bp, url_prefix='/import-export')
    app.register_blueprint(roles_bp, url_prefix='/roles')
    app.register_blueprint(sugerencias_bp, url_prefix='/sugerencias')
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')

    return app

if __name__ == "__main__":
    creacionApp().run(debug=True)
