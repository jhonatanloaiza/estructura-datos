# Especificación del TAD `Carrito`

> Documento de decisiones. Se escribe **antes** de programar y es el que manda:
> si el código y este documento no coinciden, el que está mal es el código.

---

## 1. El requisito, tal como llegó

El administrador de la tienda del campus escribió:

> «necesito poder meter productos, sacar productos, saber cuántos hay de cada uno
> y cuánto llevo en total»

La frase se entiende al leerla, pero **no alcanza para programar**: tiene cuatro
verbos y ninguno dice qué pasa en los casos que sí ocurren en una caja real. Antes
de escribir una línea de código hay que convertir esa frase en un contrato sin
huecos.

Este documento hace exactamente eso: primero enumera las ambigüedades y las decide
con su razón, y después escribe el contrato que sale de esas decisiones.

---

## 2. Ambigüedades del enunciado

Son las que nacen de las palabras que el administrador realmente usó.

### A1. «cuánto llevo en total»: ¿unidades o dinero?

**Las dos lecturas son válidas en español.** «Llevo 7» (artículos) y «llevo
$32.000» (a pagar) se dicen igual.

**Decisión:** `cuanto_llevo()` devuelve el **número total de unidades**.

**Razón:** el requisito **nunca menciona precios**. Devolver dinero obligaría a
inventar un catálogo de precios, un tipo numérico para la moneda, una política de
IVA y otra de redondeo, es decir, a inventar requisitos que nadie pidió. Se elige
la lectura que el enunciado sí puede sostener y se deja constancia escrita de la
otra.

**Consecuencia:** el total en dinero queda **fuera de alcance** (§7). Si mañana el
administrador confirma que quería dinero, la operación que se agrega es
`total_a_pagar()`; `cuanto_llevo()` no cambia de significado.

### A2. «saber cuántos hay de cada uno»: ¿cuántos hay dónde?

**Lectura A:** cuántas unidades lleva el cliente **en el carrito**.
**Lectura B:** cuántas unidades **le quedan a la tienda** (inventario).

**Decisión:** Lectura A, el carrito.

**Razón:** el TAD que se pidió se llama carrito y las otras tres operaciones son
todas sobre el carrito. La Lectura B exigiría una segunda estructura (el
inventario), validar disponibilidad al meter y descontar existencias al vender: es
otro sistema, no otra función.

**Consecuencia:** el TAD **no valida stock**. `meter("pan", 1000)` es válido aunque
la tienda tenga 3 panes.

### A3. ¿Qué identifica a un producto?

El requisito dice «productos» sin decir cómo se nombran. Si la clave fuera la
cadena exacta escrita por el cajero, `"Pan"`, `"pan"` y `" pan "` serían **tres
productos distintos** y la operación de A2 quedaría sin sentido: el mismo pan
aparecería repartido en tres renglones.

**Decisión:** el producto se identifica por una **cadena no vacía**, y la clave es
esa cadena **normalizada**:

1. se recortan los espacios de los extremos y se colapsan los espacios internos
   (`"  pan   integral "` se vuelve `"pan integral"`);
2. se pasa a minúsculas (`"Pan Integral"` se vuelve `"pan integral"`).

**No se quitan tildes:** `"café"` y `"cafe"` son productos distintos.

**Razón:** los dos primeros pasos corrigen errores de digitación que no cambian el
producto (mayúsculas y espacios sobrantes). Quitar tildes, en cambio, sí puede
fusionar productos que de verdad son distintos, y el requisito no da ninguna
autorización para hacerlo. Ante la duda, la norma es no destruir información.

**Consecuencia:** `meter("Pan", 2)` y `meter("pan", 3)` dejan 5 unidades de
`"pan"`. Guardar el nombre "bonito" para mostrar en pantalla queda fuera de
alcance: este TAD guarda cantidades, no presentación.

### A4. «meter» un producto que ya está en el carrito

**Lectura A:** se agrega un renglón nuevo (el carrito queda con dos «pan»).
**Lectura B:** se suma sobre el renglón que ya existe.

**Decisión:** Lectura B, las cantidades **se acumulan**.

