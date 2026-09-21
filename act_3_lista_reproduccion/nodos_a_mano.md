# Parte A — La cadena a mano

Antes de escribir `ListaEnlazada`, se construyó la cadena sin ninguna clase de
lista: solo una clase mínima `Nodo` (`dato`, `siguiente`) y variables sueltas.
El código está en [`nodos_a_mano.py`](nodos_a_mano.py) y su salida real en
[`salida_nodos_a_mano.txt`](salida_nodos_a_mano.txt).

## 1. Tres nodos enlazados y un bucle

```python
n1 = Nodo("Canción A")
n2 = Nodo("Canción B")
n3 = Nodo("Canción C")
n1.siguiente = n2
n2.siguiente = n3

actual = n1
while actual is not None:
    print(actual.dato)
    actual = actual.siguiente
```

```
 n1                n2                n3
┌──────────┬───┐  ┌──────────┬───┐  ┌──────────┬──────┐
│ Canción A│ ●─┼─▶│ Canción B│ ●─┼─▶│ Canción C│ None │
└──────────┴───┘  └──────────┴───┘  └──────────┴──────┘
```

El bucle no necesita saber cuántos nodos hay: se detiene cuando `siguiente` es
`None`. Salida: `['Canción A', 'Canción B', 'Canción C']`.

## 2. Insertar al principio: el orden de las dos asignaciones

```python
nuevo = Nodo("Última hora")
nuevo.siguiente = n1     # 1) el nuevo apunta a la cabeza vieja
cabeza = nuevo           # 2) la cabeza pasa a ser el nuevo
```

```
paso 1                          paso 2
 nuevo ──▶ n1 ──▶ n2 ──▶ n3      cabeza=nuevo ──▶ n1 ──▶ n2 ──▶ n3
```

Aquí el orden es a prueba de fallos porque `n1` todavía está guardado en una
variable. Lo mismo hace `ListaEnlazada.insertar_al_principio`.

## 3. Qué pasa si se reasigna el enlace antes de guardar el segundo

Caso: la cadena `X → Y → Z` de la que solo se conoce la cabeza `X`, y se quiere
insertar `Nuevo` entre `X` e `Y`.

**Orden incorrecto** (se pisa el enlace antes de guardarlo):

```python
cabeza.siguiente = nuevo_medio   # ← el único enlace a Y desaparece aquí
nuevo_medio.siguiente = ???      # ya no hay de dónde sacar a Y
```

```
Antes                        Después de la primera asignación

 X ──▶ Y ──▶ Z                X ──▶ Nuevo ──▶ None

                              Y ──▶ Z     (nadie apunta a Y: inalcanzable)
```

Resultado real de la ejecución:

```
antes:   ['X', 'Y', 'Z']
después: ['X', 'Nuevo']
¿Y sigue existiendo? False
¿Z sigue existiendo? False
```

`Y` y `Z` **no se borraron**: nadie ordenó eliminarlos. Se *perdieron*, porque
la única referencia que llevaba hasta ellos era `X.siguiente`, y al
reasignarla sin haberla guardado, el recolector de basura de Python los
liberó (el script lo comprueba con `weakref`). En un lenguaje sin recolector
serían memoria filtrada; en Python son canciones que desaparecen de la lista
sin error ni aviso, que es lo más difícil de depurar.

**Orden correcto** (guardar antes de reasignar):

```python
nuevo_medio.siguiente = cabeza.siguiente   # 1) el nuevo recibe el resto de la cadena
cabeza.siguiente = nuevo_medio             # 2) ahora sí se pisa el enlace
```

```
paso 1                             paso 2
 X ──▶ Y ──▶ Z                      X ──▶ Nuevo ──▶ Y ──▶ Z
        ▲
 Nuevo ─┘  (Nuevo ya conoce a Y)
```

Salida: `['X', 'Nuevo', 'Y', 'Z']`.

## 4. La regla general

> **Primero se conecta lo nuevo con lo que ya existe; después se desconecta lo
> viejo.** Un enlace solo se sobrescribe cuando su valor anterior ya está
> guardado en otra parte.

Esa regla aparece en las tres modificaciones de `lista_enlazada.py`:

| Operación | Guarda primero | Reasigna después |
|---|---|---|
| `insertar_al_principio` | `Nodo(x, self._cabeza)` conoce la cabeza vieja | `self._cabeza = nuevo` |
| `borrar` (del medio) | `victima = anterior.siguiente` | `anterior.siguiente = victima.siguiente` |
| `agregar` | `nuevo` ya existe | `self._cola.siguiente = nuevo`, luego `self._cola = nuevo` |
