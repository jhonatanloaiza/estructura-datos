"""Los cuatro casos límite: lista vacía, un elemento, borrar el primero y borrar el último.

Son los casos donde una lista enlazada suele fallar (cabeza y cola mal
actualizadas). Cada caso tiene su bloque y sus pruebas por separado, y todos
corren contra las dos implementaciones.

Además de comprobar el resultado inmediato, cada bloque sigue operando sobre la
lista después del caso límite: un puntero mal actualizado casi nunca falla en el
momento, falla en la operación siguiente.
"""

import pytest


def llenar(Lista, *canciones):
    lista = Lista()
    for c in canciones:
        lista.agregar(c)
    return lista


# ===========================================================================
# 1. Lista vacía
# ===========================================================================

def test_vacia_recorrer_no_produce_nada(Lista):
    assert list(Lista()) == []


def test_vacia_obtener_lanza_indexerror(Lista):
    with pytest.raises(IndexError):
        Lista().obtener(0)


def test_vacia_borrar_lanza_indexerror(Lista):
    lista = Lista()
    with pytest.raises(IndexError):
        lista.borrar(0)
    assert len(lista) == 0


def test_vacia_sigue_funcionando_tras_el_error(Lista):
    lista = Lista()
    with pytest.raises(IndexError):
        lista.borrar(0)
    lista.agregar("a")
    lista.insertar_al_principio("z")
    assert list(lista) == ["z", "a"]


def test_vacia_insertar_al_principio_y_agregar_dan_el_mismo_resultado(Lista):
    a, b = Lista(), Lista()
    a.insertar_al_principio("x")
    b.agregar("x")
    assert list(a) == list(b) == ["x"]
    assert len(a) == len(b) == 1


# ===========================================================================
# 2. Lista de un elemento
# ===========================================================================

def test_un_elemento_es_a_la_vez_primero_y_ultimo(Lista):
    lista = llenar(Lista, "solo")
    assert lista.obtener(0) == "solo"
    assert len(lista) == 1
    with pytest.raises(IndexError):
        lista.obtener(1)


def test_un_elemento_borrarlo_deja_la_lista_vacia(Lista):
    lista = llenar(Lista, "solo")
    assert lista.borrar(0) == "solo"
    assert lista.esta_vacia()
    assert list(lista) == []


def test_un_elemento_tras_borrarlo_se_puede_volver_a_usar(Lista):
    # Si la cola quedó apuntando al nodo borrado, este agregar se pierde.
    lista = llenar(Lista, "solo")
    lista.borrar(0)
    lista.agregar("nueva")
    assert list(lista) == ["nueva"]
    lista.agregar("otra")
    assert list(lista) == ["nueva", "otra"]
    assert len(lista) == 2


def test_un_elemento_borrar_y_reinsertar_al_principio(Lista):
    lista = llenar(Lista, "solo")
    lista.borrar(0)
    lista.insertar_al_principio("nueva")
    lista.agregar("fin")
    assert list(lista) == ["nueva", "fin"]


def test_un_elemento_ciclos_repetidos_de_llenar_y_vaciar(Lista):
    lista = Lista()
    for ronda in range(5):
        lista.agregar(ronda)
        assert list(lista) == [ronda]
        assert lista.borrar(0) == ronda
        assert lista.esta_vacia()


# ===========================================================================
# 3. Borrar el primero
# ===========================================================================

def test_borrar_primero_devuelve_la_primera_cancion(Lista):
    lista = llenar(Lista, "a", "b", "c")
    assert lista.borrar(0) == "a"


def test_borrar_primero_el_segundo_pasa_a_ser_primero(Lista):
    lista = llenar(Lista, "a", "b", "c")
    lista.borrar(0)
    assert list(lista) == ["b", "c"]
    assert lista.obtener(0) == "b"
    assert len(lista) == 2


def test_borrar_primero_no_afecta_al_ultimo(Lista):
    lista = llenar(Lista, "a", "b", "c")
    lista.borrar(0)
    lista.agregar("d")
    assert list(lista) == ["b", "c", "d"]


def test_borrar_primero_de_dos_deja_un_elemento_operable(Lista):
    lista = llenar(Lista, "a", "b")
    lista.borrar(0)
    assert list(lista) == ["b"]
    lista.agregar("c")
    assert list(lista) == ["b", "c"]


def test_borrar_primero_hasta_vaciar(Lista):
    lista = llenar(Lista, "a", "b", "c")
    assert [lista.borrar(0) for _ in range(3)] == ["a", "b", "c"]
    assert lista.esta_vacia()
    lista.agregar("x")
    assert list(lista) == ["x"]


# ===========================================================================
# 4. Borrar el último
# ===========================================================================

def test_borrar_ultimo_devuelve_la_ultima_cancion(Lista):
    lista = llenar(Lista, "a", "b", "c")
    assert lista.borrar(2) == "c"


def test_borrar_ultimo_el_penultimo_pasa_a_ser_ultimo(Lista):
    lista = llenar(Lista, "a", "b", "c")
    lista.borrar(2)
    assert list(lista) == ["a", "b"]
    assert lista.obtener(1) == "b"
    assert len(lista) == 2
    with pytest.raises(IndexError):
        lista.obtener(2)


def test_borrar_ultimo_y_luego_agregar_no_pierde_la_cancion(Lista):
    # Si la cola sigue apuntando al nodo borrado, "d" se cuelga de un nodo
    # que ya no está en la cadena y desaparece.
    lista = llenar(Lista, "a", "b", "c")
    lista.borrar(2)
    lista.agregar("d")
    assert list(lista) == ["a", "b", "d"]
    assert len(lista) == 3


def test_borrar_ultimo_varias_veces_seguidas(Lista):
    lista = llenar(Lista, "a", "b", "c", "d")
    assert [lista.borrar(len(lista) - 1) for _ in range(3)] == ["d", "c", "b"]
    assert list(lista) == ["a"]
    lista.agregar("z")
    assert list(lista) == ["a", "z"]


def test_borrar_ultimo_de_dos_deja_un_elemento_operable(Lista):
    lista = llenar(Lista, "a", "b")
    lista.borrar(1)
    assert list(lista) == ["a"]
    lista.insertar_al_principio("z")
    lista.agregar("y")
    assert list(lista) == ["z", "a", "y"]


def test_borrar_ultimo_tras_insertar_al_principio(Lista):
    lista = Lista()
    lista.insertar_al_principio("b")
    lista.insertar_al_principio("a")
    assert lista.borrar(1) == "b"
    lista.agregar("c")
    assert list(lista) == ["a", "c"]
