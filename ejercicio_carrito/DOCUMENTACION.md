# Documentación completa — TAD Carrito

Tienda del campus · Estructura de Datos

Este documento explica **todo el trabajo**: qué problema se resolvió, cómo se
decidió resolverlo, qué hace cada línea importante del código, cómo funcionan las
pruebas y por qué una estructura de datos gana sobre la otra (con mediciones
reales, no con teoría suelta).

Los demás archivos del proyecto son la entrega formal; este es el recorrido
completo por dentro.

---

## Índice

1. [Qué es este trabajo](#1-qué-es-este-trabajo)
2. [El método: decidir antes de programar](#2-el-método-decidir-antes-de-programar)
3. [Las decisiones: qué significa cada palabra del requisito](#3-las-decisiones-qué-significa-cada-palabra-del-requisito)
4. [El código, explicado línea por línea](#4-el-código-explicado-línea-por-línea)
5. [Las pruebas, explicadas](#5-las-pruebas-explicadas)
6. [El error de las dos cajas](#6-el-error-de-las-dos-cajas)
7. [Complejidad: la teoría y el cronómetro](#7-complejidad-la-teoría-y-el-cronómetro)
8. [Cómo ejecutar y verificar todo](#8-cómo-ejecutar-y-verificar-todo)
9. [Glosario](#9-glosario)
10. [Mapa: requisito de la actividad → dónde está resuelto](#10-mapa-requisito-de-la-actividad--dónde-está-resuelto)

---

## 1. Qué es este trabajo

### 1.1 El caso

La tienda del campus quiere reemplazar su carrito de compras, que hoy es un
archivo de texto que alguien edita a mano. El administrador entregó este
requisito, textual:

> «necesito poder meter productos, sacar productos, saber cuántos hay de cada uno
> y cuánto llevo en total»

Además entregó un fragmento del código anterior que tiene un error real: **dos
cajas distintas comparten sin querer el mismo carrito**, y al modificar una se
modifica la otra.

### 1.2 Por qué ese requisito no se puede programar tal cual

La frase se entiende perfectamente al leerla. El problema aparece al intentar
escribirla en código, porque **cada verbo admite más de una traducción** y las
traducciones llevan a programas distintos:

| Lo que dice el administrador | Lo que un programador tiene que preguntarse |
| ---------------------------- | ------------------------------------------- |
| «meter productos»            | Si el pan ya está, ¿sumo o creo otro renglón? |
| «sacar productos»            | ¿Saco una unidad, N, o el renglón completo? |
| «saber cuántos hay de cada uno» | ¿Cuántos hay **en el carrito** o **en la tienda**? |
| «cuánto llevo en total»      | ¿Cuántos **artículos** o cuánto **dinero**? |

Ninguna de esas preguntas tiene una respuesta obvia, y elegir mal no produce un
error visible: produce un programa que funciona y hace lo que no era. Por eso el
trabajo **empieza escribiendo las decisiones**, no programando.

### 1.3 Qué se entrega

| Archivo                                  | Qué es                                                             |
| ---------------------------------------- | ------------------------------------------------------------------ |
| [`spec.md`](spec.md)                     | El contrato del TAD y las 12 ambigüedades decididas, cada una razonada |
| [`test_carrito.py`](test_carrito.py)     | La batería **única** de pruebas (46 casos × 2 implementaciones)     |
| [`carrito_lista.py`](carrito_lista.py)   | Implementación con **lista de pares**                               |
| [`carrito_dict.py`](carrito_dict.py)     | Implementación con **diccionario**                                  |
| [`autopsia.md`](autopsia.md)             | El diagnóstico del error de las dos cajas, con 3 diagramas de memoria |
| [`VERIFICACION.txt`](VERIFICACION.txt)   | Salida literal de las pruebas en rojo y en verde                    |
| [`README.md`](README.md)                 | Guía rápida del repositorio                                         |
| `DOCUMENTACION.md`                       | Este documento                                                      |

**TAD** significa *Tipo Abstracto de Datos*: se define **qué operaciones existen y
qué garantizan**, sin decir cómo se guardan los datos por dentro. Que el mismo
archivo de pruebas pase con dos estructuras internas completamente distintas es la
demostración práctica de que el TAD está bien definido.

---

## 2. El método: decidir antes de programar

El trabajo se hizo en tres etapas, y cada etapa es un commit de Git. El orden no
es un detalle administrativo: **es la evidencia de que las pruebas se escribieron
antes que el código**, y no al revés para que dieran verde.

### 2.1 Las tres etapas

```
bc82066  Define el contrato del TAD Carrito y sus pruebas          → ROJO
cac09f8  Implementa el carrito con lista de pares y con diccionario → VERDE
1f8ea3e  Documenta el diagnostico del error de las dos cajas
```

**Etapa 1 (rojo).** Solo existen `spec.md` y `test_carrito.py`. Las pruebas ya
describen exactamente cómo debe comportarse el carrito, pero no hay ninguna
implementación, así que fallan. Ese fallo es **el punto**: significa que las
pruebas están describiendo algo que todavía no existe.

```
E   ModuleNotFoundError: No module named 'carrito_lista'
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
```

**Etapa 2 (verde).** Aparecen las dos implementaciones. `test_carrito.py` **no se
toca**: es exactamente el mismo archivo del commit anterior.

```
92 passed in 0.13s
```

**Etapa 3.** La autopsia del error y la documentación.

### 2.2 Por qué importa ese orden

Cuando el código se escribe primero y las pruebas después, es muy fácil —sin mala
intención— escribir la prueba que confirma lo que el código ya hace, incluso si lo
que hace está mal. Escribiéndolas antes, la prueba describe lo que el contrato
exige, y el código tiene que alcanzarla.

Hay un segundo beneficio, más práctico: si una prueba pasa en verde **desde el
primer momento**, es una prueba que no está probando nada. Verla fallar primero es
la única manera de saber que funciona.

### 2.3 Cómo comprobarlo sin creer en nadie

El historial se puede auditar. Volver al commit rojo y ejecutar las pruebas ahí:

```bash
git checkout bc82066 && python -m pytest -q
```

Aparecen solo `spec.md` y `test_carrito.py`, y pytest falla al importar. Para
regresar:

```bash
git checkout main
```

Un detalle sobre esa comprobación: el ejercicio vive en `actividad_carrito/` del
repositorio del curso, pero sus commits se crearon cuando era un repositorio
propio. Al volver a `bc82066` el árbol de trabajo queda con `spec.md` y
`test_carrito.py` **en la raíz** (y `clase1/`, `clase2/`, `actividad_carrito/`
desaparecen hasta que regreses a `main`), así que pytest se ejecuta desde ahí.

---

## 3. Las decisiones: qué significa cada palabra del requisito

Están todas en [`spec.md`](spec.md) con su justificación completa. Aquí va el
resumen y, sobre todo, **dónde se ve cada decisión en el código**.

### 3.1 Tabla completa

| #   | Pregunta                                   | Decisión                                   | Dónde vive en el código |
| --- | ------------------------------------------ | ------------------------------------------ | ----------------------- |
| A1  | «cuánto llevo»: ¿unidades o dinero?        | Unidades                                   | `cuanto_llevo()`        |
| A2  | «cuántos hay»: ¿carrito o inventario?      | Carrito                                    | todo el TAD             |
| A3  | ¿Qué identifica a un producto?             | Cadena no vacía, normalizada               | `_clave()`              |
| A4  | ¿Meter algo que ya está?                   | Se acumula                                 | `meter()`               |
| A5  | ¿Cuántas unidades saca `sacar`?            | Cantidad explícita; al llegar a 0 se borra | `sacar()`               |
| A6  | ¿Cantidad cero?                            | `ValueError`                               | `_validar_cantidad()`   |
| A7  | ¿Negativos o no enteros?                   | `ValueError`                               | `_validar_cantidad()`   |
| A8  | ¿Sacar más de lo que hay?                  | `ValueError`, carrito intacto              | `sacar()`               |
| A9  | ¿Sacar lo que no está?                     | `ValueError`                               | `sacar()`               |
| A10 | ¿Consultar lo que no está?                 | Devuelve `0`                               | `cuanto_hay()`          |
| A11 | ¿Carrito recién creado?                    | Todo en `0`                                | `__init__()`            |
| A12 | ¿Un carrito o varios?                      | Uno independiente por instancia            | `__init__()`            |

### 3.2 Las cuatro que nacen de la frase del administrador

Estas son las importantes, porque cambian **qué sistema se construye**.

**A1 — «cuánto llevo en total»: unidades o dinero.** En español las dos lecturas
son válidas: «llevo 7» y «llevo $32.000» se dicen igual. Se decidió **unidades**
porque el requisito **nunca menciona precios**. Elegir dinero habría obligado a
inventar un catálogo, un tipo numérico para la moneda, una política de IVA y otra
de redondeo, es decir, a inventar requisitos que nadie pidió. La otra lectura no
se descarta: queda escrita en el documento y declarada fuera de alcance, de modo
que si el administrador confirma que quería dinero, lo que se hace es **agregar**
`total_a_pagar()`, no cambiarle el significado a `cuanto_llevo()`.

**A2 — «cuántos hay de cada uno»: dónde.** «Hay» puede ser en el carrito o en la
bodega. Se decidió **el carrito**, porque las otras tres operaciones son todas
sobre el carrito. La otra lectura no es una función más: es un segundo TAD
(inventario) con validación de disponibilidad y descuento de existencias.

**A3 — qué identifica a un producto.** Si la clave fuera el texto exacto que
escribe el cajero, `"Pan"`, `"pan"` y `" pan "` serían tres productos distintos y
la pregunta de A2 quedaría sin sentido: el mismo pan repartido en tres renglones.
Se decidió normalizar (espacios y mayúsculas) pero **no quitar tildes**, porque
recortar espacios corrige un error de digitación mientras que quitar tildes puede
fusionar productos que de verdad son distintos.

**A4 — meter algo que ya está.** Se acumula. La razón está en el propio requisito:
pedir «cuántos hay **de cada uno**» ya asume una cantidad por producto.

### 3.3 Las ocho de los casos extremos

Son las que nadie menciona al hablar pero que el programa encuentra el primer día:
cantidad cero (A6), negativos y no enteros (A7), sacar de más (A8), sacar lo que
no está (A9), consultar lo que no está (A10), carrito vacío (A11) e independencia
entre carritos (A12).

Dos merecen comentario:

**La asimetría entre A9 y A10** parece una contradicción y no lo es. `sacar` un
producto ausente lanza error, pero `cuanto_hay` de un producto ausente devuelve
`0`. La diferencia es entre **ordenar** y **preguntar**: una orden imposible no se
puede ejecutar, pero una pregunta sobre algo ausente sí tiene respuesta correcta,
y devolverla permite usar el resultado en una suma sin envolver cada consulta en
un `try`.

**A5, el producto que llega a cero, desaparece.** Si existieran los dos estados
—"ausente" y "presente con cantidad 0"— habría **dos representaciones del mismo
carrito**, y toda operación futura tendría que acordarse de contemplar las dos. Es
una fuente clásica de errores que se elimina prohibiendo el estado redundante.

### 3.4 El contrato resultante

| Operación                 | Devuelve | Falla con `ValueError` cuando…                                   |
| ------------------------- | -------- | ---------------------------------------------------------------- |
| `Carrito()`               | —        | nunca                                                            |
| `meter(producto, cantidad)` | `None`  | producto inválido; cantidad no entera, cero o negativa            |
| `sacar(producto, cantidad)` | `None`  | lo anterior; producto ausente; cantidad mayor que la disponible   |
| `cuanto_hay(producto)`    | `int`    | producto inválido                                                |
| `cuanto_llevo()`          | `int`    | nunca                                                            |

### 3.5 El invariante

El **invariante de representación** es lo que siempre es cierto del carrito, pase
lo que pase. Se cumple al crearlo y ninguna operación lo rompe:

1. toda cantidad guardada es un entero **≥ 1** (nunca 0, nunca negativa);
2. **no hay dos entradas para el mismo producto**;
3. `cuanto_llevo()` es exactamente la suma de las cantidades guardadas;
4. el almacenamiento **pertenece a la instancia** y no se comparte con otra.

El punto 4 es el que el código anterior violaba.

---

## 4. El código, explicado línea por línea

Las dos implementaciones cumplen el mismo contrato con estructuras distintas:

```python
# carrito_dict.py                    # carrito_lista.py
{"pan": 5, "leche": 2}               [("pan", 5), ("leche", 2)]
```

### 4.1 La estructura de cada archivo

Los dos archivos tienen exactamente la misma organización:

```
Docstring del módulo   ← representación, por qué esa estructura, costos, invariante
class Carrito
├── __init__               construcción
├── _clave                 validación + normalización del nombre   (privado)
├── _validar_cantidad      validación de la cantidad               (privado)
├── _buscar_indice         solo en la versión con lista            (privado)
├── meter                  ─┐
├── sacar                   │ las cuatro operaciones del contrato
├── cuanto_hay              │
├── cuanto_llevo           ─┘
└── __repr__               ayuda de depuración (no contractual)
```

El guion bajo inicial (`_clave`, `_productos`) es la convención de Python para
decir «esto es interno, no forma parte de lo que se promete». No lo impide el
lenguaje: es un acuerdo entre programadores.

### 4.2 `__init__` — la línea que evita el error

```python
def __init__(self) -> None:
    self._productos: dict[str, int] = {}     # carrito_dict.py
    self._productos: list[tuple[str, int]] = []   # carrito_lista.py
```

Parece la línea más trivial del proyecto y es la más importante. El contenedor se
crea **dentro del constructor**, así que se ejecuta **una vez por cada carrito**:
dos llamadas a `Carrito()` producen dos contenedores distintos.

Las dos formas de escribirlo mal son exactamente el error del código anterior:

```python
class Carrito:
    _productos = {}                       # MAL: vive en la clase, lo comparten todos

    def __init__(self, productos={}):     # MAL: se evalúa una sola vez
        self._productos = productos
```

Hay una segunda decisión, esta por omisión: **el constructor no recibe ningún
contenedor desde afuera**. No hay parámetro por el que se pueda colar una
referencia ajena. Esa ausencia es deliberada.

La anotación `dict[str, int]` no cambia el comportamiento —Python no la verifica en
ejecución— pero documenta el contenido: claves de texto, valores enteros.

### 4.3 `_clave` — cómo se normaliza un nombre

```python
@staticmethod
def _clave(producto: object) -> str:
    if not isinstance(producto, str):
        raise ValueError(
            "El producto debe ser una cadena de texto; se recibió "
            f"{type(producto).__name__}."
        )

    clave = " ".join(producto.split()).lower()

    if not clave:
        raise ValueError("El nombre del producto no puede estar vacío.")

    return clave
```

Es un `@staticmethod` porque no necesita mirar el carrito: convierte un texto en
otro. Recibe `object` y no `str` en la anotación justamente porque su trabajo es
comprobar que sea `str`.

La línea del medio hace tres cosas seguidas:

| Paso                   | Resultado con `"  Pan   Integral "` |
| ---------------------- | ----------------------------------- |
| `producto.split()`     | `['Pan', 'Integral']`               |
| `" ".join(...)`        | `'Pan Integral'`                    |
| `.lower()`             | `'pan integral'`                    |

`split()` **sin argumentos** es la clave del truco: separa por cualquier bloque de
espacios y descarta los vacíos, así que recortar los extremos y colapsar los
espacios internos salen de una sola operación. Con `split(" ")` habría que limpiar
los `''` a mano.

La comprobación final atrapa `""` y `"   "`, que sobreviven a la normalización
convertidos en cadena vacía y no identifican ningún producto.

**Por qué el mensaje de error dice el tipo recibido:** `type(producto).__name__`
produce `'NoneType'`, `'int'`, `'list'`. Un mensaje que dice *qué* llegó mal ahorra
el trabajo de averiguarlo.

### 4.4 `_validar_cantidad` — y la trampa de `True`

```python
@staticmethod
def _validar_cantidad(cantidad: object) -> None:
    if isinstance(cantidad, bool) or not isinstance(cantidad, int):
        raise ValueError(
            "La cantidad debe ser un número entero; se recibió "
            f"{type(cantidad).__name__}."
        )

    if cantidad < 1:
        raise ValueError(
            f"La cantidad debe ser mayor o igual a 1; se recibió {cantidad}."
        )
```

La primera condición tiene una parte que parece sobrar y no sobra. En Python:

```python
isinstance(True, int)   # True   <- bool ES subclase de int
True == 1               # True
True + True             # 2
```

Sin el `isinstance(cantidad, bool)`, la llamada `meter("pan", True)` pasaría todas
las validaciones y metería **una unidad de pan**, en silencio. Como `True` casi
nunca aparece ahí a propósito —suele venir de una variable que se creía numérica—
rechazarlo convierte un error invisible en uno visible.

Las dos comprobaciones están separadas a propósito: la primera responde «esto no
es un número entero», la segunda «es entero pero no sirve». Son diagnósticos
distintos y merecen mensajes distintos.

### 4.5 El orden de las validaciones **es** la atomicidad

La decisión A8 dice que una operación que falla deja el carrito **exactamente como
estaba**. Eso no se implementa con `try`/`except` ni deshaciendo cambios: se
implementa **validando todo antes de tocar nada**.

En `sacar`, el orden es:

```
1. _clave(producto)            ← puede lanzar
2. _validar_cantidad(cantidad) ← puede lanzar
3. buscar cuánto hay disponible
4. ¿el producto existe?        ← puede lanzar
5. ¿alcanza la cantidad?       ← puede lanzar
6. ───── recién aquí se modifica el carrito ─────
```

Los cinco puntos donde puede fallar están **antes** del único punto donde se
escribe. Por eso no hay forma de que una excepción deje el carrito a medias. Es
más simple y más confiable que corregir después.

### 4.6 `carrito_dict.py`, operación por operación

**`meter`**

```python
clave = self._clave(producto)
self._validar_cantidad(cantidad)
self._productos[clave] = self._productos.get(clave, 0) + cantidad
```

La última línea unifica los dos casos —producto nuevo y producto que ya estaba— en
una sola expresión. `.get(clave, 0)` devuelve la cantidad actual **o `0` si la
clave no existe**, así que "empezar de cero" y "sumar a lo que había" son la misma
operación. Sin `.get` habría un `if` de cuatro líneas.

**`sacar`**

```python
clave = self._clave(producto)
self._validar_cantidad(cantidad)

disponible = self._productos.get(clave, 0)

if disponible == 0:
    raise ValueError(f"El producto '{clave}' no está en el carrito.")

if cantidad > disponible:
    raise ValueError(
        f"No se pueden sacar {cantidad} unidades de '{clave}': solo hay {disponible}."
    )

restante = disponible - cantidad

if restante == 0:
    del self._productos[clave]
else:
    self._productos[clave] = restante
```

Aquí `disponible == 0` **equivale a** «el producto no está», y eso es consecuencia
directa del invariante: como nunca se guarda una cantidad 0, la única forma de que
`.get` devuelva 0 es que la clave no exista. Una sola consulta responde dos
preguntas.

El `del` del final es lo que sostiene el punto 1 del invariante: el producto que
llega a cero se borra, no se queda en 0.

**`cuanto_hay`**

```python
return self._productos.get(self._clave(producto), 0)
```

Una línea que hace tres cosas: valida y normaliza el nombre, busca, y devuelve `0`
si no está (A10). Se lee de adentro hacia afuera.

**`cuanto_llevo`**

```python
return sum(self._productos.values())
```

`.values()` da las cantidades sin las claves, y `sum` las suma. Sobre el carrito
vacío devuelve `0`, que es justo lo que pide A11, sin ningún caso especial.

Aquí hay una decisión de diseño que vale la pena mirar: **se recalcula en cada
llamada**. La alternativa sería guardar un atributo `self._total` y mantenerlo al
día, lo que bajaría el costo de O(n) a O(1). No se hizo, porque un total guardado
es **estado duplicado**: la misma información en dos lugares, que pueden dejar de
coincidir si alguna operación futura olvida actualizarlo. Para un carrito de
campus, con decenas de productos, se prefiere el dato que siempre es correcto
sobre el dato que es rápido.

**`__repr__`**

```python
return f"{type(self).__name__}({self._productos!r})"
```

Se usa cuando se escribe el objeto en la consola y, sobre todo, cuando pytest
informa un fallo. El `!r` aplica `repr()` al contenido, así que las cadenas salen
con comillas. Muestra la estructura interna a propósito: al leer un error se ve de
inmediato si es la versión con llaves (dict) o con corchetes (lista).

Está declarado **fuera del contrato** y ninguna prueba depende de su formato.

### 4.7 `carrito_lista.py`, operación por operación

La diferencia de fondo: **la lista no tiene acceso por clave**. Todo empieza por
buscar.

**`_buscar_indice`**

```python
def _buscar_indice(self, clave: str) -> int | None:
    for indice, (nombre, _cantidad) in enumerate(self._productos):
        if nombre == clave:
            return indice
    return None
```

Es la búsqueda lineal que el diccionario no necesita hacer, y el único motivo de
que esta versión sea O(n) donde la otra es O(1).

Dos detalles de Python: `enumerate` entrega la posición junto con el elemento, y
`(nombre, _cantidad)` **desempaqueta** la tupla directamente en el `for`. El guion
bajo delante de `_cantidad` avisa que ese valor no se va a usar.

Devuelve `None` —y no `-1`— cuando no encuentra, porque `-1` es un índice válido en
Python (el último elemento) y confundirlos es un error clásico.

**`meter`**

```python
indice = self._buscar_indice(clave)

if indice is None:
    self._productos.append((clave, cantidad))
else:
    _nombre, cantidad_actual = self._productos[indice]
    self._productos[indice] = (clave, cantidad_actual + cantidad)
```

Aquí se ve el trabajo que el diccionario hacía gratis: **buscar antes de agregar**
es lo único que impide que queden dos pares `("pan", …)` en la lista. Si esa
búsqueda se olvidara, el carrito tendría dos renglones de pan y `cuanto_hay`
devolvería solo el primero. El punto 2 del invariante, que el diccionario regala
por construcción, aquí hay que sostenerlo a mano.

**Por qué tuplas y no listas de dos elementos:** las tuplas son inmutables, así que
la cantidad no se modifica en el sitio; el par se **reemplaza completo**. Eso evita
que alguien que se haya guardado una referencia al par pueda alterar el carrito por
detrás — que es, en pequeño, el mismo problema de la autopsia.

**`sacar`**

```python
indice = self._buscar_indice(clave)

if indice is None:
    raise ValueError(f"El producto '{clave}' no está en el carrito.")

_nombre, disponible = self._productos[indice]

if cantidad > disponible:
    raise ValueError(...)

restante = disponible - cantidad

if restante == 0:
    self._productos.pop(indice)
else:
    self._productos[indice] = (clave, restante)
```

Mismo contrato, mismos errores, mismos mensajes. La diferencia: `pop(indice)` no
solo elimina, además **desplaza una posición** todos los pares que venían después,
que es trabajo extra que `del diccionario[clave]` no hace.

**`cuanto_llevo`**

```python
return sum(cantidad for _nombre, cantidad in self._productos)
```

Una expresión generadora que descarta el nombre y suma las cantidades. No construye
ninguna lista intermedia: va entregando los valores a `sum` uno por uno.

### 4.8 La misma secuencia, en las dos estructuras

Traza real de estado, ejecutada sobre las dos implementaciones a la vez:

| Operación               | `carrito_dict`                    | `carrito_lista`                       |
| ----------------------- | --------------------------------- | ------------------------------------- |
| `Carrito()`             | `{}`                              | `[]`                                  |
| `meter('pan', 2)`       | `{'pan': 2}`                      | `[('pan', 2)]`                        |
| `meter('Pan', 3)`       | `{'pan': 5}`                      | `[('pan', 5)]`                        |
| `meter('  LECHE ', 1)`  | `{'pan': 5, 'leche': 1}`          | `[('pan', 5), ('leche', 1)]`          |
| `sacar('pan', 5)`       | `{'leche': 1}`                    | `[('leche', 1)]`                      |
| `meter('pan', 4)`       | `{'leche': 1, 'pan': 4}`          | `[('leche', 1), ('pan', 4)]`          |
| `cuanto_llevo()`        | `5`                               | `5`                                   |

Lo que se ve en esa tabla:

- **Fila 3:** `'Pan'` se acumuló sobre `'pan'` (A3 + A4). No apareció un segundo
  renglón.
- **Fila 4:** `'  LECHE '` se guardó como `'leche'` (A3).
- **Fila 5:** al llegar a 0, `'pan'` **desapareció** (A5).
- **Fila 6:** al volver a meterlo, se comporta como producto nuevo y queda al
  final. El TAD **no promete ningún orden**, y por eso ninguna prueba lo asume.
- **Última fila:** el comportamiento observable es idéntico. Eso es cumplir el
  mismo contrato.

---

## 5. Las pruebas, explicadas

### 5.1 Cómo un solo archivo prueba dos implementaciones

La restricción de la actividad es clara: **un solo archivo de pruebas, sin
modificarlo entre una implementación y la otra**. El mecanismo que lo permite son
las *fixtures parametrizadas* de pytest.

```python
IMPLEMENTACIONES = [CarritoLista, CarritoDict]

@pytest.fixture(params=IMPLEMENTACIONES, ids=["lista", "dict"])
def clase_carrito(request):
    return request.param          # devuelve la CLASE

@pytest.fixture
def carrito(clase_carrito):
    return clase_carrito()        # devuelve una INSTANCIA nueva
```

Una **fixture** es un preparativo que pytest arma antes de cada prueba. Cuando una
prueba declara `def test_algo(carrito)`, pytest ve que necesita `carrito`, lo
construye y se lo pasa.

Lo interesante es el `params=`: cuando una fixture está parametrizada, pytest
ejecuta **cada prueba que dependa de ella una vez por cada parámetro**. Y esa
parametrización **se propaga**: `carrito` depende de `clase_carrito`, así que
hereda las dos variantes sin declarar nada.

```
test_meter_producto_y_consultar_cantidad
├── [lista]  → carrito = CarritoLista()
└── [dict]   → carrito = CarritoDict()
```

Los `ids=["lista", "dict"]` son lo que hace legible la salida de `pytest -v`. Sin
ellos aparecerían nombres de clase completos.

Hay dos fixtures y no una porque **algunas pruebas necesitan crear más de un
carrito** —las de independencia entre cajas—, y para eso les hace falta la clase,
no una instancia ya construida.

**Nada en el archivo de pruebas menciona listas ni diccionarios.** Todo se expresa
con las cuatro operaciones del contrato. Esa es la razón de que el mismo archivo
sirva para las dos.

### 5.2 Aislamiento entre pruebas

pytest reconstruye las fixtures **para cada prueba**, no una vez para todas. Cada
caso arranca con un carrito recién creado, así que ninguna prueba puede contaminar
a otra ni el resultado puede depender del orden de ejecución.

### 5.3 Qué cubre cada bloque

| Bloque                          | Casos | Qué verifica                                                    |
| ------------------------------- | ----- | ---------------------------------------------------------------- |
| 1. Carrito vacío                | 2     | A11 — el caso base no es un caso especial                        |
| 2. Meter                        | 4     | A4 — acumulación, productos separados, unidad por unidad         |
| 3. Sacar                        | 6     | A5, A9 — reducir, vaciar, no afectar a otros, volver a meter     |
| 4. Consultar                    | 2     | A10 — devuelve 0 y **no crea** el producto al preguntar          |
| 5. Identidad del producto       | 12    | A3 — mayúsculas, espacios, tildes, nombres inválidos             |
| 6. Cantidades inválidas         | 11    | A6, A7 — cero, negativos, no enteros, `True`/`False`             |
| 7. Atomicidad                   | 4     | A8 — el carrito queda intacto y sigue usable tras un error       |
| 8. Independencia entre carritos | 5     | A12 — **el error de la autopsia**                                |
|                                 | **46**| por implementación → **92** en total                             |

### 5.4 Los casos extremos que pedía la actividad

Los tres exigidos explícitamente están cubiertos, y con más de un caso cada uno:

- **Carrito vacío:** `test_carrito_nuevo_esta_vacio`,
  `test_carrito_nuevo_no_tiene_ningun_producto`,
  `test_sacar_de_un_carrito_vacio_falla`.
- **Sacar lo que no está:** `test_sacar_producto_que_no_esta_falla`,
  `test_sacar_de_un_carrito_vacio_falla`.
- **Cantidad cero:** `test_cantidad_cero_al_meter_falla`,
  `test_cantidad_cero_al_sacar_falla`, y el caso `False` de
  `test_cantidad_que_no_es_entero_falla`.

### 5.5 Las pruebas que vigilan el error de las dos cajas

Este bloque es la contraparte ejecutable de [`autopsia.md`](autopsia.md): son las
pruebas que habrían atrapado el error **antes** de que llegara a la tienda.

| Prueba                                                      | Qué bloquea                                    |
| ----------------------------------------------------------- | ---------------------------------------------- |
| `test_dos_carritos_recien_creados_son_independientes`        | el síntoma: lo que se mete en una caja se ve en la otra |
| `test_las_operaciones_de_una_caja_no_se_filtran_a_la_otra`   | la versión con las dos cajas trabajando a la vez |
| `test_cada_carrito_tiene_su_propio_almacenamiento`           | la causa: el alias entre instancias            |
| `test_la_clase_no_guarda_contenedores_mutables`              | la variante con atributo de clase              |
| `test_el_constructor_no_tiene_valores_por_omision_mutables`  | la variante con valor por omisión mutable      |

Las tres últimas merecen explicación porque hacen algo poco común: **inspeccionan
el objeto en vez de usarlo**.

```python
contenedores_1 = [v for v in vars(caja_1).values() if isinstance(v, (list, dict, set))]
contenedores_2 = [v for v in vars(caja_2).values() if isinstance(v, (list, dict, set))]

for propio, ajeno in zip(contenedores_1, contenedores_2):
    assert propio is not ajeno
```

`vars(objeto)` devuelve los atributos de la instancia. La prueba recorre los que
son contenedores mutables **sin saber cómo se llaman** —por eso funciona para
cualquier implementación futura— y exige que los de un carrito **no sean el mismo
objeto** que los del otro. Es la traducción a código de la comprobación
`caja_1._productos is caja_2._productos` de la autopsia.

```python
por_omision = clase_carrito.__init__.__defaults__ or ()
assert not any(isinstance(valor, (list, dict, set)) for valor in por_omision)
```

`__defaults__` es donde Python guarda los valores por omisión de una función. Si
alguien escribiera `def __init__(self, productos={})`, el diccionario aparecería
ahí y la prueba fallaría. Es el error del código anterior, atrapado en su origen.

**Por qué `is not` y no `!=`:** `!=` compara **contenido** y dos diccionarios
vacíos distintos son iguales (`{} == {}` es `True`). `is not` compara **identidad**,
que es exactamente lo que se quiere verificar: que no sean el mismo objeto.

### 5.6 Los doctests

Además de las 92 pruebas, los docstrings del código contienen ejemplos ejecutables:

```python
>>> carrito = Carrito()
>>> carrito.meter("pan", 2)
>>> carrito.meter("Pan", 3)
>>> carrito.cuanto_hay("PAN")
5
```

Se pueden ejecutar como pruebas de verdad:

```bash
python -m pytest --doctest-modules carrito_lista.py carrito_dict.py -q
```

Su valor no es la cobertura —eso ya lo dan las 92— sino que **la documentación no
puede quedar desactualizada sin que alguien se entere**: si el comportamiento
cambia, el ejemplo del docstring falla.

---

## 6. El error de las dos cajas

El diagnóstico completo, con las tres versiones del diagrama de memoria, está en
[`autopsia.md`](autopsia.md). Resumen:

**El código.**

```python
class Caja:
    def __init__(self, nombre, productos={}):   # <-- el error
        self.nombre = nombre
        self.productos = productos
```

**La evidencia**, salida real del intérprete:

```
caja_1 is caja_2                     = False          ← las cajas SÍ son distintas
caja_1.productos is caja_2.productos = True           ← el diagnóstico
id(Caja.__init__.__defaults__[0])    = 0x1b227d37c00  ← y viene de aquí
```

**El diagrama.**

```text
    caja_1 ────────►  ┌───────────────────────────┐
                      │  Caja             @…61640 │
                      │  productos ───────────────┼──────┐
                      └───────────────────────────┘      │
                                                         ▼
                                                ┌──────────────────┐
                                                │ dict     @…37c00 │
                                                │   {'pan': 2}     │
                                                └──────────────────┘
                                                         ▲
    caja_2 ────────►  ┌───────────────────────────┐      │
                      │  Caja             @…616a0 │      │
                      │  productos ───────────────┼──────┘
                      └───────────────────────────┘
```

**La explicación en tres pasos:**

1. En Python, una variable **no contiene** un objeto: lo señala. `self.productos =
   productos` no copia el diccionario, **copia la dirección**.
2. Los valores por omisión se evalúan **una sola vez**, cuando se define la
   función. Ese `{}` es un objeto único guardado dentro de `__init__`, que se
   presta a todas las cajas.
3. `meter` **modifica el diccionario en el sitio**. No crea uno nuevo: escribe
   dentro del objeto compartido, y las dos cajas lo ven.

Lo que hace difícil de encontrar el error es que **las cajas de verdad son
objetos distintos**. Lo compartido está un nivel más abajo.

**El detalle que cierra el argumento:** como el diccionario contaminado es el valor
por omisión de la función, una caja creada después nace con el pan de otro cliente.

```python
caja_3 = Caja("Caja 3")
caja_3.productos        # {'pan': 2}
```

**La corrección:**

```python
def __init__(self, nombre, productos=None):
    self.nombre = nombre
    self.productos = {} if productos is None else dict(productos)
```

`None` es inmutable, así que compartirlo no hace daño; y el `{}` ahora se evalúa en
**cada** llamada. En el TAD entregado el problema ni siquiera puede plantearse: el
constructor no recibe contenedores.

---

## 7. Complejidad: la teoría y el cronómetro

### 7.1 Lo que dice la teoría

Con `n` = número de productos **distintos** en el carrito:

| Operación      | `carrito_lista.py` | `carrito_dict.py` | Por qué                                     |
| -------------- | ------------------ | ----------------- | ------------------------------------------- |
| `meter`        | O(n)               | O(1) promedio     | la lista busca recorriendo; el dict calcula la posición |
| `sacar`        | O(n)               | O(1) promedio     | igual, y `pop` además desplaza              |
| `cuanto_hay`   | O(n)               | O(1) promedio     | igual                                       |
| `cuanto_llevo` | O(n)               | O(n)              | las dos suman todo: no hay atajo            |

La notación **O(...)** describe cómo crece el tiempo cuando crecen los datos, no
cuánto tarda. **O(1)** significa que el tiempo no depende del tamaño; **O(n)**, que
crece proporcionalmente.

El diccionario logra O(1) con una **tabla hash**: convierte la clave en un número
que indica dónde mirar, sin recorrer nada. Se dice "promedio" porque en el peor
caso —muchas claves cayendo en la misma posición— puede degradarse.

### 7.2 Lo que dice el cronómetro

Medición real sobre estas dos implementaciones (Python 3.12, Windows):

**Llenar el carrito con `n` productos distintos**

| n     | lista     | dict    | lista/dict |
| ----- | --------- | ------- | ---------- |
| 10    | 0.03 ms   | 0.01 ms | 2×         |
| 100   | 0.34 ms   | 0.08 ms | 4×         |
| 1 000 | 30.15 ms  | 0.85 ms | 35×        |
| 5 000 | 766.36 ms | 3.84 ms | **200×**   |

**2 000 consultas del producto que está al final (peor caso de la lista)**

| n     | lista       | dict    | lista/dict |
| ----- | ----------- | ------- | ---------- |
| 10    | 2.13 ms     | 0.81 ms | 3×         |
| 100   | 12.56 ms    | 0.85 ms | 15×        |
| 1 000 | 121.92 ms   | 0.85 ms | 144×       |
| 5 000 | 1 388.39 ms | 2.50 ms | **554×**   |

### 7.3 Cómo se leen esas tablas

**La columna del diccionario es plana.** De n=10 a n=5 000 —quinientas veces más
productos— el tiempo de consulta pasa de 0.81 ms a 2.50 ms. Eso es O(1) medido: el
tamaño del carrito casi no influye.

**La columna de la lista crece con n.** En la segunda tabla, cada vez que `n` se
multiplica por 10, el tiempo se multiplica por 10: 12.56 → 121.92 → 1 388.39. Eso
es O(n) medido, tan limpio como en el libro.

**Y llenar la lista es O(n²).** La primera tabla lo muestra: de n=1 000 a n=5 000
el tamaño se multiplica por 5, pero el tiempo se multiplica por **25** (30 ms →
766 ms). Tiene sentido: llenar son `n` llamadas a `meter`, y cada una cuesta O(n),
así que el total es n × n. Es el patrón de rendimiento que hace que un programa
funcione perfecto en pruebas y se caiga en producción.

### 7.4 Entonces, ¿la lista es mala?

No, y conviene decirlo con precisión:

- **Con pocos productos da igual.** En n=10 la diferencia es de centésimas de
  milisegundo. Un carrito de campus real tiene 5 o 20 productos: cualquiera de las
  dos sirve, y elegir por rendimiento ahí sería optimización prematura.
- **La lista conserva el orden de inserción** de forma natural. Este TAD no promete
  ningún orden, así que la ventaja no se usa, pero existiría si el requisito lo
  pidiera.
- **La lista enseña algo que el diccionario esconde:** el trabajo de garantizar que
  no haya claves repetidas. En `carrito_lista.py` ese trabajo se ve escrito; en
  `carrito_dict.py` lo hace la estructura.

**La elección para producción es el diccionario**, porque la operación que el TAD
hace todo el tiempo —buscar un producto por su nombre— es exactamente la que el
diccionario resuelve en O(1).

### 7.5 Nota sobre `collections.Counter`

La actividad prohíbe usarlo, y la razón es exactamente lo que se acaba de recorrer:
`Counter` es un diccionario de cuentas con valor por omisión, y habría resuelto el
ejercicio en una línea sin que nadie viera qué hay debajo.

---

## 8. Cómo ejecutar y verificar todo

**Requisitos:** Python 3.10 o superior y pytest. El mínimo lo fija la anotación
`int | None` de `_buscar_indice`, que es sintaxis introducida en 3.10.

```bash
python -m pip install pytest
```

**Las 92 pruebas:**

```bash
python -m pytest -q
```

**Ver qué implementación corre cada caso** (aparecen como `[lista]` y `[dict]`):

```bash
python -m pytest -v
```

**Los ejemplos de la documentación:**

```bash
python -m pytest --doctest-modules carrito_lista.py carrito_dict.py -q
```

**El historial de Git:**

```bash
git log --oneline --decorate
```

**Comprobar que las pruebas estaban en rojo antes de la implementación:**

```bash
git checkout bc82066 && python -m pytest -q
```

Para regresar:

```bash
git checkout main
```

Un detalle sobre esa comprobación: el ejercicio vive en `actividad_carrito/` del
repositorio del curso, pero sus commits se crearon cuando era un repositorio
propio. Al volver a `bc82066` el árbol de trabajo queda con `spec.md` y
`test_carrito.py` **en la raíz** (y `clase1/`, `clase2/`, `actividad_carrito/`
desaparecen hasta que regreses a `main`), así que pytest se ejecuta desde ahí.

La salida literal de todas estas ejecuciones está guardada en
[`VERIFICACION.txt`](VERIFICACION.txt).

---

## 9. Glosario

**TAD (Tipo Abstracto de Datos).** Definición de un tipo por **sus operaciones y
lo que garantizan**, sin decir cómo se guardan los datos. Permite cambiar la
estructura interna sin que ningún usuario del tipo se entere.

**Contrato.** El conjunto de precondiciones, postcondiciones y errores de cada
operación. Es lo que promete el TAD.

**Precondición.** Lo que tiene que ser cierto **antes** de llamar a una operación
para que funcione. Ejemplo: la cantidad debe ser un entero ≥ 1.

**Postcondición.** Lo que queda garantizado **después**. Ejemplo: tras `meter`, la
cantidad del producto aumentó exactamente en lo que se pidió.

**Invariante de representación.** Lo que es cierto del objeto **siempre**, entre
una operación y otra. Ejemplo: nunca hay una cantidad guardada en 0.

**Atomicidad.** Que una operación se aplique completa o no se aplique. Si falla, no
deja el estado a medias.

**Mutable / inmutable.** Un objeto mutable se puede modificar sin crear uno nuevo
(listas, diccionarios, conjuntos). Uno inmutable no (enteros, cadenas, tuplas,
`None`). Es la propiedad en el centro del error de las dos cajas: **solo los
objetos mutables pueden producirlo**.

**Referencia.** Lo que una variable guarda en realidad: la dirección de un objeto,
no el objeto. Por eso `a = b` no copia.

**Alias.** Dos nombres que señalan **el mismo objeto**. Modificar por uno se ve por
el otro. Se detecta con `is`, no con `==`.

**`is` vs `==`.** `==` pregunta si el **contenido** es igual; `is` pregunta si son
**el mismo objeto**. Dos diccionarios vacíos distintos cumplen `==` pero no `is`.

**O(1), O(n), O(n²).** Cómo crece el tiempo al crecer los datos: constante,
proporcional, o proporcional al cuadrado.

**Tabla hash.** La estructura bajo el diccionario: convierte la clave en un número
que dice dónde mirar, evitando recorrer.

**Fixture (pytest).** Preparativo que pytest construye antes de cada prueba y le
entrega como argumento.

**Fixture parametrizada.** Fixture con varios valores; pytest repite cada prueba
que dependa de ella una vez por valor. Es lo que permite probar dos
implementaciones con un solo archivo.

**Doctest.** Ejemplo escrito en un docstring con `>>>` que se puede ejecutar como
prueba, de modo que la documentación no se desactualice en silencio.

**Rojo / verde.** Estados de la batería de pruebas: rojo cuando alguna falla, verde
cuando todas pasan. La secuencia rojo → verde es la evidencia de que la prueba se
escribió antes que el código.

---

## 10. Mapa: requisito de la actividad → dónde está resuelto

| Lo que pedía la actividad                                          | Dónde está                                                      | Estado |
| ------------------------------------------------------------------ | --------------------------------------------------------------- | ------ |
| `spec.md` con el contrato del TAD                                   | [`spec.md`](spec.md) §4                                          | ✅ |
| Cuatro o más ambigüedades, cada una con su razón                    | [`spec.md`](spec.md) §2 y §3 — **12 decididas**                  | ✅ |
| `test_carrito.py` con la batería de pruebas                         | [`test_carrito.py`](test_carrito.py) — 46 casos × 2 = **92**     | ✅ |
| Caso extremo: carrito vacío                                         | bloque 1 y `test_sacar_de_un_carrito_vacio_falla`                | ✅ |
| Caso extremo: sacar lo que no está                                  | `test_sacar_producto_que_no_esta_falla`                          | ✅ |
| Caso extremo: cantidad cero                                         | `test_cantidad_cero_al_meter_falla`, `..._al_sacar_falla`        | ✅ |
| `carrito_lista.py` y `carrito_dict.py` del mismo contrato           | ambos archivos, mismo `test_carrito.py` sin modificar            | ✅ |
| `autopsia.md` con el diagnóstico                                    | [`autopsia.md`](autopsia.md) §1–§9                               | ✅ |
| Los **dos** diagramas de memoria                                    | [`autopsia.md`](autopsia.md) §4, §7 y §10 — **tres**             | ✅ |
| La corrección explicada                                             | [`autopsia.md`](autopsia.md) §9–§12                              | ✅ |
| Historial de Git: pruebas en rojo antes de la implementación        | commits `bc82066` → `cac09f8`, auditable con `git checkout`      | ✅ |
| **Restricción:** sin `collections.Counter`                          | ninguna implementación importa nada                              | ✅ |
| **Restricción:** un solo archivo de pruebas, sin modificar          | fixture parametrizada; nada en él menciona lista ni diccionario  | ✅ |
| **Restricción:** diagramas con flechas entre variables y objetos    | los tres diagramas de `autopsia.md`                              | ✅ |
