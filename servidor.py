import socket
import select
import threading

HOST = "0.0.0.0"  # Escuchar en todas las interfaces de red
PORT = 12345      # Puerto donde se aceptan conexiones

# Crear el socket del servidor (TCP/IPv4)
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # reutilizar dirección rápidamente
servidor.bind((HOST, PORT))
servidor.listen()  # empezar a escuchar conexiones entrantes
print(f"Servidor escuchando en {HOST}:{PORT}")

# Lista que contiene el socket del servidor y todos los sockets cliente conectados
# Se usa con select.select() para saber cuáles sockets tienen datos listos para leer
conexiones_activas = [servidor]

# Bandera que controla el bucle principal: mientras True, el servidor acepta/gestiona conexiones
ejecutando = True

# Mapa: socket_cliente -> (ip, puerto)
# Se usa para saber la dirección (origen) de los mensajes cuando llegan
direcciones_clientes = {}


# ----------------------------
# HILO: escuchar comandos desde la consola
# ----------------------------
def escuchar_consola():
    """Hilo que permite introducir comandos desde la consola local.

    Actualmente soporta el comando "salir" para detener el servidor de forma ordenada.
    Este hilo evita bloquear el bucle principal y permite cerrar el servidor desde la terminal.
    """
    global ejecutando
    while ejecutando:
        comando = input()
        if comando.strip().lower() == "salir":
            # Señalar al bucle principal que debe detenerse
            ejecutando = False
            print("Cayo el servidorr...")
            try:
                # Cerrar el socket del servidor para forzar que select/accept fallen y salir
                servidor.close()
            except:
                pass


# Lanzar el hilo de consola 
threading.Thread(target=escuchar_consola, daemon=True).start()



while ejecutando:
    try:
        # select.select(lista_lectura, lista_escritura, lista_excepciones, timeout)
        # Devuelve los sockets listos para lectura en sockets_para_lectura
        sockets_para_lectura, _, _ = select.select(conexiones_activas, [], [], 1)
    except (OSError, ValueError):
        # Si el socket del servidor se cerró o la lista es inválida, salimos del bucle
        break

    # Procesar cada socket listo para lectura
    for socket_actual in sockets_para_lectura:
        # Si el socket listo es el socket del servidor, significa que hay una nueva conexión entrante
        if socket_actual == servidor:
            try:
                # Aceptar la conexión entrante 
                socket_cliente, direccion_cliente = servidor.accept()

                # Añadir el socket cliente a la lista de conexiones activas para ser monitorizado por select
                conexiones_activas.append(socket_cliente)

                # Guardar la dirección para poder identificar mensajes de este cliente
                direcciones_clientes[socket_cliente] = direccion_cliente

                # Informar en consola que se conectó un cliente
                print(f"Cliente conectado: {direccion_cliente}")
            except OSError:
                # Si ocurre un OSError durante accept  detener el servidor
                ejecutando = False
        else:
            # Si el socket listo no es el servidor, es un socket cliente con datos para leer
            try:
                # Leer hasta 1024 bytes del socket cliente
                mensaje = socket_actual.recv(1024)
                if not mensaje:
                    # Eliminar la dirección guardada y mostrar que el cliente se desconectó
                    direccion_cliente_desconectado = direcciones_clientes.pop(socket_actual, None)
                    print(f"Cliente desconectado:    {direccion_cliente_desconectado}")

                    
                    try:
                        conexiones_activas.remove(socket_actual) #remover de la lista de conexiones activas
                    except ValueError:
                        pass
                    try:
                        socket_actual.close()
                    except:
                        pass
                   
                    continue

                # Intentar decodificar los bytes a texto (UTF-8). Si falla, mostramos la representación de bytes
                try:
                    texto = mensaje.decode().strip()
                except Exception:
                    texto = repr(mensaje)

                # Obtener la dirección  del socket que envió el mensaje
                direccion_origen = direcciones_clientes.get(socket_actual)
                # Mostrar en consola quién envió qué mensaje
                print(f"[{direccion_origen}] {texto}")

                # Reenviar el mensaje a todos los demás clientes conectados
                for socket_destino in conexiones_activas:
                    # Omitir el socket del servidor y el socket que envió el mensaje
                    if socket_destino != servidor and socket_destino != socket_actual:
                        try:
                            socket_destino.send(mensaje)
                        except:
                            # Si el envío falla , limpiarlo:
                            try:
                                conexiones_activas.remove(socket_destino)
                            except ValueError:
                                pass
                            try:
                                direcciones_clientes.pop(socket_destino, None)
                            except:
                                pass
                            try:
                                socket_destino.close()
                            except:
                                pass
            except:
                # En caso de cualquier excepción al leer de socket_actual, limpiar la conexión
                try:
                    conexiones_activas.remove(socket_actual)
                except ValueError:
                    pass
                direcciones_clientes.pop(socket_actual, None)
                try:
                    socket_actual.close()
                except:
                    pass


print("Servidor cerrado.")