**Razón:** el propio administrador pidió saber «cuántos hay **de cada uno**», o sea
que ya está asumiendo **una cantidad por producto**. Con la Lectura A esa pregunta
obligaría a recorrer y sumar duplicados, y dos representaciones distintas ("dos
renglones de 1" y "un renglón de 2") describirían el mismo carrito.

### A5. «sacar»: ¿cuántas unidades saca?

El verbo no trae cantidad. Podría ser una unidad, N unidades o el renglón completo.

**Decisión:** `sacar(producto, cantidad)` con la **cantidad siempre explícita**.
Para vaciar un producto se pasa exactamente la cantidad que hay.

**Razón:** un valor por omisión (por ejemplo, «saca 1») ahorra escribir un
argumento pero vuelve silencioso el caso más peligroso de una caja: creer que se
retiró todo cuando solo se retiró una unidad. Es un error que no lanza excepción y
que el cliente descubre en el recibo.

**Decisión asociada:** cuando la cantidad de un producto llega a **cero, el
producto desaparece del carrito**; no queda un renglón con cantidad 0.

**Razón:** si existieran los dos estados —"ausente" y "presente con 0"—, habría dos
formas de representar exactamente el mismo carrito, y toda operación futura tendría
que acordarse de contemplar ambas. Es la fuente clásica de errores que se evita
prohibiendo el estado redundante (ver el invariante, §5).

---

## 3. Ambigüedades de los casos extremos

Son las que el enunciado no menciona porque nadie piensa en ellas al hablar, pero
que el programa va a encontrar el primer día.

### A6. Cantidad igual a cero

**Decisión:** `meter(p, 0)` y `sacar(p, 0)` lanzan `ValueError`.

**Razón:** no modifican el carrito, así que aceptarlas no aporta nada; y cuando
aparece un 0 casi siempre viene de otro error (un campo vacío, una resta mal
hecha). Rechazarlo convierte un error silencioso en un error visible.

### A7. Cantidades negativas o que no son enteras

**Decisión:** la cantidad debe ser un `int` con valor `>= 1`. Cualquier otra cosa
—`-2`, `1.5`, `"3"`, `None`, `True`— lanza `ValueError`.

**Razón:** una cantidad negativa **invertiría el significado de las operaciones**
(`meter(p, -2)` sería un `sacar` disfrazado que se salta todas las validaciones de
`sacar`). Los decimales no aplican: este carrito cuenta unidades, no kilos. Y
`True` se rechaza explícitamente porque en Python `bool` es subclase de `int` y
`True == 1`: sin ese filtro, `meter("pan", True)` metería una unidad de pan.

### A8. Sacar más unidades de las que hay

**Decisión:** lanza `ValueError` y el carrito **queda exactamente como estaba**.

**Razón:** las dos alternativas son peores. Dejar cantidades negativas rompe el
invariante; sacar «lo que se pueda» es una extracción parcial que el requisito no
autoriza y que además deja al cajero creyendo que retiró 5 cuando retiró 2.

**Decisión asociada (atomicidad):** ninguna operación que falla deja el carrito a
medias. O se aplica completa, o no se aplica.

### A9. Sacar un producto que no está en el carrito

**Decisión:** lanza `ValueError`.

**Razón:** es una orden imposible de cumplir. Ignorarla en silencio haría que el
programa siguiera con un carrito distinto del que el cajero cree tener.

### A10. Consultar un producto que no está en el carrito

**Decisión:** `cuanto_hay(p)` devuelve `0`. **No** lanza excepción.

**Razón:** aquí sí hay una respuesta correcta y útil —de ese producto lleva cero—,
y devolverla permite usar el resultado directamente en una suma o una comparación
sin envolver cada consulta en un `try`.

**Sobre la asimetría con A9:** no es una contradicción, es la diferencia entre
preguntar y ordenar. Una **pregunta** sobre algo ausente tiene respuesta (`0`); una
**orden** sobre algo ausente no se puede ejecutar (`ValueError`).

### A11. Carrito recién creado

**Decisión:** `cuanto_llevo()` devuelve `0` y `cuanto_hay(p)` devuelve `0` para
cualquier producto válido.

**Razón:** el total de un conjunto vacío es cero; es el caso base y evita tratar el
carrito vacío como una situación especial.

### A12. ¿Un carrito o varios?

El requisito habla en singular, pero la tienda tiene **varias cajas atendiendo al
mismo tiempo**.

**Decisión:** cada `Carrito()` es **independiente**. Ninguna operación sobre un
carrito puede observarse desde otro.

**Razón:** es la razón de ser del TAD. Un almacenamiento compartido entre
instancias mezclaría las compras de dos clientes distintos.

**Consecuencia:** el almacenamiento se crea **dentro de `__init__`**, nunca como
atributo de clase ni como valor por omisión de un parámetro. Esta decisión es la
que el código anterior violaba; el diagnóstico completo está en
[`autopsia.md`](autopsia.md) y la prueba que lo verifica es
`test_dos_carritos_recien_creados_son_independientes`.

---

## 4. Contrato

Todas las operaciones normalizan el nombre del producto según A3. El tipo de error
para toda violación de precondición es `ValueError`.

### `Carrito()`

Crea un carrito vacío.

- **Postcondición:** `cuanto_llevo() == 0`.
- **Postcondición:** el almacenamiento es propio de la instancia (A12).

### `meter(producto, cantidad)`

Agrega `cantidad` unidades de `producto`.

- **Precondición:** `producto` es una cadena que no queda vacía al normalizarla.
- **Precondición:** `cantidad` es `int` y `cantidad >= 1`.
- **Postcondición:** `cuanto_hay(producto)` aumenta en `cantidad`; el resto del
  carrito no cambia.
- **Error:** `ValueError` si falla una precondición. El carrito no cambia.

### `sacar(producto, cantidad)`

Retira `cantidad` unidades de `producto`.

- **Precondición:** `producto` es una cadena que no queda vacía al normalizarla.
- **Precondición:** `cantidad` es `int` y `cantidad >= 1`.
- **Precondición:** `cuanto_hay(producto) >= cantidad`.
- **Postcondición:** `cuanto_hay(producto)` disminuye en `cantidad`; si llega a 0,
  el producto deja de estar en el carrito; el resto no cambia.
- **Error:** `ValueError` si falla una precondición. El carrito no cambia (A8).

### `cuanto_hay(producto) -> int`

Devuelve las unidades de `producto` que hay en el carrito.

- **Precondición:** `producto` es una cadena que no queda vacía al normalizarla.
- **Postcondición:** devuelve `0` si el producto no está (A10). Nunca negativo.
- **Postcondición:** no modifica el carrito.

### `cuanto_llevo() -> int`

Devuelve el total de **unidades** del carrito (A1).

- **Postcondición:** devuelve `0` si el carrito está vacío.
- **Postcondición:** el resultado es la suma de `cuanto_hay(p)` sobre todos los
  productos guardados.
- **Postcondición:** no modifica el carrito.

### Operación auxiliar (no contractual)

`repr(carrito)` devuelve una representación legible para depurar y para los
mensajes de error de pytest. **No forma parte del contrato**: su formato puede
cambiar y ninguna prueba depende de él.

---

## 5. Invariante de representación

En todo momento, para cualquier implementación:

1. toda cantidad almacenada es un entero **mayor o igual a 1** (nunca 0, nunca
   negativa);
2. **no existen dos entradas para el mismo producto** (las claves normalizadas son
   únicas);
3. `cuanto_llevo()` es exactamente la suma de las cantidades almacenadas;
4. el almacenamiento pertenece a la instancia y no se comparte con ninguna otra.

Las cuatro se cumplen al crear el carrito y las conservan `meter` y `sacar`,
incluso cuando fallan, porque validan **antes** de tocar el almacenamiento.

---

## 6. Las dos implementaciones

El contrato es el mismo; lo que cambia es la estructura de datos y, por lo tanto,
el costo. Con `n` = número de productos **distintos** en el carrito:

| Operación      | `carrito_lista.py` (lista de pares)  | `carrito_dict.py` (diccionario) |
| -------------- | ------------------------------------ | ------------------------------- |
| `meter`        | O(n) — busca el producto recorriendo  | O(1) promedio — acceso por hash |
| `sacar`        | O(n) — busca, y `pop` desplaza        | O(1) promedio                   |
| `cuanto_hay`   | O(n) — recorre hasta encontrarlo      | O(1) promedio                   |
| `cuanto_llevo` | O(n) — suma todas las cantidades      | O(n) — suma todos los valores   |

Lecturas de la tabla:

- El diccionario gana porque **la búsqueda por clave es lo que hace el TAD casi
  todo el tiempo**. Es el argumento para elegirlo en producción.
- `cuanto_llevo()` es O(n) en las dos: hay que sumar. Se podría bajar a O(1)
  guardando un total acumulado, pero eso agrega **estado duplicado** que puede
  desincronizarse con el contenido real. Para un carrito de campus (decenas de
  productos) no compensa: se prefiere el dato que siempre es correcto sobre el dato
  que es rápido.
- La lista **no es una mala elección por sí sola**: con pocos productos su costo
  real es despreciable y conserva el orden de inserción, que el diccionario solo
  garantiza desde Python 3.7. Este TAD no promete ningún orden (§7), así que esa
  ventaja no se usa.

Que las dos pasen **el mismo archivo de pruebas sin modificarlo** es la evidencia
de que el contrato está bien escrito: describe comportamiento observable, no
estructura interna.

---

## 7. Fuera de alcance (declarado, no olvidado)

Lo siguiente **no** se implementa, y es una decisión, no un descuido:

- **Precios y total en dinero** (A1): no hay precios en el requisito.
- **Inventario y validación de stock** (A2): es otro TAD.
- **Nombre de presentación** del producto (A3): se guarda la clave normalizada.
- **Persistencia**: el carrito vive en memoria mientras corre el programa. El
  archivo de texto que se está reemplazando queda fuera.
- **Orden de los productos**: el TAD no promete ningún orden al recorrer, y ninguna
  prueba lo asume.
- **Concurrencia**: un carrito no es seguro para varios hilos a la vez.

Si alguno de estos puntos era en realidad lo que el administrador quería, el
contrato **se amplía** (una operación nueva), no se reinterpreta.
