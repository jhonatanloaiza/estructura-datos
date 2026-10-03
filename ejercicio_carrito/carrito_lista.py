"""Implementación del TAD `Carrito` sobre una **lista de pares**.

Contrato: [`spec.md`](spec.md). Es exactamente el mismo que cumple
`carrito_dict.py`; lo único que cambia es la estructura de datos que hay debajo,
y ese es el punto del ejercicio: el mismo archivo de pruebas debe pasar con las
dos, sin tocar una sola línea.

Representación
--------------
Una lista `self._productos` de pares `(clave_normalizada, cantidad)`:

    [("pan", 5), ("leche", 2)]

Los pares son **tuplas**, es decir, inmutables: para cambiar una cantidad no se
modifica el par, se **reemplaza** por uno nuevo en la misma posición. Eso evita
que una referencia guardada por fuera pueda alterar el carrito por detrás.

Por qué esta versión existe
---------------------------
No es la implementación recomendada —el diccionario es mejor para lo que este TAD
hace— pero sirve para dos cosas:

1. **Mostrar el costo de la estructura equivocada.** Aquí *no hay acceso por
   clave*: encontrar un producto obliga a recorrer la lista, así que las tres
   operaciones principales pasan de O(1) a O(n). Con 20 productos da igual; con
   20.000 no.
2. **Mostrar qué trabajo hace el diccionario gratis.** El punto 2 del invariante
   —que no haya dos entradas para el mismo producto— aquí hay que sostenerlo a
   mano: cada `meter` busca primero y solo agrega si no encontró nada. Si esa
   búsqueda se olvidara, el carrito quedaría con dos renglones de "pan" y
   `cuanto_hay` devolvería solo el primero.

Costo de cada operación (`n` = productos distintos en el carrito)
-----------------------------------------------------------------
- `meter`         O(n) — recorre buscando el producto
- `sacar`         O(n) — recorre y, al eliminar, `pop` desplaza el resto
- `cuanto_hay`    O(n) — recorre hasta encontrarlo
- `cuanto_llevo`  O(n) — suma todas las cantidades

Invariante de representación (§5 de `spec.md`)
----------------------------------------------
1. toda cantidad es un entero `>= 1` (el par que llega a 0 se elimina);
2. no hay dos pares con la misma clave;
3. `cuanto_llevo()` es la suma de las cantidades;
4. la lista se crea dentro de `__init__`, así que **pertenece a la instancia** y
   no se comparte con ningún otro carrito (A12; ver `autopsia.md`).

Nota sobre la restricción de la actividad
-----------------------------------------
No se usa `collections.Counter`.
"""


