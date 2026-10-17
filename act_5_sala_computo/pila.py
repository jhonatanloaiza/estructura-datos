"""Parte D — Pila (LIFO), con nodos enlazados a mano.

Existe solo para la comparación de `recorridos.md`: mismo algoritmo de
recorrido por niveles que con `Cola`, cambiando únicamente la estructura, así
la diferencia de salida es atribuible solo a eso (`plan.md` §6). No es un
entregable por sí sola.
"""


class PilaVaciaError(Exception):
    """Se pidió `desapilar()` o `tope()` con la pila vacía."""


class _Nodo:
    __slots__ = ("dato", "siguiente")

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class Pila:
    """LIFO: lo último que entra es lo primero que sale."""

    def __init__(self):
        self._tope = None
        self._n = 0

    def __len__(self):
        return self._n

    def esta_vacia(self) -> bool:
        return self._n == 0

    def apilar(self, dato) -> None:
        self._tope = _Nodo(dato, self._tope)
        self._n += 1

    def desapilar(self):
        if self.esta_vacia():
            raise PilaVaciaError("la pila está vacía")
        nodo = self._tope
        self._tope = nodo.siguiente
        nodo.siguiente = None
        self._n -= 1
        return nodo.dato

    def tope(self):
        if self.esta_vacia():
            raise PilaVaciaError("la pila está vacía")
        return self._tope.dato
