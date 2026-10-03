"""Menú interactivo para operar el TAD `Carrito` desde la terminal.

Este archivo **no forma parte de la entrega**: el ejercicio pedía el TAD, sus
pruebas y la autopsia. Es una capa de presentación que se agrega encima para
poder usar el carrito a mano, sin escribir código en el intérprete.

Qué es y qué no es
------------------
Es un **cliente** del contrato descrito en `spec.md`. Solo llama a las cuatro
operaciones públicas —`meter`, `sacar`, `cuanto_hay`, `cuanto_llevo`— y nunca
toca `_productos` ni ninguna otra parte interna. Esa disciplina es el punto:
si el menú tuviera que asomarse a la estructura de datos para funcionar,
significaría que el TAD está mal diseñado.

La consecuencia práctica es que **cambiar de implementación es cambiar una
sola línea**: la opción 5 del menú intercambia `carrito_dict` por
`carrito_lista` y todo lo demás sigue igual, porque el contrato es el mismo.

Los errores del TAD como mensajes
---------------------------------
`spec.md` decidió que las operaciones inválidas lanzan `ValueError` en vez de
fallar en silencio (decisiones A6 a A9). Aquí se ve para qué sirvió esa
decisión: el menú atrapa esas excepciones y las convierte en un aviso legible,
sin tener que validar nada por su cuenta. La regla vive en un solo lugar.

Ejecutar:

    python menu.py
"""

from carrito_dict import Carrito as CarritoDiccionario
from carrito_lista import Carrito as CarritoLista

ANCHO = 60

#: Implementaciones entre las que se puede alternar desde el menú.
IMPLEMENTACIONES = {
    "diccionario": (CarritoDiccionario, "carrito_dict.py", "O(1) promedio"),
    "lista de pares": (CarritoLista, "carrito_lista.py", "O(n)"),
}


# ---------------------------------------------------------------------------
# Entrada de datos
# ---------------------------------------------------------------------------


def preguntar(mensaje: str) -> str:
    """Pide un texto al usuario.

    Args:
        mensaje: lo que se muestra antes del cursor.

    Returns:
        Lo que escribió, sin espacios en los extremos.

    Raises:
        SystemExit: si cierra la entrada con Ctrl+C o Ctrl+D, para que el
            programa termine con un mensaje en vez de con un rastro de error.
    """
    try:
        # El ﻿ (BOM) aparece cuando la entrada llega canalizada desde
        # PowerShell en vez de escribirse a mano; sin quitarlo, la primera
        # respuesta traería un carácter invisible pegado al principio.
        return input(mensaje).strip().lstrip("﻿").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  Hasta luego.\n")
        raise SystemExit(0)


def preguntar_cantidad(mensaje: str) -> int | None:
    """Pide una cantidad y la convierte a entero.

    Solo se encarga de que sea *un número*. Si es un número **válido** para el
    carrito (mayor o igual a 1) lo decide el TAD, no el menú: esa regla está
    en `_validar_cantidad` y no se repite aquí.

    Returns:
        El entero escrito, o `None` si lo que escribió no era un número.
    """
    texto = preguntar(mensaje)

    try:
        return int(texto)
    except ValueError:
        print(f"\n  «{texto}» no es un número entero.")
        return None


def unidades(cantidad: int) -> str:
    """Devuelve «1 unidad» o «N unidades», para no escribir «1 unidades».

        >>> unidades(1)
        '1 unidad'
        >>> unidades(5)
        '5 unidades'
    """
    return "1 unidad" if cantidad == 1 else f"{cantidad} unidades"


def clave_de_presentacion(nombre: str) -> str:
    """Normaliza un nombre igual que lo hace el TAD, solo para no mostrarlo dos veces.

    El menú lleva su propia lista de los productos que ha visto, porque el
    contrato no ofrece ninguna operación para recorrer el carrito (`spec.md`
    §7 deja el recorrido fuera de alcance). Sin esta normalización, escribir
    «Pan» y luego «pan» produciría dos renglones en pantalla para un único
    producto del carrito.

    Es una regla repetida, y conviene saberlo: la solución limpia sería
    ampliar el contrato con una operación que devuelva los productos. Mientras
    eso no exista, esta duplicación es el precio de poder mostrar el carrito.
    """
    return " ".join(nombre.split()).lower()


# ---------------------------------------------------------------------------
# Presentación
# ---------------------------------------------------------------------------


def mostrar_encabezado(nombre_implementacion: str) -> None:
    """Dibuja el título y deja claro qué implementación está activa."""
    _clase, archivo, costo = IMPLEMENTACIONES[nombre_implementacion]

    print()
    print("=" * ANCHO)
    print("  CARRITO DE COMPRAS  ·  Tienda del campus")
    print(f"  Implementación: {nombre_implementacion} ({archivo}) · búsqueda {costo}")
    print("=" * ANCHO)


def mostrar_carrito(carrito, vistos: list[str]) -> None:
    """Muestra el contenido del carrito.

    Args:
        carrito: el TAD.
        vistos: nombres que el menú ha visto pasar. Se consulta cada uno con
            `cuanto_hay`; los que devuelven 0 ya no están y no se muestran.
    """
    renglones = [(nombre, carrito.cuanto_hay(nombre)) for nombre in vistos]
    renglones = [(nombre, cantidad) for nombre, cantidad in renglones if cantidad > 0]

    print()

    if not renglones:
        print("  El carrito está vacío.")
    else:
        for nombre, cantidad in sorted(renglones):
            puntos = "." * max(3, 44 - len(nombre))
            print(f"  {nombre} {puntos} {cantidad:>3}")

        print("  " + "-" * 48)
        distintos = len(renglones)
        plural = "producto distinto" if distintos == 1 else "productos distintos"
        print(f"  {distintos} {plural}, {unidades(carrito.cuanto_llevo())} en total")


def mostrar_opciones() -> None:
    """Dibuja las opciones disponibles."""
    print()
    print("  [1] Meter productos          [4] Vaciar el carrito")
    print("  [2] Sacar productos          [5] Cambiar de implementación")
    print("  [3] Consultar un producto    [0] Salir")
    print()


# ---------------------------------------------------------------------------
# Acciones
# ---------------------------------------------------------------------------


def accion_meter(carrito, vistos: list[str]) -> None:
    """Opción 1: agrega unidades de un producto."""
    producto = preguntar("  Producto a meter: ")
    cantidad = preguntar_cantidad("  ¿Cuántas unidades?: ")

    if cantidad is None:
        return

    try:
        carrito.meter(producto, cantidad)
    except ValueError as error:
        # El TAD ya explicó qué estuvo mal; el menú solo lo repite.
        print(f"\n  No se pudo: {error}")
        return

    clave = clave_de_presentacion(producto)
    if clave not in vistos:
        vistos.append(clave)

    print(f"\n  Listo: {clave} queda en {unidades(carrito.cuanto_hay(producto))}.")


def accion_sacar(carrito, vistos: list[str]) -> None:
    """Opción 2: retira unidades de un producto."""
    producto = preguntar("  Producto a sacar: ")
    cantidad = preguntar_cantidad("  ¿Cuántas unidades?: ")

    if cantidad is None:
        return

    try:
        carrito.sacar(producto, cantidad)
    except ValueError as error:
        print(f"\n  No se pudo: {error}")
        return

    restante = carrito.cuanto_hay(producto)

    if restante == 0:
        print(f"\n  Listo: {clave_de_presentacion(producto)} salió del carrito.")
    else:
        print(f"\n  Listo: quedan {unidades(restante)}.")


def accion_consultar(carrito, _vistos: list[str]) -> None:
    """Opción 3: pregunta cuántas unidades hay de un producto.

    Demuestra la decisión A10: preguntar por un producto que no está **no es un
    error**, responde 0.
    """
    producto = preguntar("  ¿Qué producto quieres consultar?: ")

    try:
        cantidad = carrito.cuanto_hay(producto)
    except ValueError as error:
        print(f"\n  No se pudo: {error}")
        return

    if cantidad == 0:
        print(f"\n  No llevas ninguna unidad de «{clave_de_presentacion(producto)}».")
    else:
        print(f"\n  Llevas {unidades(cantidad)} de «{clave_de_presentacion(producto)}».")


def accion_vaciar(carrito, vistos: list[str]) -> None:
    """Opción 4: retira todo, usando solo operaciones del contrato."""
    if carrito.cuanto_llevo() == 0:
        print("\n  El carrito ya estaba vacío.")
        return

    retirados = 0

    for nombre in list(vistos):
        cantidad = carrito.cuanto_hay(nombre)
        if cantidad > 0:
            carrito.sacar(nombre, cantidad)
            retirados += cantidad

    vistos.clear()
    print(f"\n  Carrito vaciado: se retiraron {unidades(retirados)}.")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------


def cambiar_implementacion(actual: str) -> str:
    """Opción 5: alterna entre las dos implementaciones del mismo contrato.

    El carrito se crea de nuevo y queda vacío: son dos objetos distintos, y
    ninguno puede ver lo que hay en el otro (decisión A12).
    """
    nombres = list(IMPLEMENTACIONES)
    nuevo = nombres[(nombres.index(actual) + 1) % len(nombres)]

    print(f"\n  Cambiado a: {nuevo}. El carrito empieza vacío.")

    return nuevo


def main() -> None:
    """Bucle principal del menú."""
    implementacion = "diccionario"
    carrito = IMPLEMENTACIONES[implementacion][0]()
    vistos: list[str] = []

    acciones = {
        "1": accion_meter,
        "2": accion_sacar,
        "3": accion_consultar,
        "4": accion_vaciar,
    }

    while True:
        mostrar_encabezado(implementacion)
        mostrar_carrito(carrito, vistos)
        mostrar_opciones()

        opcion = preguntar("  Opción: ")

        if opcion == "0":
            print("\n  Hasta luego.\n")
            return

        if opcion == "5":
            implementacion = cambiar_implementacion(implementacion)
            carrito = IMPLEMENTACIONES[implementacion][0]()
            vistos = []
            continue

        accion = acciones.get(opcion)

        if accion is None:
            print(f"\n  «{opcion}» no es una opción del menú.")
            continue

        accion(carrito, vistos)


if __name__ == "__main__":
    main()
