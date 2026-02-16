import select
import socket

host = "127.0.0.1"
port = 5000
servidor = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
servidor.bind((host, port))
servidor.listen()

Sockets_Activos = []

Sockets_Activos.append(servidor)


while True:
    Sockets_lectura , _ , Sockets_errores = select.select(Sockets_Activos , [] , Sockets_Activos , 1)
    for Sockets in Sockets_lectura:
       if Sockets == servidor:
            Socket_Cliente , direccion = servidor.accept()
            Sockets_Activos.append(Socket_Cliente)
       else :
           mensaje = Sockets.recv(1024)
           if mensaje == None:
               print ("se desconecto el cliente ")
               Sockets_Activos.remove(Sockets)
               Sockets.close()
           else:
               Sockets.send(mensaje.decode)
               respuesta = "aceptado".encode()
               Sockets.send(respuesta)

    for Sockets in Sockets_errores:
        Sockets_Activos.remove(Sockets)
        Sockets.close()



               