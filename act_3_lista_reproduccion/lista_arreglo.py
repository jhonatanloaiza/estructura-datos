"""TAD Lista de reproducción, implementación con arreglo (actividad 2).

Los datos viven en un bloque contiguo de posiciones. Cuando se llena, se crea
un bloque del doble de tamaño y se copian los elementos.

El desplazamiento de elementos se hace con bucles explícitos (no con
`list.insert` / `list.pop`) para que el costo medido refleje el algoritmo y no
la velocidad de una rutina en C.

Contrato: ver `spec.md`.
"""

_CAPACIDAD_INICIAL = 4


class ListaArreglo:
    def __init__(self):
        self._datos = [None] * _CAPACIDAD_INICIAL
        self._n = 0

    # -- consulta -----------------------------------------------------------

    def __len__(self):
        return self._n

    def esta_vacia(self):
        return self._n == 0

    def obtener(self, i):
        self._validar_indice(i)
        return self._datos[i]

    def __iter__(self):
        for i in range(self._n):
            yield self._datos[i]

    # -- modificación -------------------------------------------------------

    def insertar_al_principio(self, x):
        self._asegurar_espacio()
        for i in range(self._n, 0, -1):
            self._datos[i] = self._datos[i - 1]
        self._datos[0] = x
        self._n += 1

    def agregar(self, x):
        self._asegurar_espacio()
        self._datos[self._n] = x
        self._n += 1

    def borrar(self, i):
        self._validar_indice(i)
        borrado = self._datos[i]
        for j in range(i, self._n - 1):
            self._datos[j] = self._datos[j + 1]
        self._datos[self._n - 1] = None
        self._n -= 1
        return borrado

    # -- internos -----------------------------------------------------------

    def _validar_indice(self, i):
        if isinstance(i, bool) or not isinstance(i, int):
            raise TypeError("el índice debe ser un entero")
        if i < 0 or i >= self._n:
            raise IndexError(f"índice {i} fuera de rango (tamaño {self._n})")

    def _asegurar_espacio(self):
        if self._n < len(self._datos):
            return
        nuevo = [None] * (2 * len(self._datos))
        for i in range(self._n):
            nuevo[i] = self._datos[i]
        self._datos = nuevo
