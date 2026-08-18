# Autopsia: dos cajas que comparten el mismo carrito

> Diagnóstico del error del código anterior. Todos los valores y direcciones que
> aparecen aquí son **salida real** de ejecutar el código, no ejemplos
> inventados. Las direcciones cambian en cada ejecución; lo que no cambia —y es
> lo único que importa— es **cuáles coinciden entre sí**.
>
> En los diagramas se escriben abreviadas: `@…37c00` es el final de
> `0x1b227d37c00`.

---

## 1. El síntoma

Dos cajas distintas de la tienda, creadas por separado, terminan compartiendo el
mismo carrito: se pasa un producto por la Caja 1 y aparece también en la Caja 2.
El cliente de la Caja 2 termina pagando el pan del cliente de la Caja 1.

## 2. El código que lo produce

```python
class Caja:
    def __init__(self, nombre, productos={}):   # <-- aquí está el error
        self.nombre = nombre
        self.productos = productos

    def meter(self, producto, cantidad):
        self.productos[producto] = self.productos.get(producto, 0) + cantidad

    def cuanto_hay(self, producto):
        return self.productos.get(producto, 0)


caja_1 = Caja("Caja 1")
caja_2 = Caja("Caja 2")

caja_1.meter("pan", 2)
```

A simple vista el código parece correcto: hay dos llamadas a `Caja(...)`, así que
hay dos objetos `Caja`, y cada uno guarda su propio atributo `productos`. Las dos
primeras afirmaciones son ciertas. **La tercera no.**

## 3. La evidencia

```
ANTES
  id(caja_1)             = 0x1b228061640
  id(caja_2)             = 0x1b2280616a0
  caja_1 is caja_2       = False          <-- las cajas SÍ son objetos distintos
  id(caja_1.productos)   = 0x1b227d37c00
  id(caja_2.productos)   = 0x1b227d37c00  <-- LA MISMA DIRECCIÓN
  caja_1.productos is caja_2.productos
                         = True           <-- EL DIAGNÓSTICO
  id(Caja.__init__.__defaults__[0])
                         = 0x1b227d37c00  <-- y viene de aquí
```

Esto es lo que hace tan difícil de ver el error: **las cajas de verdad son
distintas**. `caja_1 is caja_2` da `False`, tienen direcciones distintas, tienen
nombres distintos. Lo que no es distinto es el diccionario al que las dos apuntan.

## 4. Diagrama de memoria: ANTES de modificar nada

```text
        NOMBRES                       OBJETOS EN MEMORIA
    ───────────────            ──────────────────────────────

    caja_1 ────────►  ┌───────────────────────────┐
                      │  Caja             @…61640 │
                      │  nombre    = "Caja 1"     │
                      │  productos ───────────────┼──────┐
                      └───────────────────────────┘      │
                                                         ▼
                                                ┌──────────────────┐
                                                │ dict     @…37c00 │
                                                │       { }        │
                                                └──────────────────┘
                                                         ▲
    caja_2 ────────►  ┌───────────────────────────┐      │
                      │  Caja             @…616a0 │      │
                      │  nombre    = "Caja 2"     │      │
                      │  productos ───────────────┼──────┘
                      └───────────────────────────┘


    Caja.__init__.__defaults__[0] ───────────────► el mismo dict @…37c00
```

Hay que leer las **flechas**, no las cajas: hay tres objetos `Caja`-y-`dict` en el
dibujo, pero **dos flechas terminan en el mismo destino**. Ese es el alias.

Mientras el diccionario esté vacío el error es invisible: las dos cajas muestran
`{}`, que es lo que se espera. El error ya ocurrió, pero todavía no se nota.

## 5. Qué hace realmente `self.productos = productos`

En Python, una variable **no es una caja que contiene un valor**: es una etiqueta
pegada a un objeto que vive en otra parte. Por eso la asignación:

```python
self.productos = productos
```

**no copia el diccionario**. Copia únicamente la *dirección* del diccionario, o
sea, pega una segunda etiqueta al mismo objeto. Después de esa línea hay dos
nombres —`caja_1.productos` y `caja_2.productos`— y un solo diccionario.

Y aquí está la parte que sorprende: `productos={}` **no crea un diccionario cada
vez que se llama a `Caja(...)`**. Los valores por omisión se evalúan **una sola
vez**, cuando Python define la función, y quedan guardados dentro de la propia
función:

```python
Caja.__init__.__defaults__      # ({},)  <- el diccionario vive AQUÍ
```

Así que ese `{}` es **un objeto único** que se reparte a todas las cajas que no
reciban el argumento. No hay dos diccionarios: hay uno solo, prestado dos veces.

## 6. La operación que rompe la independencia

```python
caja_1.meter("pan", 2)
```

`meter` hace `self.productos[producto] = ...`, o sea **modifica el diccionario en
el sitio** (los diccionarios son mutables). No crea uno nuevo ni reasigna nada:
escribe dentro del objeto compartido.

## 7. Diagrama de memoria: DESPUÉS de `caja_1.meter("pan", 2)`

```text
        NOMBRES                       OBJETOS EN MEMORIA
    ───────────────            ──────────────────────────────

    caja_1 ────────►  ┌───────────────────────────┐
                      │  Caja             @…61640 │
                      │  nombre    = "Caja 1"     │
                      │  productos ───────────────┼──────┐
                      └───────────────────────────┘      │
                                                         ▼
                                                ┌──────────────────┐
                                                │ dict     @…37c00 │
                                                │   {'pan': 2}     │  <-- cambió
                                                └──────────────────┘
                                                         ▲
    caja_2 ────────►  ┌───────────────────────────┐      │
                      │  Caja             @…616a0 │      │
                      │  nombre    = "Caja 2"     │      │
                      │  productos ───────────────┼──────┘
                      └───────────────────────────┘


    Caja.__init__.__defaults__[0] ───────────────► el mismo dict @…37c00
```

**Las flechas son exactamente las mismas que en el diagrama anterior.** Lo único
que cambió es el *contenido* del objeto al que las dos apuntan. Por eso:

```
DESPUÉS de caja_1.meter('pan', 2)
  id(caja_1.productos)   = 0x1b227d37c00   <-- la dirección no cambió
  id(caja_2.productos)   = 0x1b227d37c00
  caja_1.productos       = {'pan': 2}
  caja_2.productos       = {'pan': 2}      <-- la Caja 2 "ve" el pan ajeno
  caja_2.cuanto_hay('pan') = 2
```

Y todavía hay algo peor. El diccionario compartido **es el valor por omisión de la
función**, así que la contaminación no se queda entre estas dos cajas: sobrevive y
alcanza a las que todavía no existen.

```python
caja_3 = Caja("Caja 3")
caja_3.productos        # {'pan': 2}   <-- nace con el pan de otro cliente
```

Una caja recién abierta ya trae mercancía adentro.

**Dónde está el error, entonces:** no está en `meter` ni en `append` ni en el
`[]=`. Esas operaciones hicieron exactamente lo que se les pidió sobre el objeto
que se les dio. El error ocurrió **antes**, en el `__init__`, cuando las dos cajas
recibieron el mismo objeto en vez de uno propio. El síntoma aparece al modificar;
la causa es de construcción.

## 8. La misma falla tiene otras dos caras

Conviene reconocerlas, porque el diagrama de memoria es idéntico en las tres:

**Causa 1 — valor por omisión mutable** (la del código anterior):

```python
def __init__(self, nombre, productos={}):   # se evalúa UNA vez
```

**Causa 2 — atributo de clase mutable:**

```python
class Caja:
    productos = {}      # vive en la CLASE, no en cada objeto
```

Aquí el diccionario pertenece a `Caja`, y todas las instancias lo alcanzan por el
mismo camino. Es el mismo dibujo con la flecha saliendo de la clase.

**Causa 3 — asignación entre objetos ya creados:**

```python
caja_2.productos = caja_1.productos   # dos nombres, un objeto
```

Es la forma más honesta de las tres, porque al menos se ve escrita.

La regla que las une: **un objeto mutable creado una sola vez y alcanzable por más
de un camino.**

## 9. La corrección

```python
class Caja:
    def __init__(self, nombre, productos=None):
        self.nombre = nombre
        self.productos = {} if productos is None else dict(productos)
```

Dos cambios, cada uno con su motivo:

1. **`productos=None`**: `None` es inmutable, así que compartirlo no puede hacer
   daño. Es un centinela que significa "no me pasaron nada".
2. **`{}` dentro del cuerpo**: el `{}` ahora se evalúa **en cada llamada**, así
   que cada caja construye su propio diccionario. `dict(productos)` en la otra
   rama hace lo mismo cuando sí llega un valor: **copia** en vez de guardar la
   referencia recibida.

Evidencia de que quedó corregido:

