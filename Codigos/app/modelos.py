from flask_login import UserMixin
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#Modelos
class Libros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), unique=True, nullable=False)
    editorial = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    año_publicacion = db.Column(db.String(50))
    puntuacion = db.Column(db.Integer, nullable=True)
    ubicacion_estudio = db.Column(db.String(300))
    url_imagen = db.Column(db.String(300))   

    def __repr__(self):
        return f'<Libros {self.titulo}>'
    

class Libros_automaticos(db.Model):
    auto_id = db.Column(db.String(100), primary_key=True)
    titulo = db.Column(db.String(100))
    isbn = db.Column(db.String(100))
    editorial = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    año_publicacion = db.Column(db.String(50))
    url_imagen = db.Column(db.String(300))   

    def __repr__(self):
        return f'<Libros {self.titulo}>'
    
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(128))

class fecha_modificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ultima_modificacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    
    @classmethod
    def actualizar_fecha_modificacion(cls):
        fecha = db.session.query(cls).get(1)
        if not fecha:
            fecha = cls()
            db.session.add(fecha)
        FechaUTC=datetime.now(timezone.utc)
        zona_horaria_local = ZoneInfo('Europe/Berlin')
        fecha.ultima_modificacion = FechaUTC.astimezone(zona_horaria_local)

    def __repr__(self):
        return f'<Fecha Modificación: {self.ultima_modificacion}>'

