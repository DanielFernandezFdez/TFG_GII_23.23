from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from . import db

class Libros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), unique=True, nullable=False)
    editorial = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    anyo_publicacion = db.Column(db.String(50))
    puntuacion = db.Column(db.Integer, nullable=True)
    ubicacion_estudio = db.Column(db.String(300))
    url_imagen = db.Column(db.String(300))
    visitas_mensuales = db.Column(db.Integer, default=0)
    visitas_totales = db.Column(db.Integer, default=0)
    mes_creacion = db.Column(db.String(100), nullable=False, default=datetime.now().strftime("%m"))
    anyo_creacion = db.Column(db.String(100), nullable=False, default=datetime.now().strftime("%Y"))
    puntuacion_masculino_generico = db.Column(db.Integer, nullable=True)
    puntuacion_menores = db.Column(db.Integer, nullable=True)
    puntuacion_adultos = db.Column(db.Integer, nullable=True)
    puntuacion_ubicacion = db.Column(db.Integer, nullable=True)
    puntuacion_actividades = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Libros {self.titulo}>"


class Libros_automaticos(db.Model):
    auto_id = db.Column(db.String(100), primary_key=True)
    logo = db.Column(db.String(300))
    disponible=db.Column(db.Boolean)
    titulo = db.Column(db.String(100))
    isbn = db.Column(db.String(100))
    editorial = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    anyo_publicacion = db.Column(db.String(50))
    url_imagen = db.Column(db.String(300))

    def __repr__(self):
        return f"<Libros {self.titulo}>"


class fecha_modificacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ultima_modificacion = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    @classmethod
    def actualizar_fecha_modificacion(cls):
        fecha = db.session.get(cls, 1)
        if not fecha:
            fecha = cls()
            db.session.add(fecha)
        FechaUTC = datetime.now(timezone.utc)
        zona_horaria_local = ZoneInfo("Europe/Berlin")
        fecha.ultima_modificacion = FechaUTC.astimezone(zona_horaria_local)

    def __repr__(self):
        return f"<Fecha Modificación: {self.ultima_modificacion}>"

class GestionEstimacion(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    actividades_produccion= db.Column(db.String(255), nullable=True)
    actividades_poder = db.Column(db.String(255), nullable=True)
    actividades_mantenimiento = db.Column(db.String(255), nullable=True)
    actividades_hombre= db.Column(db.String(255), nullable=True)
    actividades_mujer= db.Column(db.String(255), nullable=True)


class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(100), unique=True, nullable=False)
    usuarios = db.relationship('Usuarios', backref='rol', lazy='joined')

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasenya_encriptada = db.Column(db.String(128), nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    
class Botones(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_boton = db.Column(db.String(100), unique=True, nullable=False)
    roles_autorizados=db.Column(db.String(255), nullable=True)
    
    
class Estimacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    masculino_generico = db.Column(db.Boolean, nullable=False)
    numero_ninyas = db.Column(db.Integer, nullable=True)
    numero_ninyos = db.Column(db.Integer, nullable=True)
    numero_hombres = db.Column(db.Integer, nullable=False)
    numero_mujeres = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.Integer, nullable=False)
    res_actividades_hombre = db.Column(db.String(255), nullable=True)
    res_actividades_mujer = db.Column(db.String(255), nullable=True)
    titulo = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    institucion = db.Column(db.String(100), nullable=False)
    resultado = db.Column(db.Integer, nullable=False)
       
class EstadisticasPorMes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mes = db.Column(db.String(100), nullable=False)
    anyo = db.Column(db.String(100), nullable=False)
    numero_libros = db.Column(db.Integer, nullable=False)
    numero_visitas_totales = db.Column(db.Integer, nullable=False)
    numero_estimaciones = db.Column(db.Integer, nullable=False)
    numero_usuarios = db.Column(db.Integer, nullable=False)
    libro_mas_visitado = db.Column(db.String(100), nullable=False)
    isbn_libro_mas_visitado = db.Column(db.String(100), nullable=False)
    visitas_libro_mas_visitado = db.Column(db.Integer, nullable=False)
    url_imagen_libro_mas_visitado = db.Column(db.String(300), nullable=False)
    numero_sugerencias = db.Column(db.Integer, nullable = False)