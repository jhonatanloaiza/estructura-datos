"""Pruebas de la cola simple (Parte A): comportamiento FIFO y casos límite."""

import pytest

from cola import Cola, ColaVaciaError


def test_cola_nueva_esta_vacia():
    cola = Cola()
    assert cola.esta_vacia()
    assert len(cola) == 0


def test_encolar_decolar_respeta_el_orden_de_llegada():
    cola = Cola()
    for x in ["a", "b", "c"]:
        cola.encolar(x)
    assert [cola.decolar() for _ in range(3)] == ["a", "b", "c"]
    assert cola.esta_vacia()


def test_frente_no_retira_el_elemento():
    cola = Cola()
    cola.encolar("a")
    cola.encolar("b")
    assert cola.frente() == "a"
    assert len(cola) == 2
    assert cola.decolar() == "a"


def test_decolar_con_cola_vacia_lanza_error():
    cola = Cola()
    with pytest.raises(ColaVaciaError):
        cola.decolar()


def test_frente_con_cola_vacia_lanza_error():
    cola = Cola()
    with pytest.raises(ColaVaciaError):
        cola.frente()


def test_un_elemento_queda_vacia_tras_decolar():
    cola = Cola()
    cola.encolar("solo")
    assert cola.decolar() == "solo"
    assert cola.esta_vacia()


def test_tras_vaciarse_se_puede_volver_a_usar():
    cola = Cola()
    cola.encolar("a")
    cola.decolar()
    cola.encolar("b")
    cola.encolar("c")
    assert [cola.decolar() for _ in range(2)] == ["b", "c"]
    assert cola.esta_vacia()


def test_mezcla_de_encolar_y_decolar_intercalados():
    cola = Cola()
    cola.encolar(1)
    cola.encolar(2)
    assert cola.decolar() == 1
    cola.encolar(3)
    assert cola.decolar() == 2
    assert cola.decolar() == 3
    assert cola.esta_vacia()


def test_admite_datos_repetidos_y_cualquier_tipo():
    cola = Cola()
    for x in [None, 0, "", "x", "x"]:
        cola.encolar(x)
    assert [cola.decolar() for _ in range(5)] == [None, 0, "", "x", "x"]
