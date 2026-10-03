"""Pruebas de la API con TestClient: un flujo feliz completo y los errores.

Cada prueba crea su propia `ColaAtencion` (fixture `cliente`) para no
arrastrar estado entre pruebas, aunque la API en producción use una sola cola
en memoria durante la vida del proceso (`spec.md` §8, fuera de alcance:
persistencia y aislamiento multiusuario).
"""

import pytest
from fastapi.testclient import TestClient

import main
from cola_atencion import ColaAtencion


@pytest.fixture
def cliente():
    main.cola = ColaAtencion()
    return TestClient(main.app)


def registrar(cliente, tipo="paciente", nombre="N", identificacion="1",
               motivo="dolor", nivel_prioridad=3):
    return cliente.post("/registrar", json={
        "tipo": tipo, "nombre": nombre, "identificacion": identificacion,
        "motivo": motivo, "nivel_prioridad": nivel_prioridad,
    })


# -- flujo feliz ------------------------------------------------------------

def test_registrar_devuelve_201_con_id_y_posicion(cliente):
    r = registrar(cliente, nombre="Ana", nivel_prioridad=2)
    assert r.status_code == 201
    cuerpo = r.json()
    assert cuerpo["solicitud"]["nombre"] == "Ana"
    assert cuerpo["solicitud"]["atendido"] is False
    assert cuerpo["posicion_en_cola"] == 1


def test_siguiente_devuelve_la_mas_urgente(cliente):
    registrar(cliente, nombre="rutina", nivel_prioridad=5)
    registrar(cliente, nombre="critico", nivel_prioridad=1)
    r = cliente.get("/siguiente")
    assert r.status_code == 200
    assert r.json()["nombre"] == "critico"


def test_atender_retira_e_indica_el_tipo(cliente):
    registrar(cliente, tipo="vehiculo", nombre="ambulancia", nivel_prioridad=1)
    r = cliente.post("/atender")
    assert r.status_code == 200
    cuerpo = r.json()
    assert cuerpo["tipo"] == "vehiculo"
    assert cuerpo["atendido"] is True
    assert cliente.get("/estado").json()["total"] == 0


def test_sacar_quita_sin_marcar_atendido(cliente):
    id_creado = registrar(cliente, nombre="se_retira").json()["solicitud"]["id"]
    r = cliente.delete(f"/cola/{id_creado}")
    assert r.status_code == 200
    assert r.json()["atendido"] is False
    assert cliente.get("/estado").json()["total"] == 0


def test_estado_desglosa_por_tipo_y_nivel(cliente):
    registrar(cliente, tipo="paciente", nivel_prioridad=1)
    registrar(cliente, tipo="paciente", nivel_prioridad=1)
    registrar(cliente, tipo="vehiculo", nivel_prioridad=3)
    r = cliente.get("/estado")
    cuerpo = r.json()
    assert cuerpo["total"] == 3
    assert cuerpo["por_tipo"] == {"paciente": 2, "vehiculo": 1}
    # JSON no tiene claves enteras: el 1 y el 3 de Python llegan como "1" y "3".
    assert cuerpo["por_nivel"]["1"] == 2
    assert cuerpo["por_nivel"]["3"] == 1


def test_listar_cola_respeta_el_orden_de_prioridad(cliente):
    registrar(cliente, nombre="rutina", nivel_prioridad=5)
    registrar(cliente, nombre="urgente", nivel_prioridad=1)
    r = cliente.get("/cola")
    nombres = [s["nombre"] for s in r.json()["pendientes"]]
    assert nombres == ["urgente", "rutina"]


# -- errores ------------------------------------------------------------------

def test_siguiente_con_cola_vacia_da_404(cliente):
    r = cliente.get("/siguiente")
    assert r.status_code == 404


def test_atender_con_cola_vacia_da_404(cliente):
    r = cliente.post("/atender")
    assert r.status_code == 404


def test_sacar_id_inexistente_da_404(cliente):
    r = cliente.delete("/cola/999")
    assert r.status_code == 404


@pytest.mark.parametrize("nivel", [0, 6, -1])
def test_registrar_nivel_fuera_de_rango_da_422(cliente, nivel):
    r = registrar(cliente, nivel_prioridad=nivel)
    assert r.status_code == 422


def test_registrar_tipo_invalido_da_422(cliente):
    r = registrar(cliente, tipo="ambulancia")
    assert r.status_code == 422


def test_registrar_nombre_vacio_da_422(cliente):
    r = registrar(cliente, nombre="")
    assert r.status_code == 422


def test_raiz_lista_los_endpoints(cliente):
    r = cliente.get("/")
    assert r.status_code == 200
    assert "POST /registrar" in r.json()["endpoints"]
