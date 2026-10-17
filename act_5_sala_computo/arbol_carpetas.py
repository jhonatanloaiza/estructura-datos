"""Parte C y D — El árbol de carpetas del servidor de entregas.

Carpetas anidadas por facultad, programa, curso y semestre. Cada `Carpeta`
puede tener entregas propias (archivos que viven directamente en ella) y
subcarpetas (`hijos`), que es una `list` de Python — permitido: el objeto de
estudio de esta actividad es la recursión y la cola, no cómo se guardan los
hijos de un nodo (`constitucion.md` §2).

`contar_entregas` y `ruta_mas_profunda` son recursivas (RF6, RF7).
`listar_por_niveles` es iterativa, con la `Cola` de la Parte A (RF8).
`recorrer_por_niveles_con_pila` existe solo para la comparación de la Parte D
(`recorridos.md`): mismo algoritmo, pero con `Pila` en vez de `Cola`.
"""

from cola import Cola
from pila import Pila


class Carpeta:
    def __init__(self, nombre, entregas=0, hijos=None):
        self.nombre = nombre
        self.entregas = entregas
        self.hijos = hijos if hijos is not None else []

    def __repr__(self):
        return f"Carpeta({self.nombre!r}, entregas={self.entregas}, hijos={len(self.hijos)})"


def contar_entregas(carpeta: "Carpeta | None") -> int:
    """Total de entregas bajo `carpeta`, incluida ella misma (RF6).

    Caso base: `carpeta is None` (árbol vacío, o "no hay más hijos" cuando se
    llama sobre un hijo que no existe) aporta 0. Un nodo sin hijos simplemente
    no suma nada en el bucle y devuelve sus propias entregas.
    """
    if carpeta is None:
        return 0
    total = carpeta.entregas
    for hijo in carpeta.hijos:
        total += contar_entregas(hijo)
    return total


def ruta_mas_profunda(carpeta: "Carpeta | None") -> list:
    """Lista de nombres desde `carpeta` hasta el nodo más profundo de su
    rama más larga (RF7).

    Caso base: `carpeta is None` devuelve `[]` (árbol vacío). Un nodo sin
    hijos devuelve `[su_nombre]` porque el bucle no encuentra ninguna rama
    que lo supere.

    Desempate (spec.md HU5): si dos ramas llegan a la misma profundidad
    máxima, se conserva la primera encontrada en el orden de `hijos` — solo
    se reemplaza `mejor` cuando una candidata es estrictamente más larga.
    """
    if carpeta is None:
        return []
    mejor = [carpeta.nombre]
    for hijo in carpeta.hijos:
        candidata = [carpeta.nombre] + ruta_mas_profunda(hijo)
        if len(candidata) > len(mejor):
            mejor = candidata
    return mejor


def listar_por_niveles(carpeta: "Carpeta | None") -> list:
    """Nombres agrupados por nivel de profundidad, nivel 0 = la raíz (RF8).

    Iterativo, con la `Cola` de la Parte A: se encola `(nodo, nivel)`, se
    decola, se registra el nombre en `niveles[nivel]`, y se encolan sus hijos
    con `nivel + 1`. Árbol vacío devuelve `[]` (no es un error).
    """
    niveles = []
    if carpeta is None:
        return niveles
    cola = Cola()
    cola.encolar((carpeta, 0))
    while not cola.esta_vacia():
        nodo, nivel = cola.decolar()
        if nivel == len(niveles):
            niveles.append([])
        niveles[nivel].append(nodo.nombre)
        for hijo in nodo.hijos:
            cola.encolar((hijo, nivel + 1))
    return niveles


def recorrer_por_niveles_con_pila(carpeta: "Carpeta | None") -> list:
    """El mismo algoritmo que `listar_por_niveles`, cambiando `Cola` por
    `Pila` (Parte D, solo para comparar en `recorridos.md`). No es un
    recorrido por niveles correcto: se incluye precisamente para mostrar en
    qué se diferencia de uno.
    """
    visitados = []
    if carpeta is None:
        return visitados
    pila = Pila()
    pila.apilar((carpeta, 0))
    while not pila.esta_vacia():
        nodo, nivel = pila.desapilar()
        visitados.append((nodo.nombre, nivel))
        for hijo in nodo.hijos:
            pila.apilar((hijo, nivel + 1))
    return visitados
