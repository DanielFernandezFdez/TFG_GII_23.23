import requests
from bs4 import BeautifulSoup
import re

parser = "html.parser"
descripcion = "No se ha encontrado descripción"
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
languaje = "es; q=0.5"
sintitulo = "No se ha encontrado título"
sineditorial = "No se ha encontrado editorial"


def obtener_resumen_extendido(isbn):
    url_endpoint = "https://www.agapea.com/ajax/funcionesAjaxResumen.inc.php"

    data = {"ISBN": isbn, "col": "0", "res": "1"}  # ISBN del libro

    # Cabeceras necesarias para la solicitud
    headers = {
        "User-Agent": "Mozilla/5.0 (Tu User Agent)",
        "Referer": "https://www.agapea.com",
        "X-Requested-With": "XMLHttpRequest",  # Esto indica que es una solicitud de AJAX
    }

    # Realiza la solicitud POST al endpoint
    respuesta = requests.post(url_endpoint, headers=headers, data=data)

    if respuesta.status_code == 200:
        # Decodificar correctamente el contenido
        contenido_html = respuesta.content.decode("utf-8")

        # Analizar el contenido HTML
        soup = BeautifulSoup(contenido_html, parser)

        # Extraer el texto plano de la descripción
        descrip = soup.get_text(strip=True)
        if descrip:
            return descrip
        
    return descripcion


def buscar_libro_amazon(elemento):
    contador_intentos=0
    headers = {
        "User-Agent": userAgent,
        "Accept-Languaje": languaje,
    }

    url_busqueda = f"https://www.amazon.es/s?k={elemento}"

    respuesta = requests.get(url_busqueda, headers=headers)
    informacion = ['Amazon','amazon-logo.svg',True]
    if respuesta.status_code == 200:
        instancia = BeautifulSoup(respuesta.content, parser)

        primer_resultado = instancia.find(
            "div", {"data-component-type": "s-search-result"}
        )

        if primer_resultado:
            zona_titulo = primer_resultado.find("div", {"data-cy": "title-recipe"})
            link = zona_titulo.find("a", {"class": "a-link-normal"})["href"]
            book_url = "https://www.amazon.es" + link
        
        while contador_intentos < 3:
            contador_sin_datos = 0
            contador_intentos += 1
            respuesta_libro = requests.get(book_url, headers=headers)

            if respuesta_libro.status_code == 200:
                instancia_libro = BeautifulSoup(respuesta_libro.content, parser)

                encontradoISBN10 = False
                encontradoISBN13 = False
                encontradoEditorial = False
                encontradoFecha = False
                
               
                titulo = instancia_libro.find("span", id="productTitle")
                if titulo:
                    titulo = titulo.get_text(strip=True)
                    informacion.append(titulo)
                else:
                    informacion.append(sintitulo)
                    contador_sin_datos += 1

                ISBNyeditorial = instancia_libro.find(
                    "div", id="richProductInformation_feature_div"
                )
                

                if ISBNyeditorial:
                    temp=[None, None, None, None]
                    for elem in ISBNyeditorial.find_all("li"):

                        div_ISBN10 = elem.find(
                            "div", id="rpi-attribute-book_details-isbn10"
                        )
                        div_ISBN13 = elem.find(
                            "div", id="rpi-attribute-book_details-isbn13"
                        )
                        div_editorial = elem.find(
                            "div", id="rpi-attribute-book_details-publisher"
                        )
                        div_fecha = elem.find(
                            "div", id="rpi-attribute-book_details-publication_date"
                        )
                        if div_ISBN10:
                            ISBN10_sin = div_ISBN10.find_all("span")
                            if ISBN10_sin:
                                ISBN10 = ISBN10_sin[2]
                                ISBN10 = ISBN10.get_text(strip=True)
                                ISBN10 = ISBN10.replace("-", "")
                                temp[0]=ISBN10
                                encontradoISBN10 = True

                        if div_ISBN13:
                            ISBN13_sin = div_ISBN13.find_all("span")
                            if ISBN13_sin:
                                ISBN13 = ISBN13_sin[2]
                                ISBN13 = ISBN13.get_text(strip=True)
                                ISBN13 = ISBN13.replace("-", "")
                                temp[1]=ISBN13
                                encontradoISBN13 = True

                        if div_editorial:
                            editorial_sin = div_editorial.find_all("span")
                            if editorial_sin:
                                editorial = editorial_sin[2]
                                editorial = editorial.get_text(strip=True)
                                temp[2]=editorial
                                encontradoEditorial = True

                        if div_fecha:
                            fecha_sin = div_fecha.find_all("span")
                            if fecha_sin:
                                fecha = fecha_sin[2]
                                fecha = fecha.get_text(strip=True)
                                patron = r"\b(19|20)\d{2}\b"
                                fecha = re.search(patron, fecha)
                                temp[3]=fecha.group()
                                encontradoFecha = True

                if not encontradoISBN10:
                    informacion.append("No se ha encontrado ISBN10")
                    contador_sin_datos += 1
                else:
                    informacion.append(temp[0])
                if not encontradoISBN13:
                    informacion.append("No se ha encontrado ISBN13")
                    contador_sin_datos += 1
                else:
                    informacion.append(temp[1])
                if not encontradoEditorial:
                    informacion.append(sineditorial)
                    contador_sin_datos += 1
                else:
                    informacion.append(temp[2])
                if not encontradoFecha:
                    informacion.append("No se ha encontrado fecha")
                    contador_sin_datos += 1
                else:
                    informacion.append(temp[3])
                
                zonadescrip = instancia_libro.find(
                    "div", id="bookDescription_feature_div"
                )
                if zonadescrip:
                    descrip = zonadescrip.find(
                        "div", {"class": "books-expander-content"}
                    )
                    if descrip:
                        descrip = descrip.get_text(strip=True)
                        informacion.append(descrip)
                    else:
                        zonadescrip = zonadescrip.get_text(strip=True)
                        informacion.append(zonadescrip)
                else:
                    informacion.append(descripcion)
                    contador_sin_datos += 1

                imagen_find = instancia.find("img", class_="s-image")

                if imagen_find:
                    imagen = imagen_find["src"]
                    informacion.append(imagen)
                else:
                    informacion.append("No se pudo encontrar la etiqueta de la imagen.")
                    contador_sin_datos += 1
                    
            if contador_sin_datos == 0:
                return informacion
    
    informacion[2] =False      
    return informacion


def buscar_libro_agapea_libro(info):

    headers = {
        "User-Agent": userAgent,
        "Accept-Languaje": languaje,
    }

    url_busqueda = f"https://www.agapea.com/buscar/buscador.php?texto={info}"

    respuesta = requests.get(url_busqueda, headers=headers)
    if respuesta.status_code == 200:

        instancia = BeautifulSoup(respuesta.content, parser)

        primer_resultado = instancia.find("div", {"class": "resultados"})
        if primer_resultado:
            primer_resultado = primer_resultado.find("li", {"class": "resumen-mini"})

        if primer_resultado:
            primer_resultado = primer_resultado.find("div", {"class": "info1"})
            link = primer_resultado.find("a")["href"]
            link = f"https://www.agapea.com{link}"

            respuesta_libro = requests.get(link, headers=headers)

            if respuesta_libro.status_code == 200:
                instancia_libro = BeautifulSoup(respuesta_libro.content, parser)
                info = buscar_libro_agapea_generico(instancia_libro)

            return info
    return None


def buscar_libro_agapea_isbn(info):

    headers = {
        "User-Agent": userAgent,
        "Accept-Languaje": languaje,
    }

    url_busqueda = f"https://www.agapea.com/buscar/buscador.php?texto={info}"

    respuesta = requests.get(url_busqueda, headers=headers)

    if respuesta.status_code == 200:

        instancia_libro = BeautifulSoup(respuesta.content, parser)
        info_libro = instancia_libro.find("div", {"id": "cnt-busqueda"})
        if info_libro:
            return None
        info = buscar_libro_agapea_generico(instancia_libro)
        return info
    return None


