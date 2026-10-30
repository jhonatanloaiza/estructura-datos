# Predicción de complejidad (Parte B)

Derivada leyendo `lista_arreglo.py`, **antes de cronometrar nada**. El commit
que agrega este archivo es anterior al de `medicion.py` y `resultados.csv`, y
esa fecha es la prueba de que esto es una predicción y no una explicación
hecha después de ver los números.

Los conteos no se quedan en papel: `test_lista_arreglo.py` los comprueba
contando comparaciones y escrituras reales (sin medir tiempo).

## Qué se cuenta

Dos operaciones elementales sobre registros:

- **Comparación:** un `==` o `<` entre dos registros.
- **Movimiento:** escribir un registro en una posición del bloque.

`n` es el número de registros. Lo demás (validar la posición, llamar al método,
actualizar `i`) es una cantidad fija por llamada o por vuelta de bucle: cambia
la constante, no la forma de la curva.

## Las cinco operaciones

### 1. `obtener(pos)` — O(1)

```python
self._validar_pos(pos, self._n)   # dos comparaciones de enteros
return self._datos[pos]           # una lectura directa
```

No hay bucle. Son 0 comparaciones de registros y 0 movimientos, sea cual sea
`n`: el arreglo calcula dónde está `pos` sin recorrer nada.

### 2. `insertar(pos, x)` — O(n); O(1) amortizado al final

```python
for i in range(self._n, pos, -1):          # n - pos vueltas
    self._datos[i] = self._datos[i - 1]    # 1 movimiento por vuelta
self._datos[pos] = x                       # 1 movimiento más
```

El costo es **n − pos + 1 movimientos**, así que depende de dónde se inserte:

| Caso | `pos` | Movimientos | Clase |
|---|---|---|---|
| Peor: al inicio | 0 | n + 1 | O(n) |
| Promedio: posición uniforme | cualquiera | n/2 + 1 | O(n) |
| Mejor: al final, con espacio | n | 1 | O(1) |

Falta un costo escondido: si el bloque está lleno, `_asegurar_espacio` copia los
n elementos a uno del doble de tamaño. Esa inserción cuesta n, pero compra n
inserciones gratis. En un ciclo completo son n copias + n escrituras para n
inserciones: **2 movimientos por inserción**, constante. Por eso al final es
O(1) *amortizado*, no O(1) a secas.

Se predicen dos curvas para la misma operación: lineal al inicio, plana al final.

### 3. `insertar_ordenado(x)` — O(n)

Primero `_cota_inferior`, luego `insertar`:

- **Comparaciones:** a lo sumo ⌊log₂ n⌋ + 1 (mismo argumento de la operación 5).
- **Movimientos:** n − p + 1, con p la posición que le toca. Si los libros nuevos
  caen en cualquier parte del catálogo, en promedio n/2 + 1.

T(n) ≈ log₂ n + n/2, y manda el término lineal. Con 80.000 registros son 17
comparaciones contra unos 40.000 movimientos: **99,96 % del trabajo es
desplazar**. Encontrar el sitio con búsqueda binaria no abarata la inserción.

### 4. `buscar_lineal(x)` — O(n)

```python
for i in range(self._n):
    if self._datos[i] == x:    # 1 comparación por vuelta
        return i
```

Si `x` está en la posición p hace p + 1 comparaciones. Con posiciones uniformes
el promedio es (n + 1)/2. Si `x` no está, compara con todos: n. En ambos casos
es lineal; el fallo cuesta el doble que el acierto.

### 5. `buscar_binaria(x)` — O(log n)

`_cota_inferior` mantiene un intervalo `[bajo, alto)` de m posiciones. Cada
vuelta hace 1 comparación y deja a lo sumo ⌊m/2⌋ posiciones, así que tras k
vueltas quedan como mucho n/2ᵏ. El bucle termina al llegar a 0, es decir, tras a
lo sumo ⌊log₂ n⌋ + 1 vueltas. Se suma 1 comparación final para confirmar si lo
hallado es `x`. Total: **⌊log₂ n⌋ + 2 comparaciones**, acierte o falle.

