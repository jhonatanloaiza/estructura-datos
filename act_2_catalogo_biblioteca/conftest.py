"""Permite correr `pytest` desde la raíz del repositorio.

act_3 también tiene un `lista_arreglo.py`, con otro contrato. Python guarda los
módulos por nombre, así que al correr todo junto act_3 recibiría el de esta
carpeta. Se olvida el módulo apenas se recolecta esta carpeta: las pruebas de
aquí conservan su referencia y act_3 importa el suyo.
"""

import sys
from pathlib import Path

CARPETA = Path(__file__).parent


def pytest_collectreport(report):
    modulo = sys.modules.get("lista_arreglo")
    if modulo is not None and Path(modulo.__file__).parent == CARPETA:
        del sys.modules["lista_arreglo"]
