"""Fixture compartida: la misma batería corre contra las dos implementaciones.

`test_contrato.py` (el archivo de la actividad 2) no se modifica: para probar
otra estructura basta con agregarla aquí.
"""

import pytest

from lista_arreglo import ListaArreglo
from lista_enlazada import ListaEnlazada

IMPLEMENTACIONES = [
    pytest.param(ListaArreglo, id="arreglo"),
    pytest.param(ListaEnlazada, id="enlazada"),
]


@pytest.fixture(params=IMPLEMENTACIONES)
def Lista(request):
    return request.param
