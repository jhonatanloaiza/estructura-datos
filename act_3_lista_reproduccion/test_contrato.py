"""Pruebas del contrato de la lista de reproducción (archivo de la actividad 2).

No se modifica al pasar de `ListaArreglo` a `ListaEnlazada`: solo usa la
interfaz pública descrita en `spec.md`. La clase la entrega la fixture `Lista`
(ver `conftest.py`).
"""

import pytest


def llenar(Lista, *canciones):
    lista = Lista()
    for c in canciones:
        lista.agregar(c)
    return lista


# -- estado inicial -----------------------------------------------------------

def test_lista_nueva_esta_vacia(Lista):
    lista = Lista()
    assert lista.esta_vacia()
    assert len(lista) == 0
    assert list(lista) == []


# -- insertar -----------------------------------------------------------------

def test_insertar_al_principio_deja_la_cancion_primera(Lista):
    lista = llenar(Lista, "b", "c")
    lista.insertar_al_principio("a")
    assert list(lista) == ["a", "b", "c"]
    assert len(lista) == 3


def test_insertar_al_principio_repetido_invierte_el_orden(Lista):
    lista = Lista()
    for c in "abcde":
        lista.insertar_al_principio(c)
    assert list(lista) == list("edcba")


def test_agregar_deja_la_cancion_al_final(Lista):
    lista = llenar(Lista, "a", "b")
    lista.agregar("c")
    assert list(lista) == ["a", "b", "c"]


def test_mezcla_de_inserciones_conserva_el_orden(Lista):
    lista = Lista()
    lista.agregar("b")
    lista.insertar_al_principio("a")
    lista.agregar("c")
    lista.insertar_al_principio("z")
    assert list(lista) == ["z", "a", "b", "c"]


def test_crece_mas_alla_de_cualquier_capacidad_inicial(Lista):
    lista = Lista()
    for i in range(1000):
        lista.agregar(i)
    assert len(lista) == 1000
    assert list(lista) == list(range(1000))


# -- obtener ------------------------------------------------------------------

def test_obtener_devuelve_la_cancion_de_cada_posicion(Lista):
    lista = llenar(Lista, "a", "b", "c", "d")
    assert [lista.obtener(i) for i in range(4)] == ["a", "b", "c", "d"]


def test_obtener_no_modifica_la_lista(Lista):
    lista = llenar(Lista, "a", "b", "c")
    lista.obtener(1)
    assert list(lista) == ["a", "b", "c"]
    assert len(lista) == 3


@pytest.mark.parametrize("i", [-1, 3, 100])
def test_obtener_fuera_de_rango_lanza_indexerror(Lista, i):
    lista = llenar(Lista, "a", "b", "c")
    with pytest.raises(IndexError):
        lista.obtener(i)


@pytest.mark.parametrize("i", ["1", 1.0, None, True])
def test_obtener_con_indice_no_entero_lanza_typeerror(Lista, i):
    lista = llenar(Lista, "a", "b", "c")
    with pytest.raises(TypeError):
        lista.obtener(i)


# -- borrar -------------------------------------------------------------------

def test_borrar_devuelve_la_cancion_borrada(Lista):
    lista = llenar(Lista, "a", "b", "c")
    assert lista.borrar(1) == "b"


def test_borrar_del_medio_cierra_el_hueco(Lista):
    lista = llenar(Lista, "a", "b", "c", "d")
    lista.borrar(2)
    assert list(lista) == ["a", "b", "d"]
    assert len(lista) == 3


def test_borrar_repetido_en_la_misma_posicion(Lista):
    lista = llenar(Lista, "a", "b", "c", "d")
    assert [lista.borrar(1) for _ in range(3)] == ["b", "c", "d"]
    assert list(lista) == ["a"]


@pytest.mark.parametrize("i", [-1, 3, 100])
def test_borrar_fuera_de_rango_lanza_indexerror_y_no_cambia_nada(Lista, i):
    lista = llenar(Lista, "a", "b", "c")
    with pytest.raises(IndexError):
        lista.borrar(i)
    assert list(lista) == ["a", "b", "c"]
    assert len(lista) == 3


def test_borrar_con_indice_no_entero_lanza_typeerror(Lista):
    lista = llenar(Lista, "a", "b")
    with pytest.raises(TypeError):
        lista.borrar("0")
    assert list(lista) == ["a", "b"]


# -- recorrer -----------------------------------------------------------------

def test_recorrer_dos_veces_da_lo_mismo(Lista):
    lista = llenar(Lista, "a", "b", "c")
    assert list(lista) == list(lista) == ["a", "b", "c"]


def test_recorrer_no_consume_la_lista(Lista):
    lista = llenar(Lista, "a", "b", "c")
    for _ in lista:
        pass
    assert len(lista) == 3


# -- independencia y datos repetidos -------------------------------------------

def test_dos_listas_no_comparten_estado(Lista):
    l1, l2 = Lista(), Lista()
    l1.agregar("a")
    assert list(l2) == []
    assert len(l2) == 0


def test_admite_canciones_repetidas_y_borra_solo_una(Lista):
    lista = llenar(Lista, "x", "x", "x")
    lista.borrar(1)
    assert list(lista) == ["x", "x"]


def test_admite_cualquier_tipo_de_dato_incluido_none(Lista):
    lista = llenar(Lista, None, 0, "", (1, 2))
    assert list(lista) == [None, 0, "", (1, 2)]
    assert lista.obtener(0) is None
