"""Parte D — Construye el árbol de prueba y captura la salida real de los dos
recorridos (con cola y con pila), para copiarla tal cual a `recorridos.md`
(igual que `nodos_a_mano.py` → `nodos_a_mano.md` en la actividad 3: nada
escrito de memoria, todo verificado ejecutando el código).

Ejecutar:  python generar_recorridos.py
"""

from arbol_carpetas import (
    Carpeta,
    listar_por_niveles,
    recorrer_por_niveles_con_pila,
)


def construir_arbol_de_prueba():
    """
    Ingenieria
    ├── Sistemas
    │   ├── EDD (2 entregas)
    │   │   └── 2026-1 (3 entregas)
    │   └── BD (1 entrega)
    └── Industrial
        └── Procesos
            └── 2025-2 (4 entregas)
    """
    semestre_edd = Carpeta("2026-1", entregas=3)
    curso_edd = Carpeta("EDD", entregas=2, hijos=[semestre_edd])
    curso_bd = Carpeta("BD", entregas=1)
    sistemas = Carpeta("Sistemas", hijos=[curso_edd, curso_bd])

    semestre_procesos = Carpeta("2025-2", entregas=4)
    curso_procesos = Carpeta("Procesos", hijos=[semestre_procesos])
    industrial = Carpeta("Industrial", hijos=[curso_procesos])

    return Carpeta("Ingenieria", hijos=[sistemas, industrial])


def main():
    raiz = construir_arbol_de_prueba()

    print("=== Recorrido por niveles, con la Cola de la Parte A ===")
    niveles = listar_por_niveles(raiz)
    for i, nivel in enumerate(niveles):
        print(f"nivel {i}: {nivel}")
    orden_cola = [nombre for nivel in niveles for nombre in nivel]
    print("orden de visita:", orden_cola)

    print()
    print("=== El mismo recorrido, cambiando la Cola por una Pila ===")
    visitas = recorrer_por_niveles_con_pila(raiz)
    for nombre, nivel in visitas:
        print(f"  visita: {nombre!r} (nivel {nivel})")
    orden_pila = [nombre for nombre, _ in visitas]
    print("orden de visita:", orden_pila)

    print()
    print("=== Comparación ===")
    print("orden con cola:", orden_cola)
    print("orden con pila:", orden_pila)
    print("¿mismo conjunto de nodos?", set(orden_cola) == set(orden_pila))
    print("¿mismo orden?", orden_cola == orden_pila)


if __name__ == "__main__":
    main()
