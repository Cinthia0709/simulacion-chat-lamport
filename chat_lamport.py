import threading
import time
import random
from queue import Queue

class Nodo(threading.Thread):
    def __init__(self, id_nodo, red):
        super().__init__()
        self.id_nodo = id_nodo
        self.red = red  # Referencia al gestor de red
        self.reloj = 0
        self.buzon = Queue()
        self.activo = True

    def evento_interno(self, descripcion):
        self.reloj += 1
        print(f"[{time.strftime('%H:%M:%S')}] [Nodo {self.id_nodo}] EVENTO INTERNO ('{descripcion}'). Reloj local: {self.reloj}")

    def enviar_mensaje(self, id_destino, texto):
        self.reloj += 1
        mensaje = {
            'emisor': self.id_nodo,
            'texto': texto,
            'reloj_emisor': self.reloj
        }
        print(f"[{time.strftime('%H:%M:%S')}] [Nodo {self.id_nodo}] ENVIANDO a Nodo {id_destino}: '{texto}' (Reloj enviado: {self.reloj})")
        # Se envía a través de la red simulada
        self.red.enviar_con_retardo(id_destino, mensaje)

    def recibir_mensaje(self, mensaje):
        reloj_recibido = mensaje['reloj_emisor']
        emisor = mensaje['emisor']
        texto = mensaje['texto']
        
        # Regla de Lamport para recepción
        self.reloj = max(self.reloj, reloj_recibido) + 1
        print(f"[{time.strftime('%H:%M:%S')}] [Nodo {self.id_nodo}] RECIBIDO de Nodo {emisor}: '{texto}'. (Reloj recibido: {reloj_recibido} -> Nuevo Reloj local: {self.reloj})")

    def run(self):
        while self.activo:
            if not self.buzon.empty():
                mensaje = self.buzon.get()
                self.recibir_mensaje(mensaje)
            time.sleep(0.1)


class RedSimulada:
    def __init__(self):
        self.nodos = {}

    def registrar_nodo(self, nodo):
        self.nodos[nodo.id_nodo] = nodo

    def enviar_con_retardo(self, id_destino, mensaje):
        # Hilo separado para simular la latencia de red aleatoria
        def entregar():
            retardo = random.uniform(1.0, 4.0)  # Retardo aleatorio entre 1 y 4 segundos
            time.sleep(retardo)
            if id_destino in self.nodos:
                self.nodos[id_destino].buzon.put(mensaje)

        threading.Thread(target=entregar, daemon=True).start()


# --- SIMULACIÓN Y PRUEBA ---
if __name__ == "__main__":
    red = RedSimulada()
    N = 3  # Cantidad de nodos

    # Crear e iniciar N nodos
    nodos = [Nodo(i, red) for i in range(N)]
    for n in nodos:
        red.registrar_nodo(n)
        n.start()

    time.sleep(1)

    # Escenario de prueba para forzar desorden
    nodos[0].evento_interno("Escribiendo borrador")
    nodos[0].enviar_mensaje(id_destino=1, texto="Hola Nodo 1 (Mensaje A)")
    
    # Nodo 0 envía un segundo mensaje muy rápido
    nodos[0].enviar_mensaje(id_destino=1, texto="¿Recibiste el anterior? (Mensaje B)")

    # Evento interno en otro nodo
    nodos[2].evento_interno("Procesando datos")
    nodos[2].enviar_mensaje(id_destino=1, texto="Saludos desde Nodo 2")

    # Esperar a que la red entregue los mensajes con retardo
    time.sleep(6)

    # Detener nodos
    for n in nodos:
        n.activo = False
