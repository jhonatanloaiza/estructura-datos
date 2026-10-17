"""Pruebas de `arbol_carpetas.py`: las tres consultas, con los casos límite
de spec.md §7 (árbol vacío, un solo nodo, empate de profundidad).
"""

from arbol_carpetas import (
    Carpeta,
    contar_entregas,
    ruta_mas_profunda,
    listar_por_niveles,
    recorrer_por_niveles_con_pila,
)


def arbol_de_ejemplo():
    """El mismo árbol que se dibuja en recorridos.md.

    Ingenieria (fac)
    ├── Sistemas (prog)
    │   ├── EDD (curso, 2 entregas)
    │   │   └── 2026-1 (semestre, 3 entregas)
    │   └── BD (curso, 1 entrega)
    └── Industrial (prog)
        └── Procesos (curso)
            └── 2025-2 (semestre, 4 entregas)
    """
    semestre_edd = Carpeta("2026-1", entregas=3)
    curso_edd = Carpeta("EDD", entregas=2, hijos=[semestre_edd])
    curso_bd = Carpeta("BD", entregas=1)
    sistemas = Carpeta("Sistemas", hijos=[curso_edd, curso_bd])

    semestre_procesos = Carpeta("2025-2", entregas=4)
    curso_procesos = Carpeta("Procesos", hijos=[semestre_procesos])
    industrial = Carpeta("Industrial", hijos=[curso_procesos])

    return Carpeta("Ingenieria", hijos=[sistemas, industrial])


# -- contar_entregas ------------------------------------------------------------

def test_contar_entregas_suma_todo_el_arbol():
    assert contar_entregas(arbol_de_ejemplo()) == 3 + 2 + 1 + 4  # = 10


def test_contar_entregas_arbol_vacio_es_cero():
    assert contar_entregas(None) == 0


def test_contar_entregas_nodo_sin_hijos_es_solo_lo_propio():
    hoja = Carpeta("2026-1", entregas=5)
    assert contar_entregas(hoja) == 5


def test_contar_entregas_desde_un_nodo_intermedio_no_cuenta_el_resto_del_arbol():
    raiz = arbol_de_ejemplo()
    sistemas = raiz.hijos[0]
    assert contar_entregas(sistemas) == 3 + 2 + 1  # no incluye Industrial


# -- ruta_mas_profunda -----------------------------------------------------------

def test_ruta_mas_profunda_sigue_la_rama_mas_larga():
    raiz = arbol_de_ejemplo()
    assert ruta_mas_profunda(raiz) == ["Ingenieria", "Sistemas", "EDD", "2026-1"]


def test_ruta_mas_profunda_arbol_vacio_es_lista_vacia():
    assert ruta_mas_profunda(None) == []


def test_ruta_mas_profunda_un_solo_nodo():
    assert ruta_mas_profunda(Carpeta("Ingenieria")) == ["Ingenieria"]


def test_ruta_mas_profunda_empate_toma_la_primera_rama():
    izquierda = Carpeta("izq", hijos=[Carpeta("izq-hijo")])
    derecha = Carpeta("der", hijos=[Carpeta("der-hijo")])
    raiz = Carpeta("raiz", hijos=[izquierda, derecha])
    assert ruta_mas_profunda(raiz) == ["raiz", "izq", "izq-hijo"]


# -- listar_por_niveles -----------------------------------------------------------

def test_listar_por_niveles_agrupa_por_profundidad():
    raiz = arbol_de_ejemplo()
    niveles = listar_por_niveles(raiz)
    assert niveles == [
        ["Ingenieria"],
        ["Sistemas", "Industrial"],
        ["EDD", "BD", "Procesos"],
        ["2026-1", "2025-2"],
    ]


def test_listar_por_niveles_arbol_vacio_es_lista_vacia():
    assert listar_por_niveles(None) == []


def test_listar_por_niveles_un_solo_nodo():
    assert listar_por_niveles(Carpeta("Ingenieria")) == [["Ingenieria"]]


# -- la comparación de la parte D --------------------------------------------------

def test_recorrido_con_pila_visita_los_mismos_nodos_que_con_cola():
    raiz = arbol_de_ejemplo()
    nombres_cola = {n for nivel in listar_por_niveles(raiz) for n in nivel}
    nombres_pila = {nombre for nombre, _ in recorrer_por_niveles_con_pila(raiz)}
    assert nombres_cola == nombres_pila


def test_recorrido_con_pila_da_un_orden_distinto_al_de_la_cola():
    raiz = arbol_de_ejemplo()
    orden_cola = [n for nivel in listar_por_niveles(raiz) for n in nivel]
    orden_pila = [nombre for nombre, _ in recorrer_por_niveles_con_pila(raiz)]
    assert orden_cola != orden_pila


def test_recorrido_con_pila_arbol_vacio_es_lista_vacia():
    assert recorrer_por_niveles_con_pila(None) == []
