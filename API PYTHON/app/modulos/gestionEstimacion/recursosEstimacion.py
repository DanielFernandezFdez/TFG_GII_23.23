from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import jsonify, request, Response
from datetime import datetime
from sqlalchemy import and_
from io import StringIO, BytesIO
import csv
from app.modelos import db, EstadisticasPorMes, Estimacion, GestionEstimacion, Libros, Usuarios

import json

def  ActualizarEstadisticasMensuales():

    estadistica_existente = EstadisticasPorMes.query.filter_by(mes=datetime.now().strftime("%m"), anyo=datetime.now().strftime("%Y")).first()
    libros = Libros.query.all()
    estimaciones = Estimacion.query.all()
    usuarios = Usuarios.query.all()
    numero_libros = len(libros)
    numero_estimaciones = len(estimaciones)
    numero_usuarios = len(usuarios)

    maxVisitas=0
    libro_mas_visitado = ""
    isbn_mas_visitado = ""
    url_imagen_mas_visitado = ""
    visitasTotales = 0

    for libro in libros :
        visitasTotales = visitasTotales + libro.visitas_mensuales
        if libro.visitas_mensuales >= maxVisitas:
            maxVisitas = libro.visitas_mensuales
            libro_mas_visitado = libro.titulo
            isbn_mas_visitado = libro.isbn
            url_imagen_mas_visitado = libro.url_imagen
 
    if estadistica_existente:
        estadistica_existente.numero_libros = numero_libros
        estadistica_existente.numero_estimaciones = numero_estimaciones
        estadistica_existente.numero_usuarios = numero_usuarios
        estadistica_existente.libro_mas_visitado = libro_mas_visitado
        estadistica_existente.isbn_libro_mas_visitado = isbn_mas_visitado
        estadistica_existente.visitas_libro_mas_visitado = maxVisitas
        estadistica_existente.url_imagen_libro_mas_visitado = url_imagen_mas_visitado
        estadistica_existente.numero_visitas_totales = visitasTotales

    else:
        nuevaEstadistica = EstadisticasPorMes(
            mes = datetime.now().strftime("%m"),
            anyo = datetime.now().strftime("%Y"),
            numero_libros = numero_libros,
            numero_estimaciones = numero_estimaciones,
            numero_usuarios = numero_usuarios,
            libro_mas_visitado = libro_mas_visitado,
            isbn_libro_mas_visitado = isbn_mas_visitado,
            visitas_libro_mas_visitado = maxVisitas,
            url_imagen_libro_mas_visitado = url_imagen_mas_visitado,
            numero_visitas_totales = visitasTotales,
            numero_sugerencias = 0
        )
        db.session.add(nuevaEstadistica)
    db.session.commit()




class ObtenerEstadisticasGraficosGenerales(Resource):
    def post(self):
        data = request.get_json()
        ActualizarEstadisticasMensuales()
        query = EstadisticasPorMes.query
        if 'mes_inicio' in data and 'anyo_inicio' in data and 'mes_fin' in data and 'anyo_fin' in data:
            mes_inicio = int(data['mes_inicio'])
            anyo_inicio = int(data['anyo_inicio'])
            mes_fin = int(data['mes_fin'])
            anyo_fin = int(data['anyo_fin'])

            query = query.filter(and_(
                EstadisticasPorMes.anyo >= anyo_inicio,
                EstadisticasPorMes.mes >= mes_inicio,
                EstadisticasPorMes.anyo <= anyo_fin,
                EstadisticasPorMes.mes <= mes_fin
            ))
        else:
            query = query.filter(EstadisticasPorMes.anyo == datetime.now().strftime("%Y"))
        estadisticas = query.all()

        return jsonify([
            {
                "mes": estadistica.mes,
                "anyo": estadistica.anyo,
                "numero_libros": estadistica.numero_libros,
                "numero_estimaciones": estadistica.numero_estimaciones,
                "numero_usuarios": estadistica.numero_usuarios,
                "libro_mas_visitado": estadistica.libro_mas_visitado,
                "isbn_libro_mas_visitado": estadistica.isbn_libro_mas_visitado,
                "visitas_libro_mas_visitado": estadistica.visitas_libro_mas_visitado,
                "url_imagen_libro_mas_visitado": estadistica.url_imagen_libro_mas_visitado,
                "numero_visitas_totales": estadistica.numero_visitas_totales,
                "numero_sugerencias" : estadistica.numero_sugerencias

            }
            for estadistica in estadisticas
        ])

