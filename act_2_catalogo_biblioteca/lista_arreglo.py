"""TAD ListaArreglo para el catálogo de la biblioteca (Parte A).

Los datos viven en un bloque contiguo de posiciones. Cuando se llena, se crea
un bloque del doble de tamaño y se copian los elementos.

De la `list` de Python solo se usa lo que tendría un arreglo de verdad: crear
el bloque con `[None] * capacidad` y leer o escribir una posición con `[]`.
El desplazamiento y las búsquedas son bucles explícitos (nada de `insert`,
`append`, `index`, `sort`, `bisect`, `in` ni rebanadas) para que el costo
medido en la Parte C refleje el algoritmo y no la velocidad de una rutina en C.

`buscar_binaria` e `insertar_ordenado` exigen que la lista ya esté ordenada de
menor a mayor. No se comprueba: revisarlo recorrería toda la lista en cada
llamada y destruiría justo la ventaja que estas operaciones quieren dar.

Complejidad y conteo de operaciones: ver `prediccion.md`.
"""

_CAPACIDAD_INICIAL = 4

NO_ENCONTRADO = -1


class ListaArreglo:
    def __init__(self, capacidad=_CAPACIDAD_INICIAL):
        if capacidad < 1:
            raise ValueError("la capacidad debe ser al menos 1")
        self._datos = [None] * capacidad
        self._n = 0

    # -- consulta -----------------------------------------------------------

    def __len__(self):
        return self._n

    def esta_vacia(self):
        return self._n == 0

    def obtener(self, pos):
        self._validar_pos(pos, self._n)
        return self._datos[pos]

    def __iter__(self):
        for i in range(self._n):
            yield self._datos[i]

    # -- búsqueda -----------------------------------------------------------

    def buscar_lineal(self, x):
        """Posición de la primera aparición de `x`, o NO_ENCONTRADO."""
        for i in range(self._n):
            if self._datos[i] == x:
                return i
        return NO_ENCONTRADO

    def buscar_binaria(self, x):
        """Posición de la primera aparición de `x`, o NO_ENCONTRADO.

        Requiere la lista ordenada.
        """
        pos = self._cota_inferior(x)
        if pos < self._n and self._datos[pos] == x:
            return pos
        return NO_ENCONTRADO

    # -- modificación -------------------------------------------------------

    def insertar(self, pos, x):
        """Pone `x` en `pos`; `pos == len(lista)` agrega al final."""
        self._validar_pos(pos, self._n + 1)
        self._asegurar_espacio()
        for i in range(self._n, pos, -1):
            self._datos[i] = self._datos[i - 1]
        self._datos[pos] = x
        self._n += 1

    def insertar_ordenado(self, x):
        """Pone `x` en su sitio. Requiere la lista ordenada."""
        self.insertar(self._cota_inferior(x), x)

    # -- internos -----------------------------------------------------------

    def _cota_inferior(self, x):
        """Primera posición cuyo elemento no es menor que `x` (o `n` si no hay)."""
        bajo, alto = 0, self._n
        while bajo < alto:
            medio = (bajo + alto) // 2
            if self._datos[medio] < x:
                bajo = medio + 1
            else:
                alto = medio
        return bajo

    def _validar_pos(self, pos, limite):
        if isinstance(pos, bool) or not isinstance(pos, int):
            raise TypeError("la posición debe ser un entero")
        if pos < 0 or pos >= limite:
            raise IndexError(f"posición {pos} fuera de rango (tamaño {self._n})")

    def _asegurar_espacio(self):
        if self._n < len(self._datos):
            return
        nuevo = [None] * (2 * len(self._datos))
        for i in range(self._n):
            nuevo[i] = self._datos[i]
        self._datos = nuevo