class Carrito:
    """Carrito de compras que cuenta unidades por producto.

    Ejemplo de uso completo (idéntico al de `carrito_dict.py`, porque el
    contrato es el mismo):

        >>> carrito = Carrito()
        >>> carrito.cuanto_llevo()
        0
        >>> carrito.meter("pan", 2)
        >>> carrito.meter("Pan", 3)          # mismo producto: se acumula (A3, A4)
        >>> carrito.cuanto_hay("PAN")
        5
        >>> carrito.meter("leche", 1)
        >>> carrito.cuanto_llevo()
        6
        >>> carrito.sacar("pan", 5)          # al llegar a 0, el producto se va
        >>> carrito.cuanto_hay("pan")
        0
        >>> carrito.cuanto_llevo()
        1
    """

    # -- Construcción ------------------------------------------------------

    def __init__(self) -> None:
        """Crea un carrito vacío.

        La lista se construye **aquí dentro**, en cada llamada. Esa es la línea
        que garantiza la decisión A12: dos cajas distintas obtienen dos listas
        distintas. Escribirla como atributo de clase o como valor por omisión de
        un parámetro reproduciría el error de `autopsia.md`.
        """
        self._productos: list[tuple[str, int]] = []

    # -- Validaciones y búsqueda (privadas) --------------------------------

    @staticmethod
    def _clave(producto: object) -> str:
        """Valida el producto y devuelve la clave normalizada según A3.

        La normalización recorta los extremos, colapsa los espacios internos y
        pasa a minúsculas. No toca las tildes: fue una decisión explícita.

            >>> Carrito._clave("  Pan   Integral ")
            'pan integral'
            >>> Carrito._clave("CAFÉ")
            'café'

        Args:
            producto: nombre del producto tal como lo escribió quien lo usa.

        Returns:
            La clave normalizada con la que se guarda internamente.

        Raises:
            ValueError: si no es una cadena, o si queda vacía al normalizarla.
        """
        if not isinstance(producto, str):
            raise ValueError(
                "El producto debe ser una cadena de texto; se recibió "
                f"{type(producto).__name__}."
            )

        # split() sin argumentos separa por cualquier bloque de espacios y
        # descarta los vacíos, así que recortar y colapsar es una sola operación.
        clave = " ".join(producto.split()).lower()

        if not clave:
            raise ValueError("El nombre del producto no puede estar vacío.")

        return clave

    @staticmethod
    def _validar_cantidad(cantidad: object) -> None:
        """Verifica que la cantidad sea un entero `>= 1` (A6, A7).

        El `isinstance(cantidad, bool)` no sobra: en Python `bool` es subclase de
        `int` y `True == 1`, así que sin ese filtro `meter("pan", True)` metería
        una unidad de pan sin protestar.

        Args:
            cantidad: valor recibido por `meter` o `sacar`.

        Raises:
            ValueError: si no es `int`, si es `bool`, o si es menor que 1.
        """
        if isinstance(cantidad, bool) or not isinstance(cantidad, int):
            raise ValueError(
                "La cantidad debe ser un número entero; se recibió "
                f"{type(cantidad).__name__}."
            )

        if cantidad < 1:
            raise ValueError(
                f"La cantidad debe ser mayor o igual a 1; se recibió {cantidad}."
            )

    def _buscar_indice(self, clave: str) -> int | None:
        """Devuelve la posición del producto en la lista, o `None` si no está.

        Esta es **la búsqueda lineal que el diccionario no necesita hacer**: es
        el motivo de que esta implementación sea O(n) donde la otra es O(1).

        Args:
            clave: clave ya normalizada por `_clave`.

        Returns:
            El índice del par correspondiente, o `None`.

        Complejidad:
            O(n).
        """
        for indice, (nombre, _cantidad) in enumerate(self._productos):
            if nombre == clave:
                return indice

        return None

    # -- Operaciones del contrato ------------------------------------------

    def meter(self, producto: str, cantidad: int) -> None:
        """Agrega `cantidad` unidades de `producto` al carrito.

        Si el producto ya estaba, las cantidades **se acumulan** (A4). Buscar
        antes de agregar es lo que mantiene el punto 2 del invariante: sin esa
        búsqueda quedarían dos pares con la misma clave.

            >>> carrito = Carrito()
            >>> carrito.meter("pan", 2)
            >>> carrito.meter("pan", 3)
            >>> carrito.cuanto_hay("pan")
            5

        Args:
            producto: nombre del producto (cadena no vacía).
            cantidad: entero mayor o igual a 1.

        Raises:
            ValueError: si el producto o la cantidad no son válidos. En ese caso
                el carrito **no cambia**, porque las dos validaciones ocurren
                antes de tocar la lista (A8, atomicidad).

        Complejidad:
            O(n) por la búsqueda.
        """
        clave = self._clave(producto)
        self._validar_cantidad(cantidad)

        indice = self._buscar_indice(clave)

        if indice is None:
            self._productos.append((clave, cantidad))
        else:
            _nombre, cantidad_actual = self._productos[indice]
            # El par es una tupla inmutable: se reemplaza completo.
            self._productos[indice] = (clave, cantidad_actual + cantidad)

    def sacar(self, producto: str, cantidad: int) -> None:
        """Retira `cantidad` unidades de `producto` del carrito.

        Si la cantidad llega a cero, el par **se elimina** de la lista; no queda
        un par con cantidad 0 (A5, punto 1 del invariante).

            >>> carrito = Carrito()
            >>> carrito.meter("pan", 3)
            >>> carrito.sacar("pan", 1)
            >>> carrito.cuanto_hay("pan")
            2
            >>> carrito.sacar("pan", 2)
            >>> carrito.cuanto_llevo()
            0

        Args:
            producto: nombre del producto (cadena no vacía).
            cantidad: entero mayor o igual a 1, y no mayor que lo disponible.

        Raises:
            ValueError: si el producto o la cantidad no son válidos, si el
                producto no está en el carrito (A9), o si se piden más unidades
                de las que hay (A8). En todos los casos el carrito queda
                **exactamente como estaba**: todas las comprobaciones se hacen
                antes de la primera modificación.

        Complejidad:
            O(n) por la búsqueda; el `pop` intermedio además desplaza los pares
            siguientes una posición.
        """
        clave = self._clave(producto)
        self._validar_cantidad(cantidad)

        indice = self._buscar_indice(clave)

        if indice is None:
            raise ValueError(f"El producto '{clave}' no está en el carrito.")

        _nombre, disponible = self._productos[indice]

        if cantidad > disponible:
            raise ValueError(
                f"No se pueden sacar {cantidad} unidades de '{clave}': "
                f"solo hay {disponible}."
            )

        restante = disponible - cantidad

        if restante == 0:
            self._productos.pop(indice)
        else:
            self._productos[indice] = (clave, restante)

    def cuanto_hay(self, producto: str) -> int:
        """Devuelve cuántas unidades de `producto` hay en el carrito.

        Un producto ausente responde `0` en vez de lanzar excepción (A10):
        preguntar por algo que no está tiene una respuesta correcta, a
        diferencia de ordenar sacarlo.

            >>> carrito = Carrito()
            >>> carrito.cuanto_hay("pan")
            0
            >>> carrito.meter("pan", 4)
            >>> carrito.cuanto_hay("pan")
            4

        Args:
            producto: nombre del producto (cadena no vacía).

        Returns:
            Las unidades de ese producto; `0` si no está en el carrito.

        Raises:
            ValueError: si el nombre del producto no es válido.

        Complejidad:
            O(n).
        """
        indice = self._buscar_indice(self._clave(producto))

        if indice is None:
            return 0

        _nombre, cantidad = self._productos[indice]

        return cantidad

    def cuanto_llevo(self) -> int:
        """Devuelve el total de **unidades** que lleva el carrito.

        Unidades, no dinero: es la decisión A1, tomada porque el requisito
        original nunca mencionó precios.

            >>> carrito = Carrito()
            >>> carrito.cuanto_llevo()
            0
            >>> carrito.meter("pan", 2)
            >>> carrito.meter("leche", 3)
            >>> carrito.cuanto_llevo()
            5

        Returns:
            La suma de las cantidades de todos los productos; `0` si está vacío.

        Complejidad:
            O(n). Se recalcula en cada llamada en vez de mantener un total
            acumulado: un acumulador sería O(1) pero introduce estado duplicado
            que puede desincronizarse del contenido real (ver §6 de `spec.md`).
        """
        return sum(cantidad for _nombre, cantidad in self._productos)

    # -- Auxiliar (no forma parte del contrato) ----------------------------

    def __repr__(self) -> str:
        """Representación legible para depurar y para los informes de pytest.

        Muestra la estructura interna a propósito, para que al leer un fallo se
        vea de inmediato con qué implementación se está trabajando: aquí
        aparecen corchetes, en `carrito_dict.py` aparecen llaves.

            >>> carrito = Carrito()
            >>> carrito.meter("pan", 2)
            >>> carrito
            Carrito([('pan', 2)])
        """
        return f"{type(self).__name__}({self._productos!r})"
