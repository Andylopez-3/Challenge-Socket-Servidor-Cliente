
import socket      # Para crear y manejar sockets 
import threading   # Para ejecutar funciones en hilos paralelos 
import time        # Para pausar la ejecución (esperas entre reintentos)

HOST = "127.0.0.1"  # Dirección IP del servidor (localhost)
PORT = 12345        # Puerto del servidor (número de identificación del servicio)
ESPERA = 3          # Segundos entre intentos de conexión si falla

def conectar():
    # Función para conectarse al servidor con reintentos automáticos
    
    while True:
        try:
            conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # AF_INET: usar protocolo IPv4
            # SOCK_STREAM: usar TCP 
            
            # Intentar conectarse al servidor en HOST:PORT
            conexion.connect((HOST, PORT))
            
            print("Conectado al servidor. Escribí mensajes y presioná Enter.")
            return conexion
        except:
            # Si falla la conexión 
            print(f"No se pudo conectar. Reintentando en {ESPERA} segundos...")
            time.sleep(ESPERA)

def recibir(conexion_compartida):
    # Función que se ejecuta en un hilo separado para recibir mensajes del servidor
    # Usa conexion_compartida (lista con 1 elemento) para permitir que otro hilo actualice la conexión
    while True:
        # Obtener el socket actual de la referencia compartida
        conexion = conexion_compartida[0]
        try:
            # Recibir hasta 1024 bytes del servidor
            mensaje_recibido = conexion.recv(1024)
            
            # Si no hay datos (servidor desconectado), lanzar una excepción
            if not mensaje_recibido:
                raise ConnectionError       # busca detener el programa y avisar que la conexion falla
                                            # interrumpe el codigo y salta al except
            # Decodificar los bytes a texto (UTF-8) y mostrar en pantalla
            print(mensaje_recibido.decode().strip())
        except:
            # Si falla la recepción 
            print("Servidor desconectado. Intentando reconexión...")
            
            # Bucle infinito para reconectar
            while True:
                # Intentar conectarse nuevamente al servidor
                nueva_conexion = conectar()
                if nueva_conexion:
                    # Esto permite que el hilo de envío use la nueva conexión
                    conexion_compartida[0] = nueva_conexion  # actualizar la conexion en la lista compartida
                    
                    # Lanzar un nuevo hilo para recibir con la nueva conexión
                    # daemon=True: el hilo se cierra automáticamente cuando el programa principal termina
                    threading.Thread(target=recibir, args=(conexion_compartida,), daemon=True).start()
                    
                    
                    return
                else:
                    print("Esperando servidor...")
                    time.sleep(ESPERA)

def enviar(conexion_compartida):
    # Función para enviar mensajes al servidor
    # Se ejecuta en el hilo principal (bloquea hasta que se escribe "salir")
    while True:
        mensaje = input()
        
        # Verificar si el usuario quiere salir
        if mensaje.strip().lower() == "salir":
            print("Desconectando...")
            try:
                # Cerrar la conexión con el servidor
                conexion_compartida[0].close()
            except:
                # Si hay error al cerrar, ignorarlo
                pass
            break
        
        try:
            # Codificar el mensaje de texto a bytes (UTF-8) y enviarlo al servidor
            conexion_compartida[0].send(mensaje.encode())
        except:
            # Si falla el envío
            print("No se pudo enviar mensaje. Esperando reconexión...")
            # Esperar antes de reintentar
            time.sleep(ESPERA)

def main():
    
    
    # Conectarse al servidor 
    conexion = conectar()
    if not conexion:
        # Si no se puede conectar, salir del programa
        return
    
    # Crear una lista con la conexión para compartirla entre hilos
    # Se usa una lista para permitir que un hilo actualice la conexión (en caso de reconexión)
    # Si usáramos una variable simple, los cambios en el hilo no afectarían al otro hilo
    # es como esta es la conexion que hay con el servidor , y para a la hora de reconectar todos sepan cual es la conexion actual 
    conexion_compartida = [conexion]
    
    # Lanzar un hilo separado que ejecute la función recibir()
    # Este hilo recibirá mensajes del servidor de forma continua
    # daemon=True: el hilo se cerrará automáticamente cuando el programa termine
    threading.Thread(target=recibir, args=(conexion_compartida,), daemon=True).start()
    
    # Ejecutar la función enviar() en el hilo principal
    # Esta función lee mensajes del usuario y los envía al servidor
    # Bloquea el programa hasta que el usuario escriba "salir"
    enviar(conexion_compartida)

if __name__ == "__main__":
    main()
