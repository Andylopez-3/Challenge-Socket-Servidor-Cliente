import socket, threading, time

HOST = "127.0.0.1"
PORT = 12345

def recibir(conexion):
    while True:
        try:
            datos = conexion.recv(1024)
            if not datos:
                print("Servidor desconectado.")
                break
            print(datos.decode().strip())
        except:
            break

def enviar(conexion):
    while True:
        try:
            mensaje = input()
            if mensaje.strip().lower() == "salir":
                print("Desconectando...")
                conexion.close()
                return False
            conexion.send(mensaje.encode())
        except:
            return True  # Señal de que se perdió la conexión

def conectar():
    while True:
        try:
            conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conexion.connect((HOST, PORT))
            print("Conectado al servidor. Escribí mensajes y presioná Enter.")
            return conexion
        except:
            print("No se pudo conectar al servidor. Reintentando en 3 segundos...")
            time.sleep(3)

def main():
    while True:
        conexion = conectar()

        t1 = threading.Thread(target=recibir, args=(conexion,))
        t1.daemon = True
        t1.start()

        # si enviar() devuelve True, fue desconexión forzada → reintentar
        if enviar(conexion):
            print("Conexión perdida. Intentando reconectar...")
            time.sleep(3)
            continue
        else:
            break

if __name__ == "__main__":
    main()


