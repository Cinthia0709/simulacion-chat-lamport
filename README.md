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

1. Clonar este repositorio:
   ```bash
   git clone [https://github.com/TU_USUARIO/simulacion-chat-lamport.git](https://github.com/TU_USUARIO/simulacion-chat-lamport.git)
   cd simulacion-chat-lamport