## Lo que esto predice para cada tamaño

Conteo de operaciones elementales (promedio donde aplica):

| Operación | n = 1.000 | n = 10.000 | n = 80.000 | n = 200.000 |
|---|---:|---:|---:|---:|
| `obtener` | 0 | 0 | 0 | 0 |
| `insertar` al inicio | 1.001 | 10.001 | 80.001 | 200.001 |
| `insertar` al final (amortizado) | 2 | 2 | 2 | 2 |
| `insertar_ordenado` (comp. + mov.) | 10 + 501 | 14 + 5.001 | 17 + 40.001 | 18 + 100.001 |
| `buscar_lineal`, acierto | 500,5 | 5.000,5 | 40.000,5 | 100.000,5 |
| `buscar_lineal`, fallo | 1.000 | 10.000 | 80.000 | 200.000 |
| `buscar_binaria` | 11 | 15 | 18 | 19 |

Crecimiento esperado del tiempo respecto a n = 1.000:

| Clase | n = 10.000 | n = 80.000 | n = 200.000 |
|---|---:|---:|---:|
| O(1) | 1 | 1 | 1 |
| O(log n) | 1,36 | 1,64 | 1,73 |
| O(n) | 10 | 80 | 200 |

## Cómo se decidirá si la medición coincide

Fijado ahora, para no acomodarlo después. La pendiente es la de la recta en
escala log-log entre n = 1.000 y n = 200.000.

| Clase | Coincide si |
|---|---|
| O(n) | la pendiente está entre 0,9 y 1,1 |
| O(1) | T(200.000) / T(1.000) es menor que 1,5 |
| O(log n) | T(200.000) / T(1.000) está entre 1,4 y 2,1 |

## Lo que puede no coincidir

El modelo supone que una comparación cuesta lo mismo con 1.000 registros que con
200.000. En un computador real eso es falso: mientras los datos caben en la
caché del procesador, leerlos es rápido, y al dejar de caber se vuelve más lento.
Se espera entonces:

- En las curvas O(n), una pendiente algo mayor que 1 en los tamaños grandes.
- En `buscar_binaria`, más crecimiento que 1,73: cada comparación salta a una
  zona lejana de la memoria, justo lo que peor lleva la caché.
- En `obtener` y `buscar_binaria`, ruido relativo mayor: son tiempos muy pequeños.

## Lo que esto predice para la decisión

Sean `s` las búsquedas por cada inserción. Los dos costos son:

```
ordenado    = s · buscar_binaria + insertar_ordenado
desordenado = s · buscar_lineal  + insertar_final
```

Igualándolos y despejando `s`, el punto de equilibrio es:

```
s* = (insertar_ordenado − insertar_final) / (buscar_lineal − buscar_binaria)
```

Quitando los términos pequeños (2 movimientos y unas 18 comparaciones) y llamando
`m` al costo de un movimiento y `c` al de una comparación:

```
s* ≈ (n/2 · m) / (n/2 · c) = m / c
```

De aquí salen dos predicciones que se pueden contrastar en la Parte D:

1. **El equilibrio casi no depende del tamaño del catálogo**, porque n se cancela.
2. **El equilibrio debería rondar 1**: mover y comparar son, cada uno, una vuelta
   de bucle en Python, y no hay razón para que uno cueste varias veces más que
   el otro.

La segunda predicción tiene una consecuencia incómoda. Si `s*` ronda 1, el
catálogo ordenado gana también en vacaciones (5:1), y la respuesta sería la misma
en las tres épocas, mientras que el enunciado avisa que si eso pasa hay que
revisar el cálculo. Queda registrado aquí para que, si ocurre, se revise a fondo y
no se dé por bueno ni se acomode para que cambie.
