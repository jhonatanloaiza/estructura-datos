"""TAD Lista de reproducción, implementación con nodos enlazados.

Cada canción vive en un `Nodo` que sabe cuál es el siguiente. La lista guarda
la cabeza, la cola (para agregar al final en O(1)) y el tamaño. No hay ninguna
`list` de Python por dentro.

Contrato: ver `spec.md`. Es el mismo que el de `ListaArreglo`.
"""


class Nodo:
    __slots__ = ("dato", "siguiente")

    def __init__(self, dato, siguiente=None):
        self.dato = dato
        self.siguiente = siguiente


class ListaEnlazada:
    def __init__(self):
        self._cabeza = None
        self._cola = None
        self._n = 0

    # -- consulta -----------------------------------------------------------

    def __len__(self):
        return self._n

    def esta_vacia(self):
        return self._n == 0

    def obtener(self, i):
        self._validar_indice(i)
        return self._nodo_en(i).dato

    def __iter__(self):
        nodo = self._cabeza
        while nodo is not None:
            yield nodo.dato
            nodo = nodo.siguiente

    # -- modificación -------------------------------------------------------

    def insertar_al_principio(self, x):
        # Primero el nodo nuevo apunta a la cabeza vieja; recién después la
        # cabeza pasa a ser el nodo nuevo. Al revés se pierde la lista.
        nuevo = Nodo(x, self._cabeza)
        self._cabeza = nuevo
        if self._cola is None:
            self._cola = nuevo
        self._n += 1

    def agregar(self, x):
        nuevo = Nodo(x)
        if self._cola is None:
            self._cabeza = nuevo
        else:
            self._cola.siguiente = nuevo
        self._cola = nuevo
        self._n += 1

    def borrar(self, i):
        self._validar_indice(i)
        if i == 0:
            victima = self._cabeza
            self._cabeza = victima.siguiente
            if self._cabeza is None:
                self._cola = None
        else:
            anterior = self._nodo_en(i - 1)
            victima = anterior.siguiente
            anterior.siguiente = victima.siguiente
            if victima is self._cola:
                self._cola = anterior
        victima.siguiente = None
        self._n -= 1
        return victima.dato

    # -- internos -----------------------------------------------------------

    def _validar_indice(self, i):
        if isinstance(i, bool) or not isinstance(i, int):
            raise TypeError("el índice debe ser un entero")
        if i < 0 or i >= self._n:
            raise IndexError(f"índice {i} fuera de rango (tamaño {self._n})")

    def _nodo_en(self, i):
        nodo = self._cabeza
        for _ in range(i):
            nodo = nodo.siguiente
        return nodo
