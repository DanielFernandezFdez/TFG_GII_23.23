#Imports
from flask import redirect,url_for,Response
import csv
from io import StringIO
from datetime import datetime,timezone
from app.modelos import *
from app.__init__ import *


def exportar_csv():
    si = StringIO()
    cw = csv.writer(si, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

   
    cw.writerow(['ID', 'Título', 'ISBN', 'Editorial', 'Descripción', 'Año de publicación',"Puntuación", 'Ubicación del estudio', 'URL de la imagen'])

  
    libros = Libros.query.all()

    
    for libro in libros:
        cw.writerow([libro.id, libro.titulo, libro.isbn, libro.editorial, libro.descripcion, libro.año_publicacion,libro.puntuacion, libro.ubicacion_estudio, libro.url_imagen])

    output = si.getvalue()


    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=libros.csv"}
    )

def importar_csv(archivo):
    stream = StringIO(archivo.stream.read().decode("UTF-8"), newline=None)
    csv_input = csv.reader(stream,delimiter=';')


    Libros.query.delete()


    for i, row in enumerate(csv_input):
        if i == 0:
      
            continue

      
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

        
        db.session.add(nuevo_libro)
   
        fecha = db.session.get(fecha_modificacion, 1)  
        print(fecha.ultima_modificacion)
        if not fecha:
           
            fecha = fecha_modificacion(id=1, ultima_modificacion=datetime.now(timezone.utc))
            db.session.add(fecha)
        fecha.actualizar_fecha_modificacion()


    db.session.commit()
    print('Datos importados')

    return redirect(url_for('pantallas_generales.catalogo'))