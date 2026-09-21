"""Parte D: mide las cuatro operaciones de la emisora en las dos estructuras.

Lista de 5.000 canciones. Cada operación se mide sobre una lista recién
construida, se repite varias veces y se reporta la mediana. Luego se calcula el
costo de un día con las frecuencias reales y el punto de quiebre.

Ejecutar:  python benchmark.py
"""

import random
import statistics
import time

from lista_arreglo import ListaArreglo
from lista_enlazada import ListaEnlazada

N = 5000
REPETICIONES = 7          # corridas por operación; se toma la mediana
FRECUENCIAS = {           # veces por día, dadas en el enunciado
    "insertar_principio": 40,
    "recorrer": 3,
    "ir_a_n": 200,
    "borrar_actual": 15,
}
ETIQUETAS = {
    "insertar_principio": "Insertar al principio",
    "recorrer": "Recorrer toda la lista",
    "ir_a_n": "Ir a la canción N",
    "borrar_actual": "Borrar la canción actual",
}
TEORICO = {
    "arreglo": {"insertar_principio": "O(n)", "recorrer": "O(n)",
                "ir_a_n": "O(1)", "borrar_actual": "O(n)"},
    "enlazada": {"insertar_principio": "O(1)", "recorrer": "O(n)",
                 "ir_a_n": "O(n)", "borrar_actual": "O(n)"},
}


def construir(clase, n=N):
    lista = clase()
    for i in range(n):
        lista.agregar(i)
    return lista


def _mediana(clase, preparar, ejecutar, lote):
    """Tiempo por operación (segundos): mediana de varias corridas de `lote` ops."""
    tiempos = []
    for _ in range(REPETICIONES):
        lista = preparar(clase)
        t0 = time.perf_counter()
        ejecutar(lista, lote)
        tiempos.append((time.perf_counter() - t0) / lote)
    return statistics.median(tiempos)


def medir_insertar_principio(clase):
    def ejecutar(lista, lote):
        for i in range(lote):
            lista.insertar_al_principio(i)
    return _mediana(clase, construir, ejecutar, 100)


def medir_recorrer(clase):
    def ejecutar(lista, lote):
        for _ in range(lote):
            for _ in lista:
                pass
    return _mediana(clase, construir, ejecutar, 10)


def medir_ir_a_n(clase):
    # Posiciones repartidas al azar (semilla fija): promedio ~ N/2 saltos.
    rng = random.Random(706132)
    posiciones = [rng.randrange(N) for _ in range(1000)]

    def ejecutar(lista, lote):
        for p in posiciones[:lote]:
            lista.obtener(p)
    return _mediana(clase, construir, ejecutar, 1000)


def medir_borrar_actual(clase):
    # La "canción actual" está en una posición cualquiera: se borra en la mitad.
    def ejecutar(lista, lote):
        for _ in range(lote):
            lista.borrar(len(lista) // 2)
    return _mediana(clase, construir, ejecutar, 100)


MEDIDORES = {
    "insertar_principio": medir_insertar_principio,
    "recorrer": medir_recorrer,
    "ir_a_n": medir_ir_a_n,
    "borrar_actual": medir_borrar_actual,
}
CLASES = {"arreglo": ListaArreglo, "enlazada": ListaEnlazada}


def main():
    medidos = {nombre: {op: m(clase) for op, m in MEDIDORES.items()}
               for nombre, clase in CLASES.items()}

    print(f"Lista de {N} canciones, mediana de {REPETICIONES} corridas.\n")
    print("| Operación | Arreglo (teórico) | Arreglo (medido) "
          "| Enlazada (teórico) | Enlazada (medido) |")
    print("|---|---|---|---|---|")
    for op in MEDIDORES:
        print(f"| {ETIQUETAS[op]} "
              f"| {TEORICO['arreglo'][op]} | {medidos['arreglo'][op] * 1e6:,.2f} µs "
              f"| {TEORICO['enlazada'][op]} | {medidos['enlazada'][op] * 1e6:,.2f} µs |")

    print("\nCosto de un día de emisión (frecuencia × costo medido):\n")
    print("| Operación | Veces/día | Arreglo (ms) | Enlazada (ms) |")
    print("|---|---|---|---|")
    total = {"arreglo": 0.0, "enlazada": 0.0}
    for op, veces in FRECUENCIAS.items():
        a = veces * medidos["arreglo"][op] * 1e3
        e = veces * medidos["enlazada"][op] * 1e3
        total["arreglo"] += a
        total["enlazada"] += e
        print(f"| {ETIQUETAS[op]} | {veces} | {a:,.2f} | {e:,.2f} |")
    print(f"| **Total** | | **{total['arreglo']:,.2f}** | **{total['enlazada']:,.2f}** |")
    print(f"\nRelación enlazada / arreglo: {total['enlazada'] / total['arreglo']:.2f}x")

    # Punto de quiebre: ¿cuántas inserciones al día (con lo demás fijo)
    # igualan el costo de las dos estructuras?
    resto = {n: sum(FRECUENCIAS[op] * medidos[n][op]
                    for op in FRECUENCIAS if op != "insertar_principio")
             for n in CLASES}
    ia, ie = medidos["arreglo"]["insertar_principio"], medidos["enlazada"]["insertar_principio"]
    ins_quiebre = (resto["enlazada"] - resto["arreglo"]) / (ia - ie)
    print(f"\nInserciones/día que igualan ambos costos (resto fijo): {ins_quiebre:,.0f}")

    ga, ge = medidos["arreglo"]["ir_a_n"], medidos["enlazada"]["ir_a_n"]
    resto_g = {n: sum(FRECUENCIAS[op] * medidos[n][op]
                      for op in FRECUENCIAS if op != "ir_a_n")
               for n in CLASES}
    saltos_quiebre = (resto_g["arreglo"] - resto_g["enlazada"]) / (ge - ga)
    print(f"Saltos 'ir a N'/día que igualan ambos costos (resto fijo): {saltos_quiebre:,.0f}")


if __name__ == "__main__":
    main()
