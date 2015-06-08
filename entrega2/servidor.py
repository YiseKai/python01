import socket
import sys
# -*- coding: utf-8 -*-


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line
server_name = sys.argv[1]


server_address = (server_name, 10000)
print >>sys.stderr, 'conectado en %s port %s' % server_address
sock.bind(server_address)
sock.listen(1)

while True:
    print >>sys.stderr, 'Esperando conexion'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'Cliente conectado:', client_address
        while True:
            data = connection.recv(4096)
            print >>sys.stderr, 'recibido "%s"' % data
            if(data.isdigit()):
                print 'Ha llegado un digito'
                connection.sendall("OK")
                buffer = 0
                with open("a.txt", "w") as archivo:
                	while(buffer <= int(data)):
                		print buffer
                		byte = connection.recv(1)
                		print 'He recibido' ,byte
                		if not len(byte):
                			break
                		archivo.write(byte)
                		print 'Se ha escrito'
                		buffer += 1
                	if(buffer == len(data)):
                		print 'Archivo recibido con exito'
                	else:
                		print 'Fin'
            break
    finally:
        connection.close()

