#Imports
from flask import redirect,url_for,Response
import csv
from io import StringIO
from datetime import datetime,timezone
from app.modelos import *
from app.__init__ import *

#Funcion de exportar a CSV
def exportar_csv():
    si = StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Escribe los encabezados en el archivo CSV
    cw.writerow(['ID', 'Título', 'ISBN', 'Editorial', 'Descripción', 'Año de publicación',"Puntuación", 'Ubicación del estudio', 'URL de la imagen'])

    # Obtiene todos los libros de la base de datos
    libros = Libros.query.all()

    # Escribe los datos de cada libro en el archivo CSV
    for libro in libros:
        cw.writerow([libro.id, libro.titulo, libro.isbn, libro.editorial, libro.descripcion, libro.año_publicacion,libro.puntuacion, libro.ubicacion_estudio, libro.url_imagen])

    output = si.getvalue()

    # Crea una respuesta HTTP con el archivo CSV
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=libros.csv"}
    )

def importar_csv(archivo):
    stream = StringIO(archivo.stream.read().decode("UTF-8"), newline=None)
    csv_input = csv.reader(stream,delimiter=';')

    # Borrar los datos existentes si es necesario
    Libros.query.delete()

    # Recorrer cada fila del CSV y actualizar la base de datos
    for i, row in enumerate(csv_input):
        if i == 0:
            # Saltar la fila de encabezados
            continue

        # Crear una nueva instancia del modelo Libros por cada fila
        nuevo_libro = Libros(
            titulo=row[1],
            isbn=row[2],
            editorial=row[3],
            descripcion=row[4],
            año_publicacion=row[5],
            puntuacion=row[6],
            ubicacion_estudio=row[7],
            url_imagen=row[8]
        )

        # Agregar el nuevo libro a la sesión de la base de datos
        db.session.add(nuevo_libro)
    # Actualizar la fecha de última modificación
        fecha = db.session.get(fecha_modificacion, 1)  # Asumiendo que solo tienes un registro para esto
        print(fecha.ultima_modificacion)
        if not fecha:
            # Si no existe un registro, crea uno nuevo
            fecha = fecha_modificacion(id=1, ultima_modificacion=datetime.now(timezone.utc))
            db.session.add(fecha)
        fecha.actualizar_fecha_modificacion()

    # Confirmar los cambios en la base de datos
    db.session.commit()
    print('Datos importados')
    # Redireccionar o enviar una respuesta adecuada
    return redirect(url_for('pantallas_generales.catalogo'))