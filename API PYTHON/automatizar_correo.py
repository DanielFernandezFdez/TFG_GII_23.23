from  email.message import EmailMessage
from datetime import datetime
from zoneinfo import ZoneInfo
import smtplib
import ssl

def mandarCorreo(nombre,  apellidos, correo,titulo,  isbn):
    email = 'prehistolibros@gmail.com'
    email_contrasena = 'jktz jmdk fhlq fzsa'
    asunto = 'Solicitud de libro'
    espana = ZoneInfo("Europe/Madrid")
    fecha_espana = datetime.now(espana)
    cuerpo = nombre + ' ' + apellidos + ' con Correo: ' + correo + ' ha sugerido el siguiente libro:\n Titulo: ' + titulo + '\nISBN: ' + isbn  +  '\n Fecha de solicitud: ' + str(fecha_espana)
    
    
    em = EmailMessage()
    em['From'] = email
    em['To'] = email
    em['Subject'] = asunto
    em.set_content(cuerpo)
    
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=contexto) as servidor:
        servidor.login(email, email_contrasena)
        servidor.sendmail(email, email, em.as_string())
        servidor.quit()
        
        
    
    