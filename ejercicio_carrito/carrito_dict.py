"""Implementación del TAD `Carrito` sobre un **diccionario**.

Contrato: [`spec.md`](spec.md). Este archivo no lo reinterpreta ni lo amplía; solo
lo cumple con una estructura de datos concreta.

Representación
--------------
Un único diccionario `self._productos` que va de la **clave normalizada** del
producto (A3 de `spec.md`) a la **cantidad** de unidades:

    {"pan": 5, "leche": 2}

Por qué un diccionario
----------------------
El TAD casi siempre está haciendo lo mismo: *dado un producto, encontrar su
cantidad*. Eso es exactamente lo que un diccionario resuelve en **O(1) promedio**
gracias a la tabla hash que tiene por debajo, mientras que una lista tiene que
recorrer (ver `carrito_lista.py` para la comparación).

Además, la unicidad de las claves del diccionario **regala el punto 2 del
invariante**: es imposible que existan dos entradas para el mismo producto,
porque el propio diccionario no lo permite. En la versión con lista esa
propiedad hay que sostenerla a mano.

Costo de cada operación (`n` = productos distintos en el carrito)
-----------------------------------------------------------------
- `meter`         O(1) promedio
- `sacar`         O(1) promedio
- `cuanto_hay`    O(1) promedio
- `cuanto_llevo`  O(n) — hay que sumar todas las cantidades

Invariante de representación (§5 de `spec.md`)
----------------------------------------------
1. todos los valores son enteros `>= 1` (el producto que llega a 0 se borra);
2. las claves son únicas y están normalizadas;
3. `cuanto_llevo()` es la suma de los valores;
4. el diccionario se crea dentro de `__init__`, así que **pertenece a la
   instancia** y no se comparte con ningún otro carrito (A12; ver `autopsia.md`).

Nota sobre la restricción de la actividad
-----------------------------------------
No se usa `collections.Counter`. Sería una sola línea, pero justamente lo que se
está estudiando es qué hace `Counter` por dentro: un diccionario de cuentas con
un valor por omisión.
"""


class Carrito:
    """Carrito de compras que cuenta unidades por producto.

    Ejemplo de uso completo:

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

        El diccionario se construye **aquí dentro**, en cada llamada. Esa es la
        línea que garantiza la decisión A12: dos cajas distintas obtienen dos
        diccionarios distintos. Escribirlo como atributo de clase o como valor
        por omisión de un parámetro reproduciría el error de `autopsia.md`.
        """
        self._productos: dict[str, int] = {}

    # -- Validaciones (privadas) -------------------------------------------

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

    # -- Operaciones del contrato ------------------------------------------

    def meter(self, producto: str, cantidad: int) -> None:
        """Agrega `cantidad` unidades de `producto` al carrito.

        Si el producto ya estaba, las cantidades **se acumulan** (A4).

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
                antes de tocar el diccionario (A8, atomicidad).

        Complejidad:
            O(1) promedio.
        """
        clave = self._clave(producto)
        self._validar_cantidad(cantidad)

        # .get(clave, 0) unifica los dos casos —producto nuevo y producto que ya
        # estaba— en una sola línea: si no existe, se parte de cero.
        self._productos[clave] = self._productos.get(clave, 0) + cantidad

    def sacar(self, producto: str, cantidad: int) -> None:
        """Retira `cantidad` unidades de `producto` del carrito.

        Si la cantidad llega a cero, el producto **desaparece** del carrito; no
        queda una entrada con valor 0 (A5, punto 1 del invariante).

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
            O(1) promedio.
        """
        clave = self._clave(producto)
        self._validar_cantidad(cantidad)

        disponible = self._productos.get(clave, 0)

        if disponible == 0:
            raise ValueError(f"El producto '{clave}' no está en el carrito.")

        if cantidad > disponible:
            raise ValueError(
                f"No se pueden sacar {cantidad} unidades de '{clave}': "
                f"solo hay {disponible}."
            )

        restante = disponible - cantidad

        if restante == 0:
            del self._productos[clave]
        else:
            self._productos[clave] = restante

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
            O(1) promedio.
        """
        return self._productos.get(self._clave(producto), 0)

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
        return sum(self._productos.values())

    # -- Auxiliar (no forma parte del contrato) ----------------------------

    def __repr__(self) -> str:
        """Representación legible para depurar y para los informes de pytest.

        Muestra la estructura interna a propósito, para que al leer un fallo se
        vea de inmediato con qué implementación se está trabajando.

            >>> carrito = Carrito()
            >>> carrito.meter("pan", 2)
            >>> carrito
            Carrito({'pan': 2})
        """
        return f"{type(self).__name__}({self._productos!r})"
