# Especificación — TAD Lista de reproducción

Contrato común a `ListaArreglo` y `ListaEnlazada`. Se escribió antes que el
código; ver `constitucion.md`.

## 1. El caso

Reproductor de una emisora universitaria. Frecuencias medidas en una semana de
emisión:

| Operación de la emisora | Veces por día |
|---|---|
| Insertar al principio (canción de última hora) | 40 |
| Recorrer toda la lista (generar la parrilla) | 3 |
| Ir a la canción número N (saltar en el aire) | 200 |
| Borrar la canción actual (se cayó el derecho de emisión) | 15 |

Objetivo: implementar la lista con dos estructuras, comprobar que cumplen el
mismo contrato y decidir con datos cuál lleva el reproductor.

## 2. Interfaz

| Operación | Firma | Retorna | Errores |
|---|---|---|---|
| Crear | `Lista()` | lista vacía | — |
| Tamaño | `len(lista)` | `int ≥ 0` | — |
| ¿Vacía? | `lista.esta_vacia()` | `bool` | — |
| Insertar al principio | `lista.insertar_al_principio(x)` | `None` | — |
| Agregar al final | `lista.agregar(x)` | `None` | — |
| Ir a la canción N | `lista.obtener(i)` | la canción en la posición `i` | `IndexError`, `TypeError` |
| Borrar | `lista.borrar(i)` | la canción borrada | `IndexError`, `TypeError` |
| Recorrer | `iter(lista)` / `for c in lista` | canciones de la primera a la última | — |

Correspondencia con las operaciones de la emisora: «ir a la canción N» =
`obtener(N)`; «borrar la canción actual» = `borrar(i)` con `i` la posición de la
canción que suena; «recorrer toda la lista» = iterar.

## 3. Decisiones

- **D1. Posiciones base 0.** La primera canción es la posición 0, la última la
  `len(lista) - 1`.
- **D2. Índice inválido → `IndexError`.** Incluye índices negativos (no hay
  «contar desde el final») y cualquier índice en una lista vacía. La operación
  fallida **no modifica** la lista.
- **D3. Índice que no es `int` → `TypeError`.** Incluye `bool`, `float`, `str`
  y `None`.
- **D4. Duplicados permitidos.** Una canción puede aparecer más de una vez;
  `borrar(i)` quita exactamente la de la posición `i`.
- **D5. Cualquier valor es una canción**, incluido `None`. Por eso el borrado
  devuelve el valor y los errores se señalan con excepciones, no con valores
  centinela.
- **D6. Borrar devuelve la canción borrada.**
- **D7. Recorrer no consume ni modifica la lista**; se puede recorrer varias
  veces. Modificar la lista mientras se recorre no está definido.
- **D8. Sin capacidad máxima.** La lista crece hasta agotar la memoria.
- **D9. Independencia.** Dos listas no comparten estado.

## 4. Invariantes

1. `len(lista)` es igual al número de canciones que produce el recorrido.
2. `insertar_al_principio(x)` deja `obtener(0) == x` y desplaza el resto una
   posición.
3. `agregar(x)` deja `obtener(len - 1) == x`.
4. `borrar(i)` reduce `len` en 1 y desplaza a la izquierda las posiciones
   mayores a `i`.
5. Toda operación que lanza excepción deja la lista intacta.

## 5. Casos límite exigidos

Cada uno con pruebas propias en `test_extremos.py`:

1. Lista vacía.
2. Lista de un elemento.
3. Borrar el primero.
4. Borrar el último.

## 6. Fuera de alcance

Inserción en posición arbitraria, búsqueda por valor, ordenamiento, persistencia,
concurrencia, lista doblemente enlazada, reproducción de audio.

## 7. Criterios de aceptación

- `test_contrato.py` (sin modificar) pasa con las dos implementaciones.
- `test_extremos.py` pasa con las dos implementaciones.
- `ListaEnlazada` no contiene ninguna `list`, `deque` ni otro contenedor.
- `comparacion.md` trae la tabla teórico vs. medido, el costo del día con las
  dos estructuras, una recomendación y qué cambiaría en las frecuencias.