class GenerarListados(Resource):
    @jwt_required()
    def post(self):
        data=request.get_json()
        db.session.query(GestionEstimacion).delete()
        db.session.commit()
        listado_nuevo = GestionEstimacion(
            actividades_produccion= json.dumps(data["actividades_produccion"] if "actividades_produccion" in data else []),
            actividades_poder = json.dumps(data["actividades_poder"] if "actividades_poder" in data else []),
            actividades_mantenimiento = json.dumps(data["actividades_mantenimiento"] if "actividades_mantenimiento" in data else []),
            actividades_hombre= json.dumps(data["actividades_hombre"] if "actividades_hombre" in data else []),
            actividades_mujer= json.dumps(data["actividades_mujer"] if "actividades_mujer" in data else []),
            
        )
        db.session.add(listado_nuevo)
        db.session.commit()
        return jsonify(
            {
                "Ok":"OK"
            }
        )

class ObtenerListados(Resource):
    def get(self):
        listados=GestionEstimacion.query.get_or_404(1)
        return jsonify(
            {
                "actividades_produccion" : json.loads(listados.actividades_produccion),
                "actividades_poder" : json.loads(listados.actividades_poder),
                "actividades_mantenimiento" : json.loads(listados.actividades_mantenimiento),
                "actividades_hombre" : json.loads(listados.actividades_hombre),
                "actividades_mujer" : json.loads(listados.actividades_mujer)
            }
        )

class BorrarListados(Resource):
    @jwt_required()
    def delete(self):
        db.session.delete(GestionEstimacion.query.get_or_404(1))
        db.session.commit()
        return jsonify(
            {
                "resultado":"OK"
            }
        )

class CalcularEstimacion(Resource):
    def post(self):
        resultado=0
        data=request.get_json()


        ponderacion_adultos=0.15
        ponderacion_ninyos = 0.15
        ponderacion_actividad=0.3

        #?Apartado de masculino generico
        masculino_generico=data["masculino_generico"]
        if masculino_generico==False:
            resultado=20
        
        #? Apartado de calculos de niños
        if data["numero_ninyos"]!=0 or data["numero_ninyas"]!=0 in data :
            numero_ninyos = data["numero_ninyos"]
            numero_ninyas = data["numero_ninyas"]
            suma=numero_ninyos+numero_ninyas
            if numero_ninyos> numero_ninyas:
                proporcion= numero_ninyas/suma
                sobre100_ninyos=proporcion*2 #50 seria lo ideal por lo tanto al hacer regla de 3 con multiplicar por 2 se saca
                resultado+=ponderacion_ninyos*sobre100_ninyos*100
            else:
                proporcion= numero_ninyos/suma
                sobre100_ninyos=proporcion*2 #50 seria lo ideal por lo tanto al hacer regla de 3 con multiplicar por 2 se saca
                resultado+=ponderacion_ninyos*sobre100_ninyos*100

        else:
            ponderacion_adultos=0.3


        #? Apartado calculos de adultos
        numero_hombres=data["numero_hombres"]
        numero_mujeres=data["numero_mujeres"]
        suma=numero_hombres+numero_mujeres
        if numero_hombres> numero_mujeres:
            proporcion= numero_mujeres/suma
            sobre100_adultos=proporcion*2 #50 seria lo ideal por lo tanto al hacer regla de 3 con multiplicar por 2 se saca
            resultado+=ponderacion_adultos*sobre100_adultos*100
        else:
            proporcion= numero_hombres/suma
            sobre100_adultos=proporcion*2 #50 seria lo ideal por lo tanto al hacer regla de 3 con multiplicar por 2 se saca
            resultado+=ponderacion_adultos*sobre100_adultos*100


        #?Apartado de listados de actividades
        res_actividades_hombre = data.get("res_actividades_hombre",[])
        res_actividades_mujer = data.get("res_actividades_mujer",[])

        actividades = GestionEstimacion.query.get_or_404(1)
        mejor_hombres = json.loads(actividades.actividades_hombre)
        mejor_mujeres = json.loads(actividades.actividades_mujer)

        contador_comun = 0
        contador_total = 0

        if len(res_actividades_hombre) != 0:
            for actividad_hombre in res_actividades_hombre:

                if actividad_hombre in mejor_hombres:
                    contador_comun += 1
                contador_total += 1

        if len(res_actividades_mujer) != 0:
            for actividad_mujer in res_actividades_mujer:

                if actividad_mujer in mejor_mujeres:
                    contador_comun += 1
                contador_total += 1

        proporcion = contador_comun / contador_total if contador_total != 0 else 0
        resultado += proporcion * ponderacion_actividad * 100


        #? Calculo de ubicacion, se pasa ya el valor correspondiente 0 a 100 

        resultado+=data["ubicacion"]*0.2


        return jsonify(
            {
                "resultado": round(resultado),
            }
        )


