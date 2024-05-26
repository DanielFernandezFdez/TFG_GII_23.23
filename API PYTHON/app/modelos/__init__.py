from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .modelos import Libros, Libros_automaticos, fecha_modificacion, GestionEstimacion, Roles, Usuarios, Botones, Estimacion, EstadisticasPorMes,EstadisticasPorMesAuxiliar