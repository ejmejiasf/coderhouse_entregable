import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_correo(**context):
    # Obtener detalles del correo desde el contexto
    configuraciones = context["var"]["value"]
    asunto = configuraciones.get("subject_mail", "Sin Asunto")
    remitente = configuraciones.get("email")
    contrasena = configuraciones.get("email_password")
    destinatario = configuraciones.get("to_address")

    # Crear el mensaje del correo
    mensaje = MIMEMultipart()
    mensaje['From'] = remitente
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    # Contenido HTML del correo
    contenido_html = """
    <html>
        <body>
            <h2>¡Hola!</h2>
            <p>El proceso de ETL se completó exitosamente.</p>
            <p>Los datos han sido cargados correctamente.</p>
        </body>
    </html>
    """
    
    # Adjuntar contenido HTML al mensaje
    mensaje.attach(MIMEText(contenido_html, 'html'))

    try:
        # Configurar servidor SMTP y enviar el correo
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()  # Activar seguridad TLS
            servidor.login(remitente, contrasena)  # Iniciar sesión

            # Enviar el correo electrónico
            servidor.sendmail(remitente, destinatario, mensaje.as_string())
            print("Correo enviado exitosamente")
    except Exception as error:
        print(f"Error al enviar el correo: {error}")
