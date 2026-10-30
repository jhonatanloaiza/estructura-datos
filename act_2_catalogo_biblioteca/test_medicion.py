"""Pruebas de la preparación de las mediciones: si los datos de partida están mal,
los tiempos también, y nada en `resultados.csv` lo delataría."""

import random

import pytest

import medicion
from lista_arreglo import NO_ENCONTRADO
from medicion import Catalogo


@pytest.fixture
def catalogo():
    return Catalogo(1000, random.Random(1))


def test_el_catalogo_por_clave_queda_ordenado_con_los_mismos_registros(catalogo):
    assert catalogo.por_clave == sorted(catalogo.por_llegada)


def test_el_catalogo_por_llegada_no_esta_ordenado(catalogo):
    assert catalogo.por_llegada != catalogo.por_clave


def test_los_dos_catalogos_comparten_los_mismos_objetos(catalogo):
    assert {id(r) for r in catalogo.por_llegada} == {id(r) for r in catalogo.por_clave}


def test_los_registros_existentes_se_encuentran(catalogo):
    for x in catalogo.existentes(100):
        assert catalogo.ordenado.buscar_binaria(x) != NO_ENCONTRADO
        assert catalogo.desordenado.buscar_lineal(x) != NO_ENCONTRADO


def test_los_registros_nuevos_no_estan_en_el_catalogo(catalogo):
    for x in catalogo.nuevos(100):
        assert catalogo.ordenado.buscar_binaria(x) == NO_ENCONTRADO


def test_se_repite_al_menos_cinco_veces():
    assert medicion.REPETICIONES >= 5


@pytest.mark.parametrize("medidor", medicion.MEDIDORES, ids=lambda m: m.__name__)
def test_cada_medidor_devuelve_un_tiempo_positivo(medidor, catalogo):
    lote, tiempo = medicion.medir(medidor, catalogo)
    assert lote > 0
    assert tiempo > 0


def test_insertar_ordenado_deja_el_catalogo_ordenado_y_no_toca_el_original(catalogo):
    preparar, ejecutar, lote = medicion.insertar_ordenado(catalogo)
    lista, nuevos = preparar()
    ejecutar(lista, nuevos)
    assert len(lista) == catalogo.n + lote
    assert list(lista) == sorted(lista)
    assert len(catalogo.ordenado) == catalogo.n


@pytest.mark.parametrize("n", medicion.TAMANOS)
def test_el_lote_de_insercion_no_cambia_mucho_el_tamano(n):
    assert medicion._lote_insercion(n) / n <= 0.05