```
  id(caja_1.productos)   = 0x155bdadb900
  id(caja_2.productos)   = 0x155bdadbf40   <-- direcciones DISTINTAS
  caja_1.productos is caja_2.productos = False
  caja_1.productos       = {'pan': 2}
  caja_2.productos       = {}              <-- ya no ve el pan ajeno
  Caja.__init__.__defaults__ = (None,)     <-- ya no guarda nada mutable
```

## 10. Diagrama de memoria: CORREGIDO

```text
        NOMBRES                       OBJETOS EN MEMORIA
    ───────────────            ──────────────────────────────

    caja_1 ────────►  ┌───────────────────────────┐
                      │  Caja                     │
                      │  nombre    = "Caja 1"     │      ┌──────────────────┐
                      │  productos ───────────────┼─────►│ dict     @…db900 │
                      └───────────────────────────┘      │   {'pan': 2}     │
                                                         └──────────────────┘

    caja_2 ────────►  ┌───────────────────────────┐
                      │  Caja                     │
                      │  nombre    = "Caja 2"     │      ┌──────────────────┐
                      │  productos ───────────────┼─────►│ dict     @…dbf40 │
                      └───────────────────────────┘      │       { }        │
                                                         └──────────────────┘

    Caja.__init__.__defaults__ = (None,)   ──────────►  nada mutable que prestar
```

Ahora **ninguna flecha se cruza con otra**. Cada caja llega a un objeto que nadie
más alcanza, y modificar uno no puede afectar al otro.

## 11. Una trampa que queda abierta: la copia superficial

`dict(productos)` copia **un solo nivel**. Si los valores fueran a su vez objetos
mutables, el error volvería un piso más abajo:

```python
plantilla = {"combo": ["pan", "leche"]}
c1 = Caja("C1", plantilla)
c2 = Caja("C2", plantilla)

c1.productos is c2.productos                # False  <- los dicts sí son distintos
c1.productos["combo"] is c2.productos["combo"]   # True   <- ¡la lista NO!
```

```text
    c1.productos ──►┌───────────────┐
                    │ dict A        │
                    │ "combo" ──────┼──────┐
                    └───────────────┘      │
                                           ▼
                                    ┌──────────────────┐
                                    │ list             │  <-- sigue compartida
                                    │ ["pan", "leche"] │
                                    └──────────────────┘
                                           ▲
    c2.productos ──►┌───────────────┐      │
                    │ dict B        │      │
                    │ "combo" ──────┼──────┘
                    └───────────────┘
```

**En este ejercicio el problema no aplica**, y por una razón concreta: los valores
del carrito son **enteros**, que son inmutables. Un entero no se puede modificar
en el sitio; `cantidad + 1` crea un entero nuevo. Por eso la copia superficial
basta. Si algún día un producto guardara una lista (lotes, descuentos aplicados),
haría falta `copy.deepcopy`.

## 12. Cómo lo evita el código entregado

Las dos implementaciones crean su almacenamiento **dentro de `__init__`**, que es
la decisión A12 de [`spec.md`](spec.md):

```python
# carrito_dict.py
def __init__(self) -> None:
    self._productos: dict[str, int] = {}

# carrito_lista.py
def __init__(self) -> None:
    self._productos: list[tuple[str, int]] = []
```

Además, el TAD **no recibe** un contenedor desde afuera: no hay ningún parámetro
por el que se pueda colar una referencia ajena. Esa ausencia es deliberada.

Y para que el error no pueda volver sin que nadie se entere, hay cuatro pruebas en
[`test_carrito.py`](test_carrito.py) que lo vigilan, una por cada forma del error:

| Prueba                                              | Qué bloquea                              |
| --------------------------------------------------- | ---------------------------------------- |
| `test_dos_carritos_recien_creados_son_independientes` | el síntoma observable                    |
| `test_cada_carrito_tiene_su_propio_almacenamiento`    | el alias entre instancias (`is`)         |
| `test_la_clase_no_guarda_contenedores_mutables`       | causa 2 (atributo de clase)              |
| `test_el_constructor_no_tiene_valores_por_omision_mutables` | causa 1 (valor por omisión mutable) |

## 13. La regla, en una línea

**Un objeto mutable que se crea una sola vez y se alcanza por dos caminos no son
dos objetos: es uno con dos nombres.** La comprobación que lo demuestra siempre es
la misma —`a is b`— y la corrección también: crear el objeto donde se necesita que
sea nuevo, es decir, dentro del constructor.
