Chat Cliente–Servidor con Reconexión Automática

Descripción

Este proyecto implementa un sistema de comunicación en red basado en arquitectura cliente-servidor usando sockets TCP en Python.

Permite que múltiples clientes se conecten a un servidor y se comuniquen entre sí en tiempo real.

El sistema incluye:

Manejo de múltiples conexiones simultáneas

Reconexión automática del cliente si el servidor cae

Difusión de mensajes entre clientes

Control del servidor desde consola

Funcionamiento General

El sistema se divide en dos componentes:

* Servidor

Escucha conexiones entrantes

Gestiona múltiples clientes simultáneamente

Recibe mensajes y los retransmite al resto

Detecta desconexiones automáticamente

Puede cerrarse desde consola escribiendo:

salir

* Cliente

Se conecta al servidor

Permite enviar mensajes

Escucha mensajes en paralelo

Si el servidor se cae:

✔ Detecta la caída
✔ Intenta reconectarse automáticamente
✔ Retoma la comunicación sin reiniciar el programa

Características Técnicas :

Concurrencia

El sistema utiliza hilos (threading) para permitir:

Recepción de mensajes sin bloquear el envío

Reconexión automática sin detener el programa

Control del servidor desde consola

Multiplexación

El servidor usa:

select.select()


Esto permite:

Gestionar múltiples clientes sin crear un hilo por conexión

Escuchar actividad en todos los sockets simultáneamente

Mejor eficiencia en el manejo de conexiones

Comunicación

Se utiliza:

TCP (SOCK_STREAM)

IPv4 (AF_INET)

Cada cliente:

Envía mensajes al servidor

El servidor los reenvía a todos los demás clientes conectados

Flujo del Sistema

El servidor inicia y comienza a escuchar conexiones.

Los clientes se conectan.

Cuando un cliente envía un mensaje:

El servidor lo recibe

Identifica su origen

Lo reenvía a los demás clientes

Si un cliente se desconecta:

El servidor limpia la conexión

Si el servidor cae:

Los clientes intentan reconectarse automáticamente

Reconexión Automática

El cliente incluye un sistema de tolerancia a fallos:

Si la conexión se pierde:

Detecta la desconexión

Intenta reconectar cada 3 segundos

Actualiza la conexión sin detener el programa

Esto permite continuar la comunicación sin reiniciar el cliente.

* Ejecución

1. Iniciar el servidor
python servidor.py


Mostrará:

Servidor escuchando en 0.0.0.0:12345

2. Iniciar uno o más clientes
python cliente.py


Cada cliente podrá enviar mensajes desde consola.

3. Salir

En cliente:

salir


En servidor:

salir

* Conceptos Aplicados

Programación en red

Sockets TCP

Multiplexación con select

Concurrencia con hilos

Manejo de fallos

Reconexión automática

Arquitectura cliente-servidor

* Objetivo Académico

Simular un sistema de mensajería distribuido que:

Maneje múltiples usuarios

Sea tolerante a fallos

Permita comunicación en tiempo real

Sirviendo como introducción práctica a

Sistemas distribuidos

Redes

Concurrencia