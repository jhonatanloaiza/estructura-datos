"""Pruebas de la cola de prioridad (Parte B): niveles, patrón de turnos, y la
demostración de que el hueco entre dos atenciones consecutivas de nivel 3
nunca supera `len(PATRON_TURNOS) - 1` atenciones de otros, aunque lleguen sin
parar solicitudes de nivel 1 y 2 (spec.md §7, caso límite 3). Ver la
aclaración en el docstring de `cola_prioridad.py`: esto acota el hueco entre
servicios de nivel 3, no la espera de cada solicitud si ya hay otras de nivel
3 delante en su propia fila.
"""

import pytest

from cola import ColaVaciaError
from cola_prioridad import ColaPrioridad, PATRON_TURNOS


# -- básico -------------------------------------------------------------------

def test_cola_nueva_esta_vacia():
    cola = ColaPrioridad()
    assert cola.esta_vacia()
    assert cola.cuantos_hay() == {1: 0, 2: 0, 3: 0}


def test_decolar_con_cola_vacia_lanza_error():
    cola = ColaPrioridad()
    with pytest.raises(ColaVaciaError):
        cola.decolar()


@pytest.mark.parametrize("nivel", [0, 4, -1, "alta"])
def test_encolar_nivel_invalido_lanza_valueerror(nivel):
    cola = ColaPrioridad()
    with pytest.raises(ValueError):
        cola.encolar("dato", nivel)
    assert cola.esta_vacia()


def test_cuantos_hay_desglosa_por_nivel():
    cola = ColaPrioridad()
    cola.encolar("a", 1)
    cola.encolar("b", 1)
    cola.encolar("c", 3)
    assert cola.cuantos_hay() == {1: 2, 2: 0, 3: 1}


# -- orden dentro de un mismo nivel: FIFO --------------------------------------

def test_mismo_nivel_sale_en_orden_de_llegada():
    cola = ColaPrioridad()
    a = cola.encolar("primero", 2)
    b = cola.encolar("segundo", 2)
    c = cola.encolar("tercero", 2)
    assert [cola.decolar() for _ in range(3)] == [a, b, c]


# -- prioridad entre niveles ----------------------------------------------------

def test_nivel_mas_urgente_se_prefiere_sobre_el_orden_de_llegada():
    cola = ColaPrioridad()
    # nivel 3 llega primero, pero nivel 1 llega después: en el primer turno
    # del patrón (reservado para nivel 1) y con nivel 1 no vacío, nivel 1 gana.
    tardio_urgente = cola.encolar("llego_tarde_pero_urgente", 1)
    cola.encolar("llego_primero_pero_normal", 3)
    assert cola.decolar() is tardio_urgente


# -- el turno reservado vacío cae en prioridad estricta -------------------------

def test_turno_reservado_vacio_no_detiene_la_atencion():
    cola = ColaPrioridad()
    # solo hay niveles 1 y 2: cuando el patrón reserve el turno para el nivel
    # 3 (posición 6), como no hay nadie de nivel 3, debe atender igual
    # (por prioridad estricta), no saltarse la atención ni fallar.
    for _ in range(4):
        cola.encolar("n1", 1)
    for _ in range(3):
        cola.encolar("n2", 2)
    atendidos = [cola.decolar() for _ in range(7)]
    assert len(atendidos) == 7
    assert cola.esta_vacia()


# -- la cota contra la espera indefinida (caso límite 3 de spec.md) -----------

def test_racha_sostenida_de_niveles_1_y_2_no_hace_esperar_a_nivel_3_mas_de_un_ciclo():
    cola = ColaPrioridad()

    def llega_mas_trabajo_urgente():
        cola.encolar("urgente", 1)
        cola.encolar("prioritaria", 2)

    # nivel 1 y 2 nunca se quedan vacíos: cada ronda llega más que lo que se
    # atiende, como en una racha sostenida de evaluaciones.
    llega_mas_trabajo_urgente()
    llega_mas_trabajo_urgente()
    objetivo = cola.encolar("consulta_normal", 3)

    cota = len(PATRON_TURNOS) - 1  # 6
    atenciones_de_otros = 0
    for _ in range(len(PATRON_TURNOS) + 1):  # margen de seguridad para la prueba
        llega_mas_trabajo_urgente()
        atendido = cola.decolar()
        if atendido is objetivo:
            break
        atenciones_de_otros += 1
    else:
        pytest.fail("nivel 3 no fue atendido dentro de un ciclo del patrón")

    assert atenciones_de_otros <= cota


def test_el_patron_avanza_aunque_el_turno_reservado_este_vacio():
    """Si el nivel 2 nunca recibe nada, el índice del patrón no se puede
    quedar detenido en la posición reservada para el nivel 2: si se quedara
    ahí, nunca llegaría a la posición reservada para el nivel 3, y nivel 3
    quedaría bloqueado para siempre mientras nivel 1 no deje de llegar
    (`cola_prioridad.py`, docstring del módulo)."""
    cola = ColaPrioridad()
    for i in range(20):
        cola.encolar(f"n1_{i}", 1)
    objetivo = cola.encolar("normal", 3)
    # nivel 2 nunca recibe nada en esta prueba.

    cota = len(PATRON_TURNOS) - 1
    for i in range(cota + 1):
        atendido = cola.decolar()
        cola.encolar(f"n1_extra_{i}", 1)  # nivel 1 nunca se vacía
        if atendido is objetivo:
            return

    pytest.fail("nivel 3 quedó bloqueado: el patrón no avanzó al no encontrar nivel 2")


def test_el_hueco_entre_atenciones_de_nivel_3_respeta_la_cota_aunque_se_acumulen_varias():
    """Con varias solicitudes de nivel 3 ya acumuladas, cada una debe esperar
    su turno dentro de su propia fila (FIFO) además del ciclo del patrón; lo
    que sí está acotado es el hueco entre una atención de nivel 3 y la
    siguiente, no el tiempo total de cada solicitud individual."""
    cola = ColaPrioridad()

    def llega_mas_trabajo_urgente():
        cola.encolar("urgente", 1)
        cola.encolar("prioritaria", 2)

    llega_mas_trabajo_urgente()
    llega_mas_trabajo_urgente()
    objetivos = [cola.encolar(f"normal_{i}", 3) for i in range(3)]

    cota = len(PATRON_TURNOS) - 1
    ids_pendientes = {id(s) for s in objetivos}
    esperas = {}
    atenciones_desde_ultimo = 0
    for _ in range(100):
        if not ids_pendientes:
            break
        llega_mas_trabajo_urgente()
        atendido = cola.decolar()
        if id(atendido) in ids_pendientes:
            esperas[id(atendido)] = atenciones_desde_ultimo
            ids_pendientes.remove(id(atendido))
            atenciones_desde_ultimo = 0
        else:
            atenciones_desde_ultimo += 1

    assert not ids_pendientes, "quedaron solicitudes de nivel 3 sin atender"
    assert all(espera <= cota for espera in esperas.values())
