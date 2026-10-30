"""Pruebas de las cuentas de `analisis.py`, de donde salen las cifras de los informes."""

import pytest

import analisis

TAMANO = 100


@pytest.fixture
def tabla():
    return {
        ("buscar_binaria", TAMANO): [1.0],
        ("buscar_lineal", TAMANO): [11.0],
        ("insertar_ordenado", TAMANO): [32.0],
        ("insertar_final", TAMANO): [2.0],
    }


def test_costo_ordenado_suma_las_busquedas_y_la_insercion(tabla):
    assert analisis.costo_ordenado(tabla, TAMANO, 5) == 5 * 1 + 32


def test_costo_desordenado_suma_las_busquedas_y_la_insercion(tabla):
    assert analisis.costo_desordenado(tabla, TAMANO, 5) == 5 * 11 + 2


def test_el_equilibrio_despeja_la_ecuacion_del_enunciado(tabla):
    assert analisis.equilibrio(tabla, TAMANO) == 3


def test_en_el_equilibrio_los_dos_catalogos_cuestan_lo_mismo(tabla):
    s = analisis.equilibrio(tabla, TAMANO)
    assert analisis.costo_ordenado(tabla, TAMANO, s) == analisis.costo_desordenado(tabla, TAMANO, s)


def test_por_encima_del_equilibrio_gana_el_ordenado(tabla):
    s = analisis.equilibrio(tabla, TAMANO) + 1
    assert analisis.costo_ordenado(tabla, TAMANO, s) < analisis.costo_desordenado(tabla, TAMANO, s)


def test_por_debajo_del_equilibrio_gana_el_desordenado(tabla):
    s = analisis.equilibrio(tabla, TAMANO) - 1
    assert analisis.costo_desordenado(tabla, TAMANO, s) < analisis.costo_ordenado(tabla, TAMANO, s)


def test_la_fraccion_para_cambiar_empata_los_costos(tabla):
    s = 5
    fraccion = analisis.fraccion_para_cambiar(tabla, TAMANO, s)
    tabla["buscar_lineal", TAMANO] = [11.0 * fraccion / 0.5]
    assert analisis.costo_desordenado(tabla, TAMANO, s) == pytest.approx(
        analisis.costo_ordenado(tabla, TAMANO, s))


def test_la_mediana_ignora_una_repeticion_atipica():
    tabla = {("buscar_lineal", TAMANO): [10.0, 10.0, 999.0]}
    assert analisis.mediana(tabla, "buscar_lineal", TAMANO) == 10


def test_formato_con_miles_y_decimales_colombianos():
    assert analisis.es(1234.5) == "1.234,5"
    assert analisis.es(80000, 0) == "80.000"


@pytest.mark.parametrize("clase, crecimiento, esperado", [
    ("O(1)", 1.2, True),
    ("O(1)", 1.8, False),
    ("O(log n)", 1.7, True),
    ("O(log n)", 2.3, False),
])
def test_criterios_de_coincidencia(clase, crecimiento, esperado):
    tabla = {("op", n): [crecimiento if n == analisis.TAMANOS[-1] else 1.0]
             for n in analisis.TAMANOS}
    assert analisis.coincide(clase, tabla, "op") is esperado


@pytest.mark.parametrize("subida, esperado", [(200, True), (660, False)])
def test_criterio_de_coincidencia_lineal(subida, esperado):
    tabla = {("op", n): [subida if n == analisis.TAMANOS[-1] else 1.0]
             for n in analisis.TAMANOS}
    assert analisis.coincide("O(n)", tabla, "op") is esperado


def test_resultados_csv_tiene_todos_los_casos_con_cinco_repeticiones_o_mas():
    tabla = analisis.leer()
    for n in analisis.TAMANOS:
        for operacion in analisis.CRITERIOS:
            assert len(tabla[operacion, n]) >= 5
