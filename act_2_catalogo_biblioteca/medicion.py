"""Parte C: mide las operaciones de ListaArreglo con `timeit`.

Cada operación se repite REPETICIONES veces por tamaño de catálogo y cuenta la
mediana. Una repetición es un lote de operaciones cronometrado de una sola vez;
el tiempo guardado en `resultados.csv` es por operación, en microsegundos.

Decisiones que afectan a lo que se mide:

- Se mide por rondas: en cada una pasan todos los casos, en orden al azar. Medir
  cada tamaño de corrido hacía que una deriva del computador (frecuencia del
  procesador, batería) se confundiera con el efecto de n.
- Los registros son ISBN-13 de texto. Un libro nuevo cae en cualquier parte del
  catálogo: el ISBN no tiene relación con el orden en que llegan los libros.
- Los dos catálogos comparten los mismos objetos, creados en orden de llegada.
  Así el desordenado recorre la memoria de corrido y el ordenado salta por toda
  ella, igual que en un catálogo real. Es lo menos favorable para el ordenado.
- `buscar_lineal` e `insertar_final` usan el catálogo desordenado (es lo que hace
  ese escenario); todo lo demás, el ordenado.
- Las búsquedas buscan registros al azar, distintos en cada repetición, para que
  un sorteo con suerte no se repita en todas. `buscar_lineal_fallo` busca
  registros que no están.
- Las operaciones que cambian el catálogo parten de una copia nueva en cada
  repetición (la copia queda fuera del cronómetro) y su lote no pasa del 5 % de
  n, para que n siga siendo prácticamente n durante toda la medición.
- `insertar_final` parte de un bloque lleno e inserta n registros: paga
  exactamente una duplicación, así que su tiempo ya es el costo amortizado.
- `insertar_inicio_contiguo` y `buscar_lineal_fallo_disperso` son controles: la
  misma operación con la memoria dispuesta al revés. Sirven para comprobar si la
  disposición en memoria explica las diferencias con la predicción.

Ejecutar:  python medicion.py
"""

import csv
import random
import statistics
import timeit
from pathlib import Path

from lista_arreglo import ListaArreglo

TAMANOS = [1_000, 10_000, 80_000, 200_000]
REPETICIONES = 11         # rondas; se toma la mediana
SEMILLA = 2026
ARCHIVO = Path(__file__).with_name("resultados.csv")


def construir(registros, capacidad):
    lista = ListaArreglo(capacidad)
    for r in registros:
        lista.insertar(len(lista), r)
    return lista


def _isbn(numero):
    return f"978{numero:010d}"


class Catalogo:
    """Los mismos n registros en los dos órdenes que compara la actividad."""

    def __init__(self, n, rng):
        self.n = n
        self.rng = rng
        turnos = list(range(n))
        rng.shuffle(turnos)
        self.por_llegada = [_isbn(2 * t) for t in turnos]
        # Cada registro va a la casilla de su número: ordena sin usar `sort`.
        self.por_clave = [None] * n
        for t, isbn in zip(turnos, self.por_llegada):
            self.por_clave[t] = isbn
        self.desordenado = construir(self.por_llegada, n)
        self.ordenado = construir(self.por_clave, n)

    def existentes(self, cuantos):
        return [self.por_clave[self.rng.randrange(self.n)] for _ in range(cuantos)]

    def nuevos(self, cuantos):
        """ISBN impares: repartidos por todo el catálogo y ninguno está en él."""
        return [_isbn(2 * self.rng.randrange(self.n) + 1) for _ in range(cuantos)]


