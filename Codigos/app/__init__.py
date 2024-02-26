from flask import Flask
from flask_login import LoginManager
from app.modelos import *




login_manager = LoginManager()
#Operaciones de Login



@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

def creacion():
    # Instancia de Flask
    app = Flask(__name__)
    app.secret_key = 'v2s7*fp(z8WUr1hCUR({"-Q|yG5muk`?Nd|Ut@cz2E:ZJ[}0/['  # Clave secreta para las sesiones
    # Configuración de la BD
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Libros.db"  # Ruta de la BD
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Rutas
    from app.routes.estado_sesion import estado_sesion
    from app.routes.modificacion_auto import modificacion_auto
    from app.routes.modificacion_libros import modificacion_libros
    from app.routes.pantallas_generales import pantallas_generales
    app.register_blueprint(estado_sesion)
    app.register_blueprint(modificacion_auto)
    app.register_blueprint(modificacion_libros)
    app.register_blueprint(pantallas_generales)
    login_manager.init_app(app)
    login_manager.login_view = 'login'  # La ruta que redirige para el login

    return app
