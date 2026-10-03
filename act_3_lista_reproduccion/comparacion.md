# Parte D — La decisión del reproductor

Lista de **5.000 canciones**. Mediciones con [`benchmark.py`](benchmark.py)
(mediana de 7 corridas sobre listas recién construidas, Python 3.12). Salida
completa en [`resultados_benchmark.txt`](resultados_benchmark.txt).

## 1. Tabla resumen: costo teórico vs. medido, por operación

| Operación | Arreglo (teórico) | Arreglo (medido) | Enlazada (teórico) | Enlazada (medido) |
|---|---|---|---|---|
| Insertar al principio | O(n) | 296,81 µs | O(1) | 0,26 µs |
| Recorrer toda la lista | O(n) | 227,83 µs | O(n) | 188,45 µs |
| Ir a la canción N | O(1) | 0,18 µs | O(n) | 59,64 µs |
| Borrar la canción actual | O(n) | 149,78 µs | O(n) | 55,22 µs |

Cómo se midió cada una:

- **Insertar al principio:** 100 inserciones seguidas sobre la lista de 5.000.
- **Recorrer:** iteración completa.
- **Ir a la canción N:** 1.000 posiciones al azar (semilla fija), promedio ≈ N/2.
- **Borrar la actual:** se borra en la posición central (`len // 2`), que es el
  caso promedio. Borrar en la posición `i` cuesta ≈ `i` en ambas estructuras
  (desplazar en el arreglo, llegar al nodo anterior en la enlazada).

La teoría acierta en todas las formas de crecimiento: `0,26 µs` y `0,18 µs` son
las operaciones O(1); las demás cuestan cientos de veces más.

## 2. Costo de un día de emisión

Costo del día = Σ (veces al día × costo medido).

| Operación | Veces/día | Arreglo (ms) | Enlazada (ms) |
|---|---|---|---|
| Insertar al principio | 40 | 11,87 | 0,01 |
| Recorrer toda la lista | 3 | 0,68 | 0,57 |
| Ir a la canción N | 200 | 0,04 | 11,93 |
| Borrar la canción actual | 15 | 2,25 | 0,83 |
| **Total** | | **14,84** | **13,33** |

Enlazada / arreglo = **0,90×**. En siete corridas completas la relación quedó
entre 0,86× y 0,94×: la enlazada siempre gana, por poco.

## 3. Lo que la teoría sola no decía

Contando solo pasos elementales (un desplazamiento en el arreglo = un salto de
nodo en la enlazada), el día cuesta:

| | Arreglo | Enlazada |
|---|---|---|
| Insertar (40) | 40 × 5.000 = 200.000 | 40 × 1 = 40 |
| Recorrer (3) | 3 × 5.000 = 15.000 | 3 × 5.000 = 15.000 |
| Ir a N (200) | 200 × 1 = 200 | 200 × 2.500 = 500.000 |
| Borrar (15) | 15 × 2.500 = 37.500 | 15 × 2.500 = 37.500 |
| **Total de pasos** | **252.700** | **552.540** |

Por pasos, el **arreglo** ganaría más de 2 a 1. Pero lo medido dice lo
contrario. La diferencia es el **costo por paso**, que la notación O ignora:

- Un desplazamiento del arreglo (`datos[i] = datos[i-1]` con aritmética de
  índices) cuesta ≈ 60 ns (296,81 µs / 5.000).
- Un salto de nodo (`nodo = nodo.siguiente`) cuesta ≈ 24 ns (59,64 µs / 2.500).

Un paso del arreglo cuesta unas 2,5 veces un paso de la enlazada, y eso compensa
que la enlazada dé el doble de pasos. La ventaja de la enlazada es real pero
**estrecha**, y depende de un detalle de implementación (ver §5).

## 4. Recomendación

**Recomiendo `ListaEnlazada`**, con un margen pequeño (≈ 10 %, unos 1,5 ms por
día).

Razón, con las frecuencias dadas: hay dos partidas enormes y opuestas.

- Las 40 inserciones al principio le ahorran a la enlazada 11,87 − 0,01 = **11,86 ms**.
- Los 200 saltos a la canción N le cuestan a la enlazada 11,93 − 0,04 = **11,89 ms** de más.

Esas dos partidas casi se anulan (la enlazada pierde 0,03 ms ahí). Lo que
inclina la balanza son las operaciones pequeñas: las 15 borraduras cuestan
1,42 ms menos en la enlazada (su paso es más barato) y las 3 pasadas por la
parrilla 0,11 ms menos: en total **1,51 ms** a favor de la enlazada, que es la
diferencia entre 14,84 ms y 13,33 ms.

### Qué tendría que cambiar en las frecuencias

Manteniendo el resto fijo, ambas estructuras cuestan lo mismo con:

| Frecuencia | Real | Punto de quiebre | Si cruza el quiebre… |
|---|---|---|---|
| Inserciones al principio | 40 / día | ≈ 35 / día | por debajo de ~35 gana el **arreglo** |
| Saltos «ir a N» | 200 / día | ≈ 225 / día | por encima de ~225 gana el **arreglo** |

(En las siete corridas: 33–37 inserciones y 213–237 saltos.)

Es decir: **basta con que las inserciones bajen de 40 a ~35 al día, o que los
saltos suban de 200 a ~225, para que la recomendación se invierta.** Los datos
reales están a un 12 % del quiebre en ambos sentidos, así que no es una
decisión robusta: si la emisora tiene una semana con menos canciones de última
hora, el arreglo pasa a ser la mejor opción.

Otras variables que la invertirían:

- **Más saltos por la parrilla (`ir a N`)** — el uso típico del «saltar en el
  aire»: cada salto extra pesa 60 µs contra 0,18 µs.
- **Lista más larga:** todos los costos escalan con n, pero como las dos partidas
  dominantes escalan igual (inserción ∝ n en el arreglo, salto ∝ n/2 en la
  enlazada), el quiebre en frecuencias casi no se mueve; lo que sí cambia es el
  costo absoluto, que crece linealmente para las dos.

## 5. Limitaciones de la medición

- **`ListaArreglo` desplaza con un bucle de Python**, no con `list.insert`. Si se
  desplazara con una rutina de C (`memmove`, o `list.insert`), un paso del
  arreglo costaría una fracción del actual y **el arreglo ganaría
  claramente** (la tabla de pasos del §3 pasaría a mandar). Se eligió el
  bucle para que las dos estructuras estén escritas en el mismo nivel y la
  comparación sea de algoritmos, pero la recomendación vale para *estas*
  implementaciones, no para «arreglo vs. enlazada» en abstracto.
- Los tiempos absolutos dependen de la máquina; la relación entre ellos (y los
  puntos de quiebre) es lo que se debe leer.
- El día tiene solo cuatro operaciones; en producción también habría
  `agregar` al final (O(1) en ambas) y otras que no cambian la conclusión.
