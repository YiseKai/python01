import socket
import sys
# -*- coding: utf-8 -*-

def enviar_archivo(dato, server_name):
    # Creamos una conexión socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Nos conectamos con el socket en cuestión
    server_address = (server_name, 10000)
    print >>sys.stderr, 'connecting to %s port %s' % server_address
    sock.connect(server_address)

    with open(dato, "r") as archivo:
            buffer = archivo.read()
    print 'Enviando el archivo'
    print str(len(buffer))
    try:
        sock.sendall(str(len(buffer)))
        recibido = sock.recv(10)
        if(recibido == "OK"):
        	print 'Ok recibido'
        	for byte in buffer:
        		print 'Enviando' ,byte
        		sock.sendall(byte)
        	print 'Enviado con exito'

    finally:
        sock.close()
finally:
    sock.close()
