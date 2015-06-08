import argparse
import os
from threading import Thread
import socket
from netifaces import interfaces, ifaddresses, AF_INET # dependency, not in stdlib
import cliente
import zmq

#Metodo que se encarga de la escucha continua del cliente en el chat
#Se ejecuta mediante un hilo de la clase Thread
def listen(masked):
    ctx = zmq.Context.instance()
    listener = ctx.socket(zmq.SUB)
    #Le llega una variable con una ip de tres parámetros fijo, que será la red nuestra: X.Y.Z
    #Este for, le asigna la cuarta dirección al usuario -> M
    #Formando así la dirección X.Y.Z.M
    for last in range(1, 255):
        listener.connect("tcp://{0}.{1}:9000".format(masked, last))
    
    listener.setsockopt(zmq.SUBSCRIBE, b'')
    #Metodo vivo que escucha continuamente
    while True:
        try:
            print(listener.recv_string())
        except (KeyboardInterrupt, zmq.ContextTerminated):
            break

def main():
    #Lineas para añadir los argumentos de la llamada a la funcion
    parser = argparse.ArgumentParser()
    parser.add_argument("interface", type=str, help="the network interface",
        choices=interfaces(),
    )
    parser.add_argument("user", type=str, default=os.environ['USER'],
        nargs='?',
        help="Your username",
    )
    args = parser.parse_args()
    inet = ifaddresses(args.interface)[AF_INET]
    addr = inet[0]['addr']
    masked = addr.rsplit('.', 1)[0]
    
    ctx = zmq.Context.instance()
    #Lanzamiento del hilo de escucha
    listen_thread = Thread(target=listen, args=(masked,))
    listen_thread.start()
    
    bcast = ctx.socket(zmq.PUB)
    bcast.bind("tcp://%s:9000" % args.interface)
    print("Conectando a %s:9000 (%s.*)" % (args.interface, masked))
    #Mostramos la IP nuestra actual en el servicio para poder interectuar con el otro usuario
    print "Tu IP es: ",addr
    while True:
        try:
            msg = raw_input()
            bcast.send_string("%s: %s" % (args.user, msg))
            if(msg == '#'):
                print 'Introduce el nombre del archivo'
                nombre_o = raw_input()
                print 'Introduce la IP de destino'
                direccion_e = raw_input()
                #Enviamos el archivo en cuestion haciendo uso de la clase cliente
                cliente.enviar_archivo(nombre_o,direccion_e)
            
        except KeyboardInterrupt:
            break
    bcast.close(linger=0)
    ctx.term()

if __name__ == '__main__':
    main()
