"""Parte B — Simulación: ¿sirve de algo la reserva de turnos?

Compara dos estrategias de atención con la **misma** secuencia de llegadas:

- `ColaPrioridadEstricta` (definida aquí, solo para esta comparación): siempre
  atiende al nivel más urgente disponible. Es el punto de control: así se
  comportaría la sala sin ningún mecanismo contra la espera indefinida.
- `ColaPrioridad` (`cola_prioridad.py`): la cola real del proyecto, con
  reserva de turnos.

Escenario: 500 instantes. En cada uno, cada nivel tiene una probabilidad
independiente de que llegue una solicitud (nivel 1: 0.35, nivel 2: 0.30,
nivel 3: 0.20). Entre los instantes 150 y 250 hay una **racha**: la
probabilidad del nivel 1 sube a 0.65, como una semana de evaluaciones. En
cada instante se atiende como máximo una solicitud (si hay alguna pendiente).

Ejecutar:  python simulacion.py
"""

import random
import statistics

from cola import Cola, ColaVaciaError
from cola_prioridad import ColaPrioridad, NIVELES_VALIDOS

INSTANTES = 500
RACHA_INICIO, RACHA_FIN = 150, 250
PROB_BASE = {1: 0.35, 2: 0.30, 3: 0.20}
PROB_RACHA = {1: 0.65, 2: 0.30, 3: 0.20}
SEMILLA = 706132


class ColaPrioridadEstricta:
    """Punto de control: atiende siempre al nivel más urgente disponible,
    sin ningún mecanismo contra la espera indefinida. No es un entregable de
    `cola_prioridad.py`: existe solo para que la comparación tenga con qué
    compararse (`plan.md` §4).
    """

    def __init__(self):
        self._colas = {nivel: Cola() for nivel in NIVELES_VALIDOS}

    def esta_vacia(self) -> bool:
        return all(c.esta_vacia() for c in self._colas.values())

    def encolar(self, dato, nivel: int):
        self._colas[nivel].encolar(dato)

    def decolar(self):
        for nivel in NIVELES_VALIDOS:
            if not self._colas[nivel].esta_vacia():
                return self._colas[nivel].decolar()
        raise ColaVaciaError("la cola está vacía")


def generar_llegadas(rng):
    """Una lista de longitud INSTANTES; cada posición es la lista de niveles
    que llegaron en ese instante (puede ser vacía, uno, o varios a la vez).
    """
    llegadas = []
    for t in range(INSTANTES):
        prob = PROB_RACHA if RACHA_INICIO <= t < RACHA_FIN else PROB_BASE
        del t
        llegadas.append([nivel for nivel in NIVELES_VALIDOS if rng.random() < prob[nivel]])
    return llegadas


def simular(cola, llegadas):
    """Corre `llegadas` contra `cola` y devuelve, por nivel, la lista de
    esperas (instante_atendido - instante_llegada) de cada solicitud.
    """
    esperas = {1: [], 2: [], 3: []}
    for t, niveles_que_llegan in enumerate(llegadas):
        for nivel in niveles_que_llegan:
            cola.encolar({"nivel": nivel, "llegada": t}, nivel)
        if not cola.esta_vacia():
            atendido = cola.decolar()
            # ColaPrioridad.decolar() devuelve una Solicitud (dato + nivel +
            # orden); ColaPrioridadEstricta devuelve el dato tal cual.
            dato = atendido.dato if hasattr(atendido, "dato") else atendido
            esperas[dato["nivel"]].append(t - dato["llegada"])
    return esperas


def resumen(esperas_por_nivel: dict) -> dict:
    resumen_ = {}
    for nivel, lista in esperas_por_nivel.items():
        if lista:
            resumen_[nivel] = {"media": statistics.mean(lista), "peor": max(lista), "n": len(lista)}
        else:
            resumen_[nivel] = {"media": 0.0, "peor": 0, "n": 0}
    return resumen_


def main():
    rng = random.Random(SEMILLA)
    llegadas = generar_llegadas(rng)

    esperas_estricta = simular(ColaPrioridadEstricta(), llegadas)
    esperas_con_reserva = simular(ColaPrioridad(), llegadas)

    r_estricta = resumen(esperas_estricta)
    r_reserva = resumen(esperas_con_reserva)

    print(f"Simulación de {INSTANTES} instantes, racha de nivel 1 entre "
          f"{RACHA_INICIO} y {RACHA_FIN}. Semilla fija ({SEMILLA}).\n")
    print("| Nivel | n atendidos | Media espera (estricta) | Peor espera (estricta) "
          "| Media espera (con reserva) | Peor espera (con reserva) |")
    print("|---|---|---|---|---|---|")
    for nivel in NIVELES_VALIDOS:
        e, c = r_estricta[nivel], r_reserva[nivel]
        print(f"| {nivel} | {e['n']} | {e['media']:.2f} | {e['peor']} "
              f"| {c['media']:.2f} | {c['peor']} |")

    print("\nAnálisis:")
    peor_estricta_3 = r_estricta[3]["peor"]
    peor_reserva_3 = r_reserva[3]["peor"]
    print(f"- Nivel 3, peor caso: {peor_estricta_3} instantes sin reserva de turnos "
          f"vs. {peor_reserva_3} con reserva.")
    if peor_estricta_3 > peor_reserva_3:
        print(f"  La reserva de turnos reduce el peor caso de nivel 3 en "
              f"{peor_estricta_3 - peor_reserva_3} instantes: durante la racha de nivel 1, "
              f"la cola estricta deja crecer su espera sin control; la cola con reserva la "
              f"mantiene acotada por el patrón, como predice spec.md §3.")
    else:
        print("  (no se observó la diferencia esperada; revisar la semilla o la duración de la racha)")

    costo_1 = r_reserva[1]["peor"] - r_estricta[1]["peor"]
    costo_2 = r_reserva[2]["peor"] - r_estricta[2]["peor"]
    print(f"- La reserva de turnos no es gratis: el peor caso de nivel 1 empeora en "
          f"{costo_1} instantes y el de nivel 2 en {costo_2}, porque ceder turnos reservados "
          f"a nivel 3 retrasa a los niveles más urgentes mientras la cola de nivel 3 tiene "
          f"demanda. Es el costo esperado de garantizar que nivel 3 nunca se quede sin turno.")


if __name__ == "__main__":
    main()
