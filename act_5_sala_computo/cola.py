"""Parte A — Cola simple (FIFO), con nodos enlazados a mano.

Nada de `collections.deque` ni de usar una `list` de Python como
almacenamiento (`constitucion.md` §2): es el mismo criterio que en la
actividad anterior se aplicó a `ListaEnlazada`.

Es la pieza que reutilizan `cola_prioridad.py` (una por cada nivel) y
`arbol_carpetas.py` (para el recorrido por niveles): ninguna de las dos sabe
cómo está hecha por dentro, solo usan `encolar`/`decolar`/`esta_vacia`
(`spec.md` RNF3).
"""


class ColaVaciaError(Exception):
    """Se pidió `decolar()` o `frente()` con la cola vacía."""


class _Nodo:
    __slots__ = ("dato", "siguiente")

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class Cola:
    """FIFO: lo primero que entra es lo primero que sale."""

    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._n = 0

    def __len__(self):
        return self._n

    def esta_vacia(self) -> bool:
        return self._n == 0

    def encolar(self, dato) -> None:
        nuevo = _Nodo(dato)
        if self._cola is None:
            self._cabeza = nuevo
        else:
            self._cola.siguiente = nuevo
        self._cola = nuevo
        self._n += 1

    def decolar(self):
        if self.esta_vacia():
            raise ColaVaciaError("la cola está vacía")
        nodo = self._cabeza
        self._cabeza = nodo.siguiente
        if self._cabeza is None:
            self._cola = None
        nodo.siguiente = None
        self._n -= 1
        return nodo.dato

    def frente(self):
        """Mira el siguiente a salir, sin retirarlo."""
        if self.esta_vacia():
            raise ColaVaciaError("la cola está vacía")
        return self._cabeza.dato
