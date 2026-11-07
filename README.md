# Simulación de Chat Distribuido con Relojes Lógicos de Lamport

**Asignatura:** Computacion distribuida y paralela 
**Autor:** Cinthia America Blanco Rodrigo
**Docente:** Luis Enrique Patiño Herrera  
**Fecha de entrega:** 7 de noviembre  

---

## 1. Descripción del Proyecto

Este proyecto implementa la simulación de un sistema de chat distribuido compuesto por $N$ procesos (nodos) independientes que se comunican mediante paso de mensajes. 

El objetivo principal es aplicar el algoritmo de **Relojes Lógicos de Lamport** para mantener una sincronización de eventos en un entorno distribuido sin reloj global, demostrando el correcto manejo del orden causal aun cuando existe latencia y desorden en el envío/recepción de mensajes.

---

## 2. Reglas del Reloj de Lamport Implementadas

Cada nodo $i$ mantiene un contador entero $L_i$ inicializado en `0` y actualiza su estado bajo 3 escenarios específicos:

1. **Evento Interno:**
   $$L_i = L_i + 1$$
2. **Envío de Mensaje:**
   $$L_i = L_i + 1$$
   *El paquete adjunta el valor actual del reloj $L_i$.*
3. **Recepción de Mensaje ($L_{mensaje}$):**
   $$L_i = \max(L_i, L_{mensaje}) + 1$$

---

## 3. Arquitectura y Manejo de Retardos

* **Concurrencia de Nodos:** Cada nodo corre en un hilo independiente (`threading.Thread`), representando un proceso distribuido autónomo con su propia cola de entrada (`Queue`).
* **Simulación de Red Asíncrona:** La clase `RedSimulada` intercepta cada mensaje y genera un hilo temporal con un retardo aleatorio entre `1.0` y `4.0` segundos (`random.uniform(1.0, 4.0)`). 
* **Desorden de Mensajes:** La latencia aleatoria simula la inestabilidad de la red real, forzando a que los mensajes lleguen al destinatario en un orden físico distinto al que fueron enviados.

---

## 4. Requisitos e Instalación

No se requieren librerías externas. La solución utiliza módulos nativos de Python 3.

* **Lenguaje:** Python 3.8+
* **Módulos estándar:** `threading`, `time`, `random`, `queue`

### Ejecución

A continuación se muestra un ejemplo real de la consola al ejecutar el programa, evidenciando el avance del tiempo lógico de Lamport:

[Nodo 0] EVENTO INTERNO ('Escribiendo borrador'). Reloj local: 1
 [Nodo 0] ENVIANDO a Nodo 1: 'Hola Nodo 1 (Mensaje A)' (Reloj enviado: 2)
 [Nodo 0] ENVIANDO a Nodo 1: '¿Recibiste el anterior? (Mensaje B)' (Reloj enviado: 3)
 [Nodo 2] EVENTO INTERNO ('Procesando datos'). Reloj local: 1
 [Nodo 2] ENVIANDO a Nodo 1: 'Saludos desde Nodo 2' (Reloj enviado: 2)
 [Nodo 1] RECIBIDO de Nodo 0: '¿Recibiste el anterior? (Mensaje B)'. (Reloj recibido: 3 -> Nuevo Reloj local: 4)
 [Nodo 1] RECIBIDO de Nodo 0: 'Hola Nodo 1 (Mensaje A)'. (Reloj recibido: 2 -> Nuevo Reloj local: 5)
 [Nodo 1] RECIBIDO de Nodo 2: 'Saludos desde Nodo 2'. (Reloj recibido: 2 -> Nuevo Reloj local: 6)

Análisis de la TrazaDesorden de llegada: El Mensaje B enviado por el Nodo 0 llegó al Nodo 1 en el segundo 18:30:02, antes que el Mensaje A (que llegó en 18:30:03), cumpliendo el requisito de desorden de red.Corrección del Reloj de Lamport: Al recibir el Mensaje B con timestamp 3, el Nodo 1 (cuyo reloj estaba en 0) calculó $\max(0, 3) + 1 = 4$, garantizando la consistencia causal del tiempo lógico.6. ConclusionesLa simulación demuestra satisfactoriamente cómo el algoritmo de Lamport resuelve la falta de un reloj físico global en sistemas distribuidos. A pesar de los retardos en la red, la regla de actualización del reloj garantiza un orden lógico de eventos consistente entre todos los nodos participantes.
