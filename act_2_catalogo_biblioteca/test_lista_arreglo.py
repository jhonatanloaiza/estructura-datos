"""Pruebas de ListaArreglo (Parte A): contrato, casos extremos y restricciones."""

import ast
import random
from pathlib import Path

import pytest

from lista_arreglo import NO_ENCONTRADO, ListaArreglo


def lista_con(*valores):
    lista = ListaArreglo()
    for v in valores:
        lista.insertar(len(lista), v)
    return lista


# -- lista vacía ------------------------------------------------------------


def test_lista_nueva_esta_vacia():
    lista = ListaArreglo()
    assert lista.esta_vacia()
    assert len(lista) == 0
    assert list(lista) == []


def test_obtener_en_lista_vacia_lanza_error():
    with pytest.raises(IndexError):
        ListaArreglo().obtener(0)


def test_buscar_en_lista_vacia_no_encuentra():
    lista = ListaArreglo()
    assert lista.buscar_lineal("x") == NO_ENCONTRADO
    assert lista.buscar_binaria("x") == NO_ENCONTRADO


def test_insertar_en_la_posicion_cero_de_una_lista_vacia():
    lista = ListaArreglo()
    lista.insertar(0, "a")
    assert list(lista) == ["a"]


def test_insertar_ordenado_en_lista_vacia():
    lista = ListaArreglo()
    lista.insertar_ordenado(5)
    assert list(lista) == [5]


# -- un elemento ------------------------------------------------------------


def test_un_elemento_se_obtiene_y_se_encuentra():
    lista = lista_con(7)
    assert lista.obtener(0) == 7
    assert lista.buscar_lineal(7) == 0
    assert lista.buscar_binaria(7) == 0
    assert not lista.esta_vacia()


def test_un_elemento_no_encuentra_otro_valor():
    lista = lista_con(7)
    assert lista.buscar_lineal(8) == NO_ENCONTRADO
    assert lista.buscar_binaria(6) == NO_ENCONTRADO
    assert lista.buscar_binaria(8) == NO_ENCONTRADO


@pytest.mark.parametrize("nuevo, esperado", [(5, [5, 7]), (9, [7, 9])])
def test_insertar_ordenado_con_un_elemento_antes_y_despues(nuevo, esperado):
    lista = lista_con(7)
    lista.insertar_ordenado(nuevo)
    assert list(lista) == esperado


# -- insertar al inicio, al final y en medio --------------------------------


def test_insertar_al_inicio_desplaza_a_todos():
    lista = lista_con("b", "c")
    lista.insertar(0, "a")
    assert list(lista) == ["a", "b", "c"]


def test_insertar_al_final_no_mueve_a_nadie():
    lista = lista_con("a", "b")
    lista.insertar(2, "c")
    assert list(lista) == ["a", "b", "c"]


def test_insertar_en_medio():
    lista = lista_con("a", "c")
    lista.insertar(1, "b")
    assert list(lista) == ["a", "b", "c"]


@pytest.mark.parametrize("pos", [-1, 3])
def test_insertar_fuera_de_rango_lanza_error_y_no_cambia_la_lista(pos):
    lista = lista_con("a", "b")
    with pytest.raises(IndexError):
        lista.insertar(pos, "x")
    assert list(lista) == ["a", "b"]


@pytest.mark.parametrize("pos", ["0", 1.0, True, None])
def test_posicion_que_no_es_entero_lanza_error(pos):
    lista = lista_con("a", "b")
    with pytest.raises(TypeError):
        lista.obtener(pos)
    with pytest.raises(TypeError):
        lista.insertar(pos, "x")


@pytest.mark.parametrize("pos", [-1, 2])
def test_obtener_fuera_de_rango_lanza_error(pos):
    with pytest.raises(IndexError):
        lista_con("a", "b").obtener(pos)


# -- crecimiento del bloque -------------------------------------------------


def test_crecer_mas_alla_de_la_capacidad_no_pierde_datos():
    lista = ListaArreglo(capacidad=1)
    for i in range(1000):
        lista.insertar(len(lista), i)
    assert len(lista) == 1000
    assert list(lista) == list(range(1000))


def test_insertar_al_inicio_justo_cuando_el_bloque_esta_lleno():
    lista = ListaArreglo(capacidad=2)
    lista.insertar(0, "b")
    lista.insertar(1, "c")
    lista.insertar(0, "a")
    assert list(lista) == ["a", "b", "c"]


@pytest.mark.parametrize("capacidad", [0, -1])
def test_capacidad_no_positiva_lanza_error(capacidad):
    with pytest.raises(ValueError):
        ListaArreglo(capacidad)


# -- búsquedas --------------------------------------------------------------


@pytest.mark.parametrize("x, pos", [(10, 0), (30, 2), (50, 4)])
def test_las_dos_busquedas_encuentran_primero_medio_y_ultimo(x, pos):
    lista = lista_con(10, 20, 30, 40, 50)
    assert lista.buscar_lineal(x) == pos
    assert lista.buscar_binaria(x) == pos


@pytest.mark.parametrize("x", [5, 25, 55])
def test_las_dos_busquedas_fallan_antes_entre_y_despues(x):
    lista = lista_con(10, 20, 30, 40, 50)
    assert lista.buscar_lineal(x) == NO_ENCONTRADO
    assert lista.buscar_binaria(x) == NO_ENCONTRADO


def test_buscar_lineal_funciona_sin_orden():
    assert lista_con(30, 10, 20).buscar_lineal(10) == 1


def test_con_repetidos_las_dos_busquedas_dan_la_primera_aparicion():
    lista = lista_con(1, 2, 2, 2, 3)
    assert lista.buscar_lineal(2) == 1
    assert lista.buscar_binaria(2) == 1