class guardarEstimacion(Resource):
    def post(self):
        data=request.get_json()
        estimacion = Estimacion(
            masculino_generico=data["masculino_generico"] if "masculino_generico" in data else False,
            numero_ninyas=data["numero_ninyas"] if "numero_ninyas" in data else 0,
            numero_ninyos=data["numero_ninyos"] if "numero_ninyos" in data else 0,
            numero_hombres=data["numero_hombres"] if "numero_hombres" in data else 0,
            numero_mujeres=data["numero_mujeres"] if "numero_mujeres" in data else 0,
            ubicacion=data["ubicacion"] if "ubicacion" in data else 0,
            res_actividades_hombre=json.dumps(data["res_actividades_hombre"] if "res_actividades_hombre" in data else []),
            res_actividades_mujer=json.dumps(data["res_actividades_mujer"] if "res_actividades_mujer" in data else []),
            titulo=data["titulo"] if "titulo" in data else "No disponible",
            isbn=data["isbn"] if "isbn" in data else "No disponible",
            nombre=data["nombre"] if "nombre" in data else "No disponible",
            apellido=data["apellido"] if "apellido" in data else "No disponible",
            correo=data["correo"] if "correo" in data else "No disponible",
            institucion=data["institucion"] if "institucion" in data else "No disponible",
            resultado=data["resultado"] if "resultado" in data else 0
        )
        db.session.add(estimacion)
        db.session.commit()
        return jsonify(
            {
                "Ok":"OK"
            }
        )

class listarEstimaciones(Resource):
    @jwt_required()
    def get(self):
        estimaciones = Estimacion.query.all()
        return jsonify(
            [
                {
                    "id": estimacion.id,
                    "masculino_generico": estimacion.masculino_generico,
                    "numero_ninyas": estimacion.numero_ninyas,
                    "numero_ninyos": estimacion.numero_ninyos,
                    "numero_hombres": estimacion.numero_hombres,
                    "numero_mujeres": estimacion.numero_mujeres,
                    "ubicacion": estimacion.ubicacion,
                    "res_actividades_hombre": json.loads(estimacion.res_actividades_hombre),
                    "res_actividades_mujer": json.loads(estimacion.res_actividades_mujer),
                    "titulo": estimacion.titulo,
                    "isbn": estimacion.isbn,
                    "nombre": estimacion.nombre,
                    "apellido": estimacion.apellido,
                    "correo": estimacion.correo,
                    "institucion": estimacion.institucion,
                    "resultado": estimacion.resultado
                }
                for estimacion in estimaciones
            ]
        )
        
class BorrarEstimacion(Resource):
    @jwt_required()
    def delete(self, id):
        estimacion = Estimacion.query.get_or_404(id)
        db.session.delete(estimacion)
        db.session.commit()
        return jsonify({"mensaje": "Estimación eliminada exitosamente"})
    
    
class DescargarEstimacionCSV(Resource):
    @jwt_required()
    def get(self, id):
        estimacion = Estimacion.query.get_or_404(id)
        si = StringIO()
        cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        cw.writerow(['Masculino Genérico', 'Numero de niñas', 'Numero de niños', 'Número de hombres', 'Número de mujeres', 
                     'Ubicación', 'Resultado actividades hombre', 'Resultado actividades mujer', 'Título', 'ISBN', 
                     'Nombre', 'Apellido', 'Correo', 'Institución', 'Resultado'])
        
        cw.writerow([
            estimacion.masculino_generico, estimacion.numero_ninyas, estimacion.numero_ninyos, estimacion.numero_hombres,
            estimacion.numero_mujeres, estimacion.ubicacion, estimacion.res_actividades_hombre, estimacion.res_actividades_mujer,
            estimacion.titulo, estimacion.isbn, estimacion.nombre, estimacion.apellido, estimacion.correo, estimacion.institucion,
            estimacion.resultado
        ])
        
        output = si.getvalue()
        output = '\ufeff' + output  # BOM para que Excel maneje correctamente utf-8
        output = output.encode('utf-8')

        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment;filename=estimacion.csv"}
        )
        