def _lote_insercion(n):
    return min(200, n // 20)


# Cada medidor devuelve (preparar, ejecutar, lote). `preparar` corre antes de
# cada repetición, fuera del cronómetro, y entrega los argumentos de `ejecutar`.


def obtener(cat):
    lote = 100_000

    def preparar():
        return [cat.rng.randrange(cat.n) for _ in range(lote)],

    def ejecutar(posiciones):
        for pos in posiciones:
            cat.ordenado.obtener(pos)
    return preparar, ejecutar, lote


def insertar_inicio(cat):
    lote = _lote_insercion(cat.n)

    def preparar():
        return construir(cat.por_clave, 2 * cat.n), cat.nuevos(lote)

    def ejecutar(lista, nuevos):
        for x in nuevos:
            lista.insertar(0, x)
    return preparar, ejecutar, lote


def insertar_inicio_contiguo(cat):
    lote = _lote_insercion(cat.n)

    def preparar():
        return construir(cat.por_llegada, 2 * cat.n), cat.nuevos(lote)

    def ejecutar(lista, nuevos):
        for x in nuevos:
            lista.insertar(0, x)
    return preparar, ejecutar, lote


def insertar_final(cat):
    lote = cat.n

    def preparar():
        return construir(cat.por_llegada, cat.n), cat.nuevos(lote)

    def ejecutar(lista, nuevos):
        for x in nuevos:
            lista.insertar(len(lista), x)
    return preparar, ejecutar, lote


def insertar_ordenado(cat):
    lote = _lote_insercion(cat.n)

    def preparar():
        return construir(cat.por_clave, 2 * cat.n), cat.nuevos(lote)

    def ejecutar(lista, nuevos):
        for x in nuevos:
            lista.insertar_ordenado(x)
    return preparar, ejecutar, lote


def buscar_lineal(cat):
    lote = max(400, 2_000_000 // cat.n)

    def preparar():
        return cat.existentes(lote),

    def ejecutar(objetivos):
        for x in objetivos:
            cat.desordenado.buscar_lineal(x)
    return preparar, ejecutar, lote


def buscar_lineal_fallo(cat):
    lote = max(100, 1_000_000 // cat.n)

    def preparar():
        return cat.nuevos(lote),

    def ejecutar(objetivos):
        for x in objetivos:
            cat.desordenado.buscar_lineal(x)
    return preparar, ejecutar, lote


def buscar_lineal_fallo_disperso(cat):
    lote = max(100, 1_000_000 // cat.n)

    def preparar():
        return cat.nuevos(lote),

    def ejecutar(objetivos):
        for x in objetivos:
            cat.ordenado.buscar_lineal(x)
    return preparar, ejecutar, lote


def buscar_binaria(cat):
    lote = 20_000

    def preparar():
        return cat.existentes(lote),

    def ejecutar(objetivos):
        for x in objetivos:
            cat.ordenado.buscar_binaria(x)
    return preparar, ejecutar, lote


MEDIDORES = [
    obtener,
    insertar_inicio,
    insertar_inicio_contiguo,
    insertar_final,
    insertar_ordenado,
    buscar_lineal,
    buscar_lineal_fallo,
    buscar_lineal_fallo_disperso,
    buscar_binaria,
]


def medir(medidor, catalogo):
    """Una repetición: devuelve (lote, tiempo por operación en µs)."""
    preparar, ejecutar, lote = medidor(catalogo)
    argumentos = None

    def setup():
        nonlocal argumentos
        argumentos = preparar()

    def stmt():
        ejecutar(*argumentos)

    return lote, timeit.timeit(stmt, setup, number=1) / lote * 1e6


def main():
    rng = random.Random(SEMILLA)
    catalogos = [Catalogo(n, rng) for n in TAMANOS]
    casos = [(medidor, c) for c in catalogos for medidor in MEDIDORES]
    lotes = {}
    tiempos = {(medidor.__name__, c.n): [] for medidor, c in casos}
    for ronda in range(REPETICIONES):
        rng.shuffle(casos)
        for medidor, catalogo in casos:
            clave = (medidor.__name__, catalogo.n)
            lotes[clave], t = medir(medidor, catalogo)
            tiempos[clave].append(t)
        print(f"Ronda {ronda + 1} de {REPETICIONES} lista", flush=True)

    columnas = ["operacion", "n", "lote", "mediana_us", "minimo_us", "maximo_us"]
    columnas += [f"rep_{i + 1}_us" for i in range(REPETICIONES)]
    filas = []
    for n in TAMANOS:
        for medidor in MEDIDORES:
            clave = (medidor.__name__, n)
            valores = tiempos[clave]
            resumen = (statistics.median(valores), min(valores), max(valores))
            filas.append([*clave, lotes[clave]] + [f"{t:.4f}" for t in (*resumen, *valores)])

    with ARCHIVO.open("w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(columnas)
        escritor.writerows(filas)
    print(f"\nEscrito {ARCHIVO.name}")


if __name__ == "__main__":
    main()