def test_buscar_con_valores_que_son_falsos_en_python():
    lista = lista_con(0, 1)
    assert lista.buscar_lineal(0) == 0
    assert lista.buscar_binaria(0) == 0


# -- insertar_ordenado ------------------------------------------------------


@pytest.mark.parametrize("x, pos", [(5, 0), (25, 2), (55, 5)])
def test_insertar_ordenado_al_inicio_en_medio_y_al_final(x, pos):
    lista = lista_con(10, 20, 30, 40, 50)
    lista.insertar_ordenado(x)
    assert lista.obtener(pos) == x
    assert len(lista) == 6


def test_insertar_ordenado_admite_repetidos():
    lista = lista_con(1, 2, 3)
    lista.insertar_ordenado(2)
    assert list(lista) == [1, 2, 2, 3]


def test_insertar_ordenado_con_valor_que_no_se_compara_no_cambia_la_lista():
    lista = lista_con(1, 2, 3)
    with pytest.raises(TypeError):
        lista.insertar_ordenado("x")
    assert list(lista) == [1, 2, 3]


def test_insertar_ordenado_de_datos_al_azar_deja_todo_ordenado():
    rng = random.Random(2)
    valores = [rng.randrange(1000) for _ in range(500)]
    lista = ListaArreglo()
    for v in valores:
        lista.insertar_ordenado(v)
    assert list(lista) == sorted(valores)


def test_la_busqueda_binaria_coincide_con_la_lineal_en_datos_al_azar():
    rng = random.Random(3)
    lista = ListaArreglo()
    for _ in range(300):
        lista.insertar_ordenado(rng.randrange(600))
    for x in range(-1, 601):
        assert lista.buscar_binaria(x) == lista.buscar_lineal(x)


# -- conteo de operaciones (respalda prediccion.md) -------------------------


class Clave:
    """Entero que cuenta las comparaciones que recibe."""

    comparaciones = 0

    def __init__(self, valor):
        self.valor = valor

    def __eq__(self, otra):
        Clave.comparaciones += 1
        return self.valor == otra.valor

    def __lt__(self, otra):
        Clave.comparaciones += 1
        return self.valor < otra.valor


class BloqueContado(list):
    """Bloque que cuenta las escrituras que recibe."""

    escrituras = 0

    def __setitem__(self, i, x):
        BloqueContado.escrituras += 1
        super().__setitem__(i, x)


def lista_de_claves(n):
    lista = ListaArreglo(capacidad=n + 1)
    for i in range(n):
        lista.insertar(i, Clave(2 * i))
    return lista


def comparaciones_de(operacion):
    Clave.comparaciones = 0
    operacion()
    return Clave.comparaciones


def test_buscar_lineal_compara_hasta_dar_con_el_elemento():
    n = 1000
    lista = lista_de_claves(n)
    assert comparaciones_de(lambda: lista.buscar_lineal(Clave(0))) == 1
    assert comparaciones_de(lambda: lista.buscar_lineal(Clave(2 * 499))) == 500
    assert comparaciones_de(lambda: lista.buscar_lineal(Clave(2 * (n - 1)))) == n


def test_buscar_lineal_fallida_compara_con_todos():
    n = 1000
    lista = lista_de_claves(n)
    assert comparaciones_de(lambda: lista.buscar_lineal(Clave(1))) == n


@pytest.mark.parametrize("n, tope", [(1_000, 11), (10_000, 15), (80_000, 18), (200_000, 19)])
def test_buscar_binaria_llega_justo_al_tope_de_la_prediccion(n, tope):
    lista = lista_de_claves(n)
    rng = random.Random(n)
    objetivos = [rng.randrange(2 * n + 1) for _ in range(500)]
    peor = max(comparaciones_de(lambda: lista.buscar_binaria(Clave(x))) for x in objetivos)
    assert peor == tope


@pytest.mark.parametrize("n, tope", [(1_000, 10), (80_000, 17)])
def test_insertar_ordenado_compara_a_lo_sumo_lo_de_la_busqueda(n, tope):
    lista = lista_de_claves(n)
    assert comparaciones_de(lambda: lista.insertar_ordenado(Clave(n))) <= tope


@pytest.mark.parametrize("pos, escrituras", [(0, 1001), (400, 601), (1000, 1)])
def test_insertar_escribe_lo_desplazado_mas_el_elemento_nuevo(pos, escrituras):
    lista = ListaArreglo(capacidad=2000)
    for i in range(1000):
        lista.insertar(i, i)
    lista._datos = BloqueContado(lista._datos)
    BloqueContado.escrituras = 0
    lista.insertar(pos, "nuevo")
    assert BloqueContado.escrituras == escrituras


# -- restricciones del enunciado --------------------------------------------


def test_lista_arreglo_no_usa_atajos_prohibidos():
    fuente = Path(__file__).with_name("lista_arreglo.py").read_text(encoding="utf-8")
    prohibidos = {"insert", "append", "extend", "pop", "remove", "index", "sort",
                  "count", "reverse", "copy"}
    for nodo in ast.walk(ast.parse(fuente)):
        assert not isinstance(nodo, (ast.Import, ast.ImportFrom, ast.Slice))
        if isinstance(nodo, ast.Attribute):
            assert nodo.attr not in prohibidos
        if isinstance(nodo, ast.Compare):
            assert not any(isinstance(op, (ast.In, ast.NotIn)) for op in nodo.ops)
        if isinstance(nodo, ast.Call) and isinstance(nodo.func, ast.Name):
            assert nodo.func.id != "sorted"
