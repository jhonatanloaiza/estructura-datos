"""Partes C y D: convierte `resultados.csv` en las cifras de los informes.

Todo número de `comparacion.md` y `decision.md` sale de aquí, para que ninguno
dependa de una cuenta a mano.

Ejecutar:  python analisis.py          (salida capturada en salida_analisis.txt)
"""

import csv
import math
import statistics
from pathlib import Path

CARPETA = Path(__file__).parent
TAMANOS = [1_000, 10_000, 80_000, 200_000]
EPOCAS = {"vacaciones": 5, "normal": 50, "exámenes": 300}

# Criterios fijados en prediccion.md antes de medir.
CRITERIOS = {
    "obtener": "O(1)",
    "insertar_final": "O(1)",
    "buscar_binaria": "O(log n)",
    "insertar_inicio": "O(n)",
    "insertar_ordenado": "O(n)",
    "buscar_lineal": "O(n)",
    "buscar_lineal_fallo": "O(n)",
}


def es(x, decimales=1):
    """Número con formato colombiano: 1.234,5"""
    texto = f"{x:,.{decimales}f}"
    return texto.replace(",", "_").replace(".", ",").replace("_", ".")


def leer(archivo="resultados.csv"):
    """{(operacion, n): tiempos por repetición en µs}"""
    tabla = {}
    with (CARPETA / archivo).open(encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            reps = [float(v) for k, v in fila.items() if k.startswith("rep_")]
            tabla[fila["operacion"], int(fila["n"])] = reps
    return tabla


def mediana(tabla, operacion, n):
    return statistics.median(tabla[operacion, n])


def pendiente(tabla, operacion):
    """Pendiente log-log entre el catálogo más pequeño y el más grande."""
    a, b = TAMANOS[0], TAMANOS[-1]
    subida = math.log(mediana(tabla, operacion, b) / mediana(tabla, operacion, a))
    return subida / math.log(b / a)


def crecimiento(tabla, operacion):
    return mediana(tabla, operacion, TAMANOS[-1]) / mediana(tabla, operacion, TAMANOS[0])


def coincide(clase, tabla, operacion):
    if clase == "O(n)":
        return 0.9 <= pendiente(tabla, operacion) <= 1.1
    if clase == "O(1)":
        return crecimiento(tabla, operacion) < 1.5
    return 1.4 <= crecimiento(tabla, operacion) <= 2.1


def costo_ordenado(tabla, n, s, insercion="insertar_ordenado"):
    return s * mediana(tabla, "buscar_binaria", n) + mediana(tabla, insercion, n)


def costo_desordenado(tabla, n, s, busqueda="buscar_lineal"):
    return s * mediana(tabla, busqueda, n) + mediana(tabla, "insertar_final", n)


def equilibrio(tabla, n, insercion="insertar_ordenado", busqueda="buscar_lineal"):
    """Búsquedas por inserción en las que los dos catálogos cuestan lo mismo."""
    extra_al_insertar = mediana(tabla, insercion, n) - mediana(tabla, "insertar_final", n)
    ahorro_al_buscar = mediana(tabla, busqueda, n) - mediana(tabla, "buscar_binaria", n)
    return extra_al_insertar / ahorro_al_buscar


def equilibrio_rango(tabla, n):
    """Equilibrio con los cuartiles que más lo bajan y más lo suben."""
    q1_ins, _, q3_ins = statistics.quantiles(tabla["insertar_ordenado", n], n=4)
    q1_lin, _, q3_lin = statistics.quantiles(tabla["buscar_lineal", n], n=4)
    fin = mediana(tabla, "insertar_final", n)
    binaria = mediana(tabla, "buscar_binaria", n)
    return (q1_ins - fin) / (q3_lin - binaria), (q3_ins - fin) / (q1_lin - binaria)


def fraccion_para_cambiar(tabla, n, s):
    """Parte del catálogo que debería recorrer en promedio una búsqueda lineal
    para que el desordenado empate con `s` búsquedas por inserción.

    Hoy recorre la mitad, y su costo es proporcional a lo que recorre.
    """
    extra_al_insertar = mediana(tabla, "insertar_ordenado", n) - mediana(tabla, "insertar_final", n)
    lineal_de_empate = mediana(tabla, "buscar_binaria", n) + extra_al_insertar / s
    return 0.5 * lineal_de_empate / mediana(tabla, "buscar_lineal", n)


def imprimir_comparacion(tabla):
    print("PARTE C. MEDIANAS POR OPERACIÓN (µs)\n")
    print("| Operación | " + " | ".join(es(n, 0) for n in TAMANOS) + " |")
    print("|---|" + "---:|" * len(TAMANOS))
    operaciones = sorted({op for op, _ in tabla})
    for op in operaciones:
        print(f"| `{op}` | " + " | ".join(es(mediana(tabla, op, n), 3) for n in TAMANOS) + " |")

    print("\nPARTE C. FORMA MEDIDA CONTRA LO PREDICHO\n")
    print("| Operación | Clase | Crecimiento 1.000→200.000 | Pendiente log-log | ¿Coincide? |")
    print("|---|---|---:|---:|---|")
    for op, clase in CRITERIOS.items():
        marca = "sí" if coincide(clase, tabla, op) else "no"
        print(f"| `{op}` | {clase} | ×{es(crecimiento(tabla, op), 2)} "
              f"| {es(pendiente(tabla, op), 3)} | {marca} |")

    print("\nPARTE C. COSTO POR ELEMENTO (ns)\n")
    print("| Elemento tocado | Memoria | " + " | ".join(es(n, 0) for n in TAMANOS) + " |")
    print("|---|---|" + "---:|" * len(TAMANOS))
    for nombre, memoria, op in COSTOS_POR_ELEMENTO:
        valores = [mediana(tabla, op, n) * 1000 / n for n in TAMANOS]
        print(f"| {nombre} | {memoria} | " + " | ".join(es(v, 1) for v in valores) + " |")


COSTOS_POR_ELEMENTO = [
    ("Mover", "dispersa", "insertar_inicio"),
    ("Mover", "contigua", "insertar_inicio_contiguo"),
    ("Comparar", "dispersa", "buscar_lineal_fallo_disperso"),
    ("Comparar", "contigua", "buscar_lineal_fallo"),
]


def imprimir_decision(tabla):
    print("\nPARTE D. COSTO TOTAL DE s BÚSQUEDAS + 1 INSERCIÓN (ms)\n")
    print("| Época | s | n | Ordenado | Desordenado | Gana | Ventaja |")
    print("|---|---:|---:|---:|---:|---|---:|")
    for epoca, s in EPOCAS.items():
        for n in TAMANOS[2:]:
            orden = costo_ordenado(tabla, n, s) / 1000
            desorden = costo_desordenado(tabla, n, s) / 1000
            gana = "ordenado" if orden < desorden else "desordenado"
            ventaja = max(orden, desorden) / min(orden, desorden)
            print(f"| {epoca} | {s} | {es(n, 0)} | {es(orden, 2)} | {es(desorden, 2)} "
                  f"| {gana} | ×{es(ventaja, 1)} |")

    print("\nPARTE D. PUNTO DE EQUILIBRIO (búsquedas por inserción)\n")
    print("| n | s* | Rango por cuartiles | s* en la corrida descartada |")
    print("|---:|---:|---|---:|")
    descartada = leer("corrida_descartada.csv")
    for n in TAMANOS:
        bajo, alto = equilibrio_rango(tabla, n)
        print(f"| {es(n, 0)} | {es(equilibrio(tabla, n), 2)} "
              f"| {es(bajo, 2)} a {es(alto, 2)} | {es(equilibrio(descartada, n), 2)} |")

    print("\nPARTE D. SENSIBILIDAD DEL EQUILIBRIO\n")
    print("| Supuesto | s* con 80.000 | s* con 200.000 |")
    print("|---|---:|---:|")
    supuestos = [
        ("Caso base: acierta, y el libro nuevo cae en cualquier parte",
         lambda n: equilibrio(tabla, n)),
        ("Toda búsqueda falla (recorre el catálogo entero)",
         lambda n: equilibrio(tabla, n, busqueda="buscar_lineal_fallo")),
        ("Todo libro nuevo cae al inicio (peor caso del ordenado)",
         lambda n: equilibrio(tabla, n, insercion="insertar_inicio")),
    ]
    for nombre, calculo in supuestos:
        print(f"| {nombre} | {es(calculo(80_000), 2)} | {es(calculo(200_000), 2)} |")

    print("\nPARTE D. QUÉ TENDRÍA QUE PASAR PARA QUE VACACIONES CAMBIE\n")
    for n in TAMANOS[2:]:
        fraccion = fraccion_para_cambiar(tabla, n, EPOCAS["vacaciones"])
        print(f"n = {es(n, 0)}: la búsqueda lineal tendría que parar, en promedio, "
              f"en el primer {es(fraccion * 100, 1)} % del catálogo (hoy: 50 %).")

    print("\nPARTE D. HOY CONTRA EL AÑO QUE VIENE (s = 50)\n")
    hoy = costo_desordenado(tabla, 80_000, 50) / 1000
    sin_cambio = costo_desordenado(tabla, 200_000, 50) / 1000
    con_cambio = costo_ordenado(tabla, 200_000, 50) / 1000
    print(f"Hoy, 80.000 desordenado:           {es(hoy, 2)} ms")
    print(f"Sin cambiar, 200.000 desordenado:  {es(sin_cambio, 2)} ms (×{es(sin_cambio / hoy, 1)})")
    print(f"Ordenando, 200.000 ordenado:       {es(con_cambio, 2)} ms (÷{es(hoy / con_cambio, 1)})")


def main():
    tabla = leer()
    imprimir_comparacion(tabla)
    imprimir_decision(tabla)


if __name__ == "__main__":
    main()