def buscar_libro_agapea_generico(instancia_libro):

    informacion = ['Agapea','agapea-logo.png',True]
    if instancia_libro==None:
        informacion[2] = False
        return informacion
    info_libro = instancia_libro.find("div", {"class": "datos-libro"})
    titulo = info_libro.find("h1")

    if titulo:
        titulo = titulo.get_text(strip=True)
        informacion.append(titulo)
    else:
        informacion.append(sintitulo)

    info_espe = instancia_libro.find("div", {"class": "detalles-libro"})

    # Encontrar todas las filas de la tabla
    filas = info_espe.find_all("tr")

    encontradoISBN10 = False
    encontradoISBN13 = False
    encontradoEditorial = False
    encontradoFecha = False
    for fila in filas:
        # Buscar las celdas de encabezado y de datos en la fila
        celda_encabezado = fila.find("th")

        celda_dato = fila.find("td")

        if celda_encabezado and celda_encabezado.get_text(strip=True) == "ISBN-10":
            ISBN10 = celda_dato.get_text(strip=True)
            ISBN10 = ISBN10[:10]
            encontradoISBN10 = True
        elif celda_encabezado and celda_encabezado.get_text(strip=True) == "ISBN":
            ISBN13 = celda_dato.get_text(strip=True)
            ISBN13 = ISBN13[:13]
            encontradoISBN13 = True
        elif celda_encabezado and celda_encabezado.get_text(strip=True) == "Editorial":
            Editorial = celda_dato.get_text(strip=True)
            encontradoEditorial = True
        elif celda_encabezado and celda_encabezado.get_text(strip=True) == "Edición":
            fecha = celda_dato.get_text(strip=True)
            patron = r"\b(19|20)\d{2}\b"
            fecha = re.search(patron, fecha)
            encontradoFecha = True

    if not encontradoISBN10:
        informacion.append("No se ha encontrado ISBN10")
    else:
        informacion.append(ISBN10)
    if not encontradoISBN13:
        informacion.append("No se ha encontrado ISBN13")
    else:
        informacion.append(ISBN13)
    if not encontradoEditorial:
        informacion.append(sineditorial)
    else:
        informacion.append(Editorial)
    if not encontradoFecha:
        informacion.append("No se ha encontrado fecha")
    else:
        informacion.append(fecha.group())

    resumen_extendido = obtener_resumen_extendido(ISBN13)
    informacion.append(resumen_extendido)

    imagen_find = instancia_libro.find("img", class_="front portada")

    if imagen_find:
        imagen = imagen_find["src"]
        informacion.append(imagen)
    else:
        informacion.append("No se pudo encontrar la etiqueta de la imagen.")
    return informacion




def obtener_info_libro_google(isbn_o_titulo, filtro):
    libros_con_descripcion = ['Google Books','google-logo.png',True]
    base_url = "https://www.googleapis.com/books/v1/volumes"
    if filtro == "isbn":
        parametros = {"q": f"isbn:{isbn_o_titulo}", "maxResults": 1}
    else:
        parametros = {"q": f"intitle:{isbn_o_titulo}", "maxResults": 1}
    try:
        respuesta = requests.get(base_url, params=parametros)
        respuesta.raise_for_status()  # Esto lanzará un error si la solicitud falla.
        resultado = respuesta.json()
        libros = resultado.get('items', [])
        if not libros:
            libros_con_descripcion[2] = False
            return libros_con_descripcion

        for libro in libros:
            info = libro['volumeInfo']
            libros_con_descripcion.append(info.get("title", sintitulo))
            libros_con_descripcion.append(next((ident['identifier'] for ident in info.get("industryIdentifiers", []) if ident["type"] == "ISBN_10"), "No se ha encontrado ISBN-10"))
            libros_con_descripcion.append(next((ident['identifier'] for ident in info.get("industryIdentifiers", []) if ident["type"] == "ISBN_13"), "No se ha encontrado ISBN-13"))
            libros_con_descripcion.append(info.get("publisher", sineditorial))
            libros_con_descripcion.append(info.get("publishedDate", "No se ha encontrado año de publicación"))
            libros_con_descripcion.append(info.get("description", descripcion))
            libros_con_descripcion.append(info.get("imageLinks", {}).get("thumbnail", "No se ha encontrado portada"))
        return libros_con_descripcion
    except requests.RequestException:
        libros_con_descripcion[2] = False
        return libros_con_descripcion





def buscar_libro(isbn_o_titulo):
    if re.match(r"\d{13}", isbn_o_titulo):
        descripcionAgapea = buscar_libro_agapea_isbn(isbn_o_titulo)
        descripcionAmazon = buscar_libro_amazon(isbn_o_titulo)
        descripcionGoogle = obtener_info_libro_google(isbn_o_titulo, "isbn")
    else:
        descripcionAgapea = buscar_libro_agapea_libro(isbn_o_titulo)
        descripcionAmazon = buscar_libro_amazon(isbn_o_titulo)
        descripcionGoogle = obtener_info_libro_google(isbn_o_titulo, "titulo")
    return [descripcionAgapea, descripcionAmazon, descripcionGoogle]




buscar_libro("9798321713754")

