"""Parte B — Cola de prioridad de 3 niveles, con reserva de turnos.

Nada de `heapq` (`constitucion.md` §2): se construye sobre tres `Cola`
simples de la Parte A (`cola.py`), una por nivel.

## El problema que resuelve el patrón de turnos

Una prioridad estricta (atender siempre al nivel más urgente disponible) deja
sin cota de espera a los niveles bajos: si llegan solicitudes de nivel 1 y 2
sin parar, una de nivel 3 puede quedar esperando indefinidamente. Eso es lo
que mide `simulacion.py` comparando esta clase contra una versión estricta.

## El mecanismo: reserva de turnos

`PATRON_TURNOS` es un ciclo fijo de niveles «reservados». En cada atención se
mira la posición actual del ciclo:

- Si el nivel reservado en esa posición tiene a alguien esperando, se le
  atiende **aunque haya niveles más urgentes esperando también**.
- Si no tiene a nadie, se atiende por prioridad estricta entre los niveles
  que sí tienen gente esperando.
- El índice del patrón avanza siempre, haya tenido o no a quien atender en
  esa posición — si no avanzara solo cuando encuentra gente, un nivel vacío
  en el momento exacto de su turno alargaría el ciclo y la cota dejaría de
  cumplirse.

Con `PATRON_TURNOS = (1, 1, 2, 1, 1, 2, 3)` (7 posiciones, una reservada para
el nivel 3), la cota es demostrable **sin reloj, contando atenciones**: en
cualquier ventana de 7 atenciones consecutivas hay exactamente una posición
reservada para el nivel 3. Mientras el nivel 3 tenga a alguien esperando, el
**hueco entre dos atenciones consecutivas de nivel 3** nunca supera
`len(PATRON_TURNOS) - 1 = 6` atenciones de otros niveles — sin importar
cuántas solicitudes de nivel 1 o 2 sigan llegando mientras tanto. Esa es la
garantía real: nivel 3 nunca deja de avanzar, al menos 1 de cada 7
atenciones es suya si tiene demanda.

Lo que esto **no** garantiza es que cada solicitud de nivel 3 espere como
máximo 6 atenciones desde que llega: si ya hay otras solicitudes de nivel 3
delante en su propia fila (que es FIFO, como cualquier otro nivel), primero
tienen que salir ellas. El límite de 6 aplica al hueco entre servicios
consecutivos de nivel 3, no al tiempo de cada solicitud si hay cola interna
acumulada en ese nivel. `test_cola_prioridad.py` demuestra ambas cosas: el
hueco acotado con una ráfaga sostenida, y que ninguna solicitud de nivel 3
se queda sin salir nunca aunque haya varias esperando a la vez.

Se prefirió este mecanismo sobre «envejecimiento» (subir el nivel de una
solicitud según cuánto lleva esperando) porque el envejecimiento necesita un
reloj y un umbral arbitrario de cuándo promover, mientras que la reserva de
turnos da una cota exacta y verificable solo con un contador (`spec.md` §3).
"""

from dataclasses import dataclass

from cola import Cola, ColaVaciaError

NIVELES_VALIDOS = (1, 2, 3)
PATRON_TURNOS = (1, 1, 2, 1, 1, 2, 3)


@dataclass
class Solicitud:
    dato: object
    nivel: int
    orden_llegada: int


class ColaPrioridad:
    """Cola de 3 niveles con reserva de turnos (ver docstring del módulo)."""

    def __init__(self):
        self._colas = {nivel: Cola() for nivel in NIVELES_VALIDOS}
        self._indice_patron = 0
        self._siguiente_orden = 0

    def __len__(self):
        return sum(len(c) for c in self._colas.values())

    def esta_vacia(self) -> bool:
        return len(self) == 0

    def cuantos_hay(self) -> dict:
        return {nivel: len(cola) for nivel, cola in self._colas.items()}

    def encolar(self, dato, nivel: int) -> Solicitud:
        if nivel not in NIVELES_VALIDOS:
            raise ValueError(f"nivel inválido: {nivel!r} (debe ser 1, 2 o 3)")
        solicitud = Solicitud(dato=dato, nivel=nivel, orden_llegada=self._siguiente_orden)
        self._siguiente_orden += 1
        self._colas[nivel].encolar(solicitud)
        return solicitud

    def decolar(self) -> Solicitud:
        if self.esta_vacia():
            raise ColaVaciaError("la cola de prioridad está vacía")

        nivel_reservado = PATRON_TURNOS[self._indice_patron]
        self._indice_patron = (self._indice_patron + 1) % len(PATRON_TURNOS)

        if not self._colas[nivel_reservado].esta_vacia():
            elegido = nivel_reservado
        else:
            elegido = next(n for n in NIVELES_VALIDOS if not self._colas[n].esta_vacia())

        return self._colas[elegido].decolar()
