"""Pruebas del núcleo del CDA (sin HTTP): `cola_atencion.ColaAtencion`.

Incluye los casos límite exigidos en `spec.md` §7: cola vacía, un elemento,
empate de prioridad, y remoción de un nodo que no es la raíz.
"""

import random

import pytest

from cola_atencion import ColaAtencion, ColaVaciaError, SolicitudNoEncontradaError


def registrar(cola, tipo="paciente", nombre="N", ident="1", motivo="dolor",
               nivel=3):
    return cola.registrar(tipo, nombre, ident, motivo, nivel)


# -- registrar y validaciones ---------------------------------------------------

def test_registrar_devuelve_solicitud_con_id_y_orden():
    cola = ColaAtencion()
    s1 = registrar(cola, nombre="A")
    s2 = registrar(cola, nombre="B")
    assert s1.id != s2.id
    assert s1.orden_llegada < s2.orden_llegada


@pytest.mark.parametrize("nivel", [0, 6, -1, 100])
def test_registrar_nivel_invalido_lanza_valueerror(nivel):
    cola = ColaAtencion()
    with pytest.raises(ValueError):
        registrar(cola, nivel=nivel)
    assert cola.esta_vacia()


def test_registrar_tipo_invalido_lanza_valueerror():
    cola = ColaAtencion()
    with pytest.raises(ValueError):
        registrar(cola, tipo="ambulancia")
    assert cola.esta_vacia()


@pytest.mark.parametrize("campo", ["nombre", "ident", "motivo"])
def test_registrar_campo_vacio_lanza_valueerror(campo):
    cola = ColaAtencion()
    kwargs = {"nombre": "A", "ident": "1", "motivo": "m"}
    kwargs[campo] = "   "
    with pytest.raises(ValueError):
        registrar(cola, **kwargs)


# -- orden de atención: prioridad y empate --------------------------------------

def test_mayor_urgencia_sale_primero_sin_importar_orden_de_registro():
    cola = ColaAtencion()
    registrar(cola, nombre="rutina", nivel=5)
    registrar(cola, nombre="critico", nivel=1)
    registrar(cola, nombre="urgente", nivel=3)
    assert cola.atender().nombre == "critico"
    assert cola.atender().nombre == "urgente"
    assert cola.atender().nombre == "rutina"


def test_empate_de_prioridad_se_desempata_por_llegada():
    cola = ColaAtencion()
    registrar(cola, nombre="primero", nivel=2)
    registrar(cola, nombre="segundo", nivel=2)
    registrar(cola, nombre="tercero", nivel=2)
    assert [cola.atender().nombre for _ in range(3)] == ["primero", "segundo", "tercero"]


def test_paciente_y_vehiculo_compiten_por_igual():
    cola = ColaAtencion()
    registrar(cola, tipo="vehiculo", nombre="ambulancia", nivel=2)
    registrar(cola, tipo="paciente", nombre="paciente", nivel=2)
    # mismo nivel: gana quien llegó primero, el tipo no influye
    assert cola.atender().nombre == "ambulancia"
    assert cola.atender().nombre == "paciente"


# -- siguiente / atender: caso límite "cola vacía" ------------------------------

def test_vacia_siguiente_lanza_colavaciaerror():
    cola = ColaAtencion()
    with pytest.raises(ColaVaciaError):
        cola.siguiente()


def test_vacia_atender_lanza_colavaciaerror():
    cola = ColaAtencion()
    with pytest.raises(ColaVaciaError):
        cola.atender()


def test_vacia_cuantos_faltan_es_cero_y_no_es_error():
    cola = ColaAtencion()
    resumen = cola.cuantos_faltan()
    assert resumen["total"] == 0
    assert resumen["por_tipo"] == {"paciente": 0, "vehiculo": 0}


def test_vacia_sacar_id_inexistente_lanza_error():
    cola = ColaAtencion()
    with pytest.raises(SolicitudNoEncontradaError):
        cola.sacar(1)


def test_vacia_sigue_funcionando_tras_los_errores():
    cola = ColaAtencion()
    with pytest.raises(ColaVaciaError):
        cola.atender()
    registrar(cola, nombre="nueva")
    assert cola.siguiente().nombre == "nueva"


# -- caso límite "un elemento" ---------------------------------------------------

