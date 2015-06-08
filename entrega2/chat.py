import argparse
import os
from threading import Thread
import socket
from netifaces import interfaces, ifaddresses, AF_INET # dependency, not in stdlib

import cliente
import zmq

def listen(masked):
    ctx = zmq.Context.instance()
    listener = ctx.socket(zmq.SUB)
    for last in range(1, 255):
        listener.connect("tcp://{0}.{1}:9000".format(masked, last))
    
    listener.setsockopt(zmq.SUBSCRIBE, b'')
    while True:
        try:
            print(listener.recv_string())
        except (KeyboardInterrupt, zmq.ContextTerminated):
            break

def main():
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
    
    listen_thread = Thread(target=listen, args=(masked,))
    listen_thread.start()
    
    bcast = ctx.socket(zmq.PUB)
    bcast.bind("tcp://%s:9000" % args.interface)
    print("Conectando a %s:9000 (%s.*)" % (args.interface, masked))
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
                #print 'Introduce el nombre del archivo a guardar'
                #nombre_d = raw_input()
                #intercambio(nombre_o,direccion_e,nombre_d,addr)
                cliente.enviar_archivo(nombre_o,direccion_e)
            
        except KeyboardInterrupt:
            break
    bcast.close(linger=0)
    ctx.term()

if __name__ == '__main__':
    main()