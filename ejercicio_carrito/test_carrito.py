"""Batería única de pruebas del TAD `Carrito`.

Este archivo es **uno solo** y se ejecuta **sin modificarse** contra las dos
implementaciones (`carrito_lista.py` y `carrito_dict.py`). Esa es justamente la
prueba de que el contrato de `spec.md` describe *comportamiento observable* y no
una estructura de datos concreta: si para hacer pasar una implementación hubiera
que tocar este archivo, el contrato estaría mal escrito.

Cómo se logra: la fixture `clase_carrito` está parametrizada con las dos clases,
así que pytest ejecuta automáticamente cada prueba dos veces, una por
implementación. En la salida aparecen identificadas como `[lista]` y `[dict]`.

Organización de las pruebas (los números remiten a las decisiones de `spec.md`):

1. Carrito vacío ............................. A11
2. Meter ..................................... A4
3. Sacar ..................................... A5, A8, A9
4. Consultar ................................. A10
5. Identidad del producto .................... A3
6. Cantidades inválidas ...................... A6, A7
7. Atomicidad ante el error .................. A8
8. Independencia entre carritos .............. A12  <- el error de `autopsia.md`

Ejecutar:

    python -m pytest -v
"""

import pytest

from carrito_lista import Carrito as CarritoLista
from carrito_dict import Carrito as CarritoDict


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

#: Las dos implementaciones del mismo contrato. Agregar una tercera aquí basta
#: para que toda la batería se ejecute también contra ella.
IMPLEMENTACIONES = [CarritoLista, CarritoDict]


@pytest.fixture(params=IMPLEMENTACIONES, ids=["lista", "dict"])
def clase_carrito(request):
    """Devuelve la **clase** a probar (no una instancia).

    Se usa en las pruebas que necesitan construir más de un carrito, como las
    de independencia entre instancias.
    """
    return request.param


@pytest.fixture
def carrito(clase_carrito):
    """Devuelve un carrito **vacío y recién creado** de la implementación en turno.

    Es la fixture que usa la mayoría de las pruebas. Como pytest la reconstruye
    para cada prueba, ninguna prueba puede contaminar a otra.
    """
    return clase_carrito()


# ---------------------------------------------------------------------------
# 1. Carrito vacío (caso extremo: A11)
# ---------------------------------------------------------------------------


def test_carrito_nuevo_esta_vacio(carrito):
    """Un carrito recién creado lleva 0 unidades en total."""
    assert carrito.cuanto_llevo() == 0


def test_carrito_nuevo_no_tiene_ningun_producto(carrito):
    """Consultar cualquier producto en un carrito vacío devuelve 0, no error (A10)."""
    assert carrito.cuanto_hay("pan") == 0
    assert carrito.cuanto_hay("leche") == 0


# ---------------------------------------------------------------------------
# 2. Meter (A4)
# ---------------------------------------------------------------------------


def test_meter_producto_y_consultar_cantidad(carrito):
    """Lo que se mete es lo que se consulta."""
    carrito.meter("pan", 3)

    assert carrito.cuanto_hay("pan") == 3
    assert carrito.cuanto_llevo() == 3


def test_meter_dos_veces_el_mismo_producto_acumula(carrito):
    """A4: meter un producto que ya está **suma**, no crea un segundo renglón."""
    carrito.meter("pan", 2)
    carrito.meter("pan", 3)

    assert carrito.cuanto_hay("pan") == 5
    assert carrito.cuanto_llevo() == 5


def test_meter_varios_productos_los_mantiene_separados(carrito):
    """Cada producto conserva su propia cantidad y el total es la suma."""
    carrito.meter("pan", 2)
    carrito.meter("leche", 4)

    assert carrito.cuanto_hay("pan") == 2
    assert carrito.cuanto_hay("leche") == 4
    assert carrito.cuanto_llevo() == 6


def test_meter_una_unidad_a_la_vez(carrito):
    """El caso más común en una caja: se van pasando productos uno por uno."""
    for _ in range(5):
        carrito.meter("manzana", 1)

    assert carrito.cuanto_hay("manzana") == 5
    assert carrito.cuanto_llevo() == 5


# ---------------------------------------------------------------------------
# 3. Sacar (A5, A8, A9)
# ---------------------------------------------------------------------------


def test_sacar_producto_reduce_la_cantidad(carrito):
    """Sacar una parte deja el resto en el carrito."""
    carrito.meter("pan", 5)

    carrito.sacar("pan", 2)

    assert carrito.cuanto_hay("pan") == 3
    assert carrito.cuanto_llevo() == 3


def test_sacar_todas_las_unidades_elimina_el_producto(carrito):
    """A5: al llegar a 0 el producto **desaparece**; no queda un renglón en 0."""
    carrito.meter("pan", 3)

    carrito.sacar("pan", 3)

    assert carrito.cuanto_hay("pan") == 0
    assert carrito.cuanto_llevo() == 0


def test_sacar_no_afecta_a_los_demas_productos(carrito):
    """Vaciar un producto no toca a los otros."""
    carrito.meter("pan", 2)
    carrito.meter("leche", 4)

    carrito.sacar("pan", 2)

    assert carrito.cuanto_hay("pan") == 0
    assert carrito.cuanto_hay("leche") == 4
    assert carrito.cuanto_llevo() == 4


def test_meter_de_nuevo_despues_de_vaciar_un_producto(carrito):
    """Vaciar y volver a meter debe comportarse como la primera vez."""
    carrito.meter("pan", 2)
    carrito.sacar("pan", 2)

    carrito.meter("pan", 4)

    assert carrito.cuanto_hay("pan") == 4
    assert carrito.cuanto_llevo() == 4


def test_sacar_producto_que_no_esta_falla(carrito):
    """Caso extremo A9: sacar lo que no está es una orden imposible -> ValueError."""
    with pytest.raises(ValueError):
        carrito.sacar("pan", 1)


def test_sacar_de_un_carrito_vacio_falla(carrito):
    """Caso extremo: el carrito vacío no es un caso especial, sigue la regla A9."""
    with pytest.raises(ValueError):
        carrito.sacar("cualquier cosa", 1)

    assert carrito.cuanto_llevo() == 0


# ---------------------------------------------------------------------------
# 4. Consultar (A10)
# ---------------------------------------------------------------------------


def test_consultar_producto_ausente_devuelve_cero_y_no_lo_crea(carrito):
    """A10: preguntar no modifica. Consultar un ausente no lo agrega al carrito."""
    carrito.meter("pan", 1)

    assert carrito.cuanto_hay("leche") == 0
    assert carrito.cuanto_llevo() == 1  # sigue habiendo solo el pan


def test_consultar_no_modifica_el_carrito(carrito):
    """Las consultas son operaciones de solo lectura."""
    carrito.meter("pan", 3)

    carrito.cuanto_hay("pan")
    carrito.cuanto_llevo()

    assert carrito.cuanto_hay("pan") == 3
    assert carrito.cuanto_llevo() == 3


# ---------------------------------------------------------------------------
# 5. Identidad del producto (A3)
# ---------------------------------------------------------------------------


def test_el_nombre_no_distingue_mayusculas(carrito):
    """A3: "Pan" y "pan" son el mismo producto."""
    carrito.meter("Pan", 2)
    carrito.meter("pan", 3)

    assert carrito.cuanto_hay("PAN") == 5
    assert carrito.cuanto_llevo() == 5


def test_el_nombre_ignora_espacios_sobrantes(carrito):
    """A3: se recortan los extremos y se colapsan los espacios internos."""
    carrito.meter("  pan   integral ", 2)

    assert carrito.cuanto_hay("pan integral") == 2
    assert carrito.cuanto_llevo() == 2


def test_se_puede_sacar_escribiendo_el_nombre_distinto(carrito):
    """La normalización también aplica al sacar: es el mismo producto."""
    carrito.meter("Leche Entera", 4)

    carrito.sacar("  leche  entera ", 4)

    assert carrito.cuanto_llevo() == 0


def test_las_tildes_si_distinguen_productos(carrito):
    """A3: se decidió NO quitar tildes; "café" y "cafe" son productos distintos."""
    carrito.meter("café", 2)

    assert carrito.cuanto_hay("café") == 2
    assert carrito.cuanto_hay("cafe") == 0


@pytest.mark.parametrize(
    "producto_invalido",
    [None, "", "   ", 5, 3.5, ["pan"], ("pan",), {"pan": 1}],
    ids=["None", "vacio", "solo_espacios", "int", "float", "lista", "tupla", "dict"],
)
def test_producto_invalido_falla(carrito, producto_invalido):
    """A3: si el nombre no identifica nada, la operación no puede ejecutarse."""
    with pytest.raises(ValueError):
        carrito.meter(producto_invalido, 1)

    with pytest.raises(ValueError):
        carrito.sacar(producto_invalido, 1)

    with pytest.raises(ValueError):
        carrito.cuanto_hay(producto_invalido)

    assert carrito.cuanto_llevo() == 0


# ---------------------------------------------------------------------------
# 6. Cantidades inválidas (A6, A7)
# ---------------------------------------------------------------------------


def test_cantidad_cero_al_meter_falla(carrito):
    """Caso extremo A6: meter cero no es una operación válida."""
    with pytest.raises(ValueError):
        carrito.meter("pan", 0)

    assert carrito.cuanto_llevo() == 0


def test_cantidad_cero_al_sacar_falla(carrito):
    """Caso extremo A6: sacar cero tampoco, y el carrito no cambia."""
    carrito.meter("pan", 2)

    with pytest.raises(ValueError):
        carrito.sacar("pan", 0)

    assert carrito.cuanto_hay("pan") == 2


def test_cantidad_negativa_al_meter_falla(carrito):
    """A7: un negativo al meter sería un `sacar` disfrazado sin validaciones."""
    with pytest.raises(ValueError):
        carrito.meter("pan", -2)

    assert carrito.cuanto_llevo() == 0


def test_cantidad_negativa_al_sacar_falla(carrito):
    """A7: un negativo al sacar sería un `meter` disfrazado."""
    carrito.meter("pan", 2)

    with pytest.raises(ValueError):
        carrito.sacar("pan", -1)

    assert carrito.cuanto_hay("pan") == 2


@pytest.mark.parametrize(
    "cantidad_invalida",
    [1.0, 2.5, "3", None, True, False, [1]],
    ids=["float_entero", "float", "str", "None", "True", "False", "lista"],
)
def test_cantidad_que_no_es_entero_falla(carrito, cantidad_invalida):
    """A7: la cantidad debe ser `int`.

    `True`/`False` merecen mención aparte: en Python `bool` es subclase de `int`
    y `True == 1`, así que sin un filtro explícito `meter("pan", True)` metería
    una unidad de pan en silencio.
    """
    with pytest.raises(ValueError):
        carrito.meter("pan", cantidad_invalida)

    assert carrito.cuanto_llevo() == 0


# ---------------------------------------------------------------------------
# 7. Atomicidad ante el error (A8)
# ---------------------------------------------------------------------------


def test_sacar_mas_de_lo_disponible_falla_y_no_modifica(carrito):
    """A8: la operación inválida se rechaza **entera**, no a medias."""
    carrito.meter("pan", 2)

    with pytest.raises(ValueError):
        carrito.sacar("pan", 3)

    assert carrito.cuanto_hay("pan") == 2
    assert carrito.cuanto_llevo() == 2


def test_una_operacion_fallida_no_afecta_al_resto_del_carrito(carrito):
    """El carrito completo queda intacto, no solo el producto involucrado."""
    carrito.meter("pan", 2)
    carrito.meter("leche", 4)

    with pytest.raises(ValueError):
        carrito.sacar("pan", 99)

    assert carrito.cuanto_hay("pan") == 2
    assert carrito.cuanto_hay("leche") == 4
    assert carrito.cuanto_llevo() == 6


def test_el_carrito_sigue_usable_despues_de_un_error(carrito):
    """Tras una excepción el objeto no queda corrupto: se puede seguir trabajando."""
    carrito.meter("pan", 2)

    with pytest.raises(ValueError):
        carrito.sacar("pan", 10)

    carrito.meter("pan", 1)
    carrito.sacar("pan", 3)

    assert carrito.cuanto_llevo() == 0


def test_secuencia_larga_de_operaciones(carrito):
    """Prueba de integración: una compra completa, con altas, bajas y consultas."""
    carrito.meter("pan", 5)
    carrito.meter("leche", 2)
    carrito.meter("Pan", 1)  # mismo producto que "pan" (A3)
    carrito.sacar("pan", 2)
    carrito.meter("huevos", 12)
    carrito.sacar("leche", 2)  # vacía la leche

    assert carrito.cuanto_hay("pan") == 4
    assert carrito.cuanto_hay("leche") == 0
    assert carrito.cuanto_hay("huevos") == 12
    assert carrito.cuanto_llevo() == 16


# ---------------------------------------------------------------------------
# 8. Independencia entre carritos (A12)
#
# Este bloque es la contraparte ejecutable de `autopsia.md`: son las pruebas que
# habrían atrapado el error de "las dos cajas comparten el mismo carrito" antes
# de que llegara a la tienda.
# ---------------------------------------------------------------------------


def test_dos_carritos_recien_creados_son_independientes(clase_carrito):
    """A12: lo que se mete en una caja NO se ve desde la otra.

    Es la prueba de comportamiento del error de `autopsia.md`. Con el código
    anterior —donde las dos cajas compartían el mismo objeto mutable— la última
    afirmación fallaba: `caja_2` "veía" el pan de `caja_1`.
    """
    caja_1 = clase_carrito()
    caja_2 = clase_carrito()

    caja_1.meter("pan", 2)

    assert caja_1.cuanto_hay("pan") == 2
    assert caja_2.cuanto_hay("pan") == 0
    assert caja_2.cuanto_llevo() == 0


def test_las_operaciones_de_una_caja_no_se_filtran_a_la_otra(clase_carrito):
    """Versión más exigente: las dos cajas trabajan a la vez, como en la tienda."""
    caja_1 = clase_carrito()
    caja_2 = clase_carrito()

    caja_1.meter("pan", 3)
    caja_2.meter("leche", 5)
    caja_1.sacar("pan", 1)

    assert caja_1.cuanto_llevo() == 2
    assert caja_2.cuanto_llevo() == 5
    assert caja_1.cuanto_hay("leche") == 0
    assert caja_2.cuanto_hay("pan") == 0


def test_cada_carrito_tiene_su_propio_almacenamiento(clase_carrito):
    """A12, versión estructural: ningún contenedor mutable se comparte.

    La prueba anterior mira el comportamiento; esta mira la causa. Recorre los
    atributos de instancia sin conocer sus nombres (por eso sirve para cualquier
    implementación) y exige que los contenedores mutables de un carrito **no
    sean el mismo objeto** que los del otro. Es la traducción a código de la
    comprobación `caja_1._productos is caja_2._productos` de `autopsia.md`.
    """
    caja_1 = clase_carrito()
    caja_2 = clase_carrito()

    contenedores_1 = [v for v in vars(caja_1).values() if isinstance(v, (list, dict, set))]
    contenedores_2 = [v for v in vars(caja_2).values() if isinstance(v, (list, dict, set))]

    assert contenedores_1, "el carrito debe guardar su estado en un contenedor propio"
    assert len(contenedores_1) == len(contenedores_2)

    for propio, ajeno in zip(contenedores_1, contenedores_2):
        assert propio is not ajeno, "dos carritos comparten el mismo objeto mutable"


def test_la_clase_no_guarda_contenedores_mutables(clase_carrito):
    """Bloquea la causa 2 del error: un contenedor mutable como atributo de clase.

    Un `_productos = []` escrito al nivel de la clase vive en la clase, no en
    cada objeto, y por lo tanto lo comparten todas las instancias.
    """
    mutables_en_la_clase = {
        nombre: valor
        for nombre, valor in vars(clase_carrito).items()
        if not nombre.startswith("__") and isinstance(valor, (list, dict, set))
    }

    assert mutables_en_la_clase == {}


def test_el_constructor_no_tiene_valores_por_omision_mutables(clase_carrito):
    """Bloquea la causa 1 del error: `def __init__(self, productos=[])`.

    Los valores por omisión se evalúan **una sola vez**, cuando se define la
    función, así que todas las instancias que usen el valor por omisión reciben
    exactamente el mismo objeto.
    """
    por_omision = clase_carrito.__init__.__defaults__ or ()

    assert not any(isinstance(valor, (list, dict, set)) for valor in por_omision)