def test_un_elemento_es_a_la_vez_siguiente_y_unico():
    cola = ColaAtencion()
    s = registrar(cola, nombre="solo")
    assert cola.siguiente().id == s.id
    assert cola.cuantos_faltan()["total"] == 1


def test_un_elemento_atenderlo_deja_la_cola_vacia():
    cola = ColaAtencion()
    registrar(cola, nombre="solo")
    atendida = cola.atender()
    assert atendida.nombre == "solo"
    assert atendida.atendido is True
    assert atendida.atendido_en is not None
    assert cola.esta_vacia()


def test_un_elemento_tras_atenderlo_se_puede_volver_a_registrar():
    cola = ColaAtencion()
    registrar(cola, nombre="solo")
    cola.atender()
    registrar(cola, nombre="nuevo")
    assert cola.siguiente().nombre == "nuevo"
    assert cola.cuantos_faltan()["total"] == 1


# -- sacar: operación distinta de atender ---------------------------------------

def test_sacar_no_lo_marca_como_atendido():
    cola = ColaAtencion()
    s = registrar(cola, nombre="se_retira")
    sacada = cola.sacar(s.id)
    assert sacada.atendido is False
    assert sacada.atendido_en is None
    assert cola.esta_vacia()


def test_sacar_id_ya_sacado_lanza_error():
    cola = ColaAtencion()
    s = registrar(cola)
    cola.sacar(s.id)
    with pytest.raises(SolicitudNoEncontradaError):
        cola.sacar(s.id)


def test_sacar_id_ya_atendido_lanza_error():
    cola = ColaAtencion()
    s = registrar(cola)
    cola.atender()
    with pytest.raises(SolicitudNoEncontradaError):
        cola.sacar(s.id)


# -- caso límite: sacar un nodo que no es la raíz --------------------------------

def test_sacar_nodo_intermedio_conserva_el_orden_del_resto():
    cola = ColaAtencion()
    ids = {}
    for nombre, nivel in [("a", 3), ("b", 1), ("c", 4), ("d", 2), ("e", 5)]:
        ids[nombre] = registrar(cola, nombre=nombre, nivel=nivel).id

    # "a" no es ni la raíz (nivel 1 = "b") ni el último insertado: es un nodo
    # intermedio del montículo.
    cola.sacar(ids["a"])

    orden_esperado = ["b", "d", "c", "e"]
    orden_real = [cola.atender().nombre for _ in range(4)]
    assert orden_real == orden_esperado
    assert cola.esta_vacia()


def test_sacar_la_raiz_promueve_correctamente_al_siguiente():
    cola = ColaAtencion()
    a = registrar(cola, nombre="raiz", nivel=1)
    registrar(cola, nombre="segundo", nivel=2)
    registrar(cola, nombre="tercero", nivel=3)

    cola.sacar(a.id)  # la raíz se saca sin pasar por "atender"

    assert cola.siguiente().nombre == "segundo"
    assert cola.atender().nombre == "segundo"
    assert cola.atender().nombre == "tercero"


# -- posición -------------------------------------------------------------------

def test_posicion_refleja_el_orden_de_prioridad_no_el_de_registro():
    cola = ColaAtencion()
    registrar(cola, nombre="rutina", nivel=5)
    urgente = registrar(cola, nombre="urgente", nivel=1)
    assert cola.posicion(urgente.id) == 1


# -- drenado tras remociones aleatorias (robustez del montículo) ----------------

def test_drenar_tras_sacar_al_azar_sale_en_orden_no_decreciente():
    rng = random.Random(706132)
    cola = ColaAtencion()
    vivos = []
    for i in range(200):
        nivel = rng.randint(1, 5)
        tipo = rng.choice(["paciente", "vehiculo"])
        s = cola.registrar(tipo, f"n{i}", str(i), "motivo", nivel)
        vivos.append(s.id)

    rng.shuffle(vivos)
    for id_ in vivos[:60]:
        cola.sacar(id_)

    anterior = None
    restantes = cola.cuantos_faltan()["total"]
    salida = []
    for _ in range(restantes):
        actual = cola.atender()
        clave_actual = (actual.nivel_prioridad, actual.orden_llegada)
        if anterior is not None:
            assert anterior <= clave_actual
        anterior = clave_actual
        salida.append(actual.id)

    assert cola.esta_vacia()
    assert len(salida) == len(set(salida)) == restantes
