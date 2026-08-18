# TAD Carrito — tienda del campus

Reemplazo del carrito de compras que hoy es un archivo de texto editado a mano.

El punto del ejercicio no es programar un carrito: es **decidir por escrito qué
significaba el requisito antes de programarlo**, y **diagnosticar con precisión**
un error de referencias compartidas del código anterior.

---

## Requisito original

El administrador escribió:

> «necesito poder meter productos, sacar productos, saber cuántos hay de cada uno
> y cuánto llevo en total»

Esa frase tiene ambigüedades que hacen imposible programar sin decidir antes. Las
decisiones están en [`spec.md`](spec.md), cada una con su razón.

---

## Archivos

| Archivo                                  | Qué contiene                                                        |
| ---------------------------------------- | ------------------------------------------------------------------- |
| [`spec.md`](spec.md)                     | Contrato del TAD y **12 ambigüedades decididas**, cada una razonada  |
| [`test_carrito.py`](test_carrito.py)     | Batería **única** de pruebas, incluidos los casos extremos           |
| [`carrito_lista.py`](carrito_lista.py)   | Implementación con **lista de pares** — O(n)                         |
| [`carrito_dict.py`](carrito_dict.py)     | Implementación con **diccionario** — O(1) promedio                   |
| [`autopsia.md`](autopsia.md)             | Diagnóstico del error de las dos cajas, con **3 diagramas** de memoria |
| [`VERIFICACION.txt`](VERIFICACION.txt)   | Salida real de las pruebas (en rojo y en verde) y el historial de Git |

---

## Cómo ejecutar

Requiere Python 3.9 o superior y `pytest`.

```bash
python -m pip install pytest
```

Ejecutar toda la batería contra las dos implementaciones:

```bash
python -m pytest -q
```

Resultado esperado: **92 pruebas** (46 casos × 2 implementaciones).

Ver qué implementación está corriendo cada caso — aparecen marcadas como
`[lista]` y `[dict]`:

```bash
python -m pytest -v
```

Ejecutar también los ejemplos de la documentación (los bloques `>>>` de los
docstrings: 14 doctests, 7 por archivo):

```bash
python -m pytest --doctest-modules carrito_lista.py carrito_dict.py -q
```

---

## Cómo está resuelto

### Las ambigüedades (`spec.md`)

Cuatro nacen de las palabras del administrador y son las que cambian el sistema:

1. **«cuánto llevo en total»: ¿unidades o dinero?** → unidades, porque el
   requisito nunca mencionó precios. El dinero queda declarado fuera de alcance.
2. **«cuántos hay de cada uno»: ¿en el carrito o en la tienda?** → en el carrito.
   El inventario es otro TAD.
3. **¿Qué identifica a un producto?** → una cadena normalizada (sin espacios
   sobrantes, en minúsculas). Sin esto, `"Pan"` y `"pan"` serían dos productos.
4. **«meter» algo que ya está: ¿renglón nuevo o acumular?** → acumular.

Las otras ocho cubren los casos extremos: cantidad cero, negativos, no enteros,
sacar de más, sacar lo que no está, consultar lo que no está, carrito vacío y la
independencia entre carritos.

### Las dos implementaciones

El mismo contrato sobre dos estructuras distintas. Con `n` = productos distintos:

| Operación      | `carrito_lista.py` | `carrito_dict.py` |
| -------------- | ------------------ | ----------------- |
| `meter`        | O(n)               | O(1) promedio     |
| `sacar`        | O(n)               | O(1) promedio     |
| `cuanto_hay`   | O(n)               | O(1) promedio     |
| `cuanto_llevo` | O(n)               | O(n)              |

El diccionario gana porque el TAD casi siempre está haciendo lo mismo: buscar un
producto por su nombre. La versión con lista se conserva porque **muestra el
trabajo que el diccionario hace gratis** (garantizar que no haya dos entradas del
mismo producto).

### El error de las dos cajas (`autopsia.md`)

Causa: `def __init__(self, nombre, productos={})`. El valor por omisión se evalúa
**una sola vez**, así que todas las cajas recibían **el mismo diccionario**.

Las cajas sí eran objetos distintos —por eso engaña—; lo que no era distinto era
el diccionario al que las dos apuntaban. El diagnóstico está hecho con salida
real del intérprete (`is`, `id()`) y tres diagramas de memoria con las flechas
entre nombres y objetos.

Cuatro pruebas de la batería impiden que el error vuelva sin que nadie se entere:
una comprueba el síntoma, otra el alias entre instancias, y las otras dos
bloquean las dos formas alternativas del mismo error (atributo de clase y valor
por omisión mutable).

---

## Historial de Git

La actividad pide que se vea el commit con las pruebas **en rojo** antes del
commit con la implementación:

```bash
git log --oneline
```

```
(último)  Documenta el diagnostico del error de las dos cajas
45ccd36   Implementa el carrito con lista de pares y con diccionario   <- VERDE
7907dda   Define el contrato del TAD Carrito y sus pruebas             <- ROJO
```

En el commit `7907dda` existen `spec.md` y `test_carrito.py` pero todavía no
existe ninguna implementación, así que las pruebas fallan al importar. La salida
literal de esa ejecución está en [`VERIFICACION.txt`](VERIFICACION.txt).

Para comprobarlo sin creer en el archivo, se puede volver a ese commit y ejecutar:

```bash
git stash --include-untracked && git checkout 7907dda && python -m pytest -q
```

Y para regresar:

```bash
git checkout main && git stash pop
```

---

## Restricciones de la actividad

- **Sin `collections.Counter`.** Ninguna de las dos implementaciones lo importa;
  el objetivo era entender qué hay debajo, que es un diccionario de cuentas con
  un valor por omisión.
- **Un solo archivo de pruebas, sin modificarlo entre implementaciones.**
  `test_carrito.py` es uno solo y corre contra las dos clases mediante una
  fixture parametrizada de pytest. No hay ninguna rama del código de pruebas que
  dependa de cuál implementación se esté probando.
- **Diagramas con flechas entre variables y objetos.** Los tres diagramas de
  `autopsia.md` muestran los nombres a la izquierda, los objetos a la derecha y
  las flechas entre ellos; el error se ve porque **dos flechas terminan en el
  mismo destino**.
