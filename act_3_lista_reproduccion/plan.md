# Plan técnico

Cómo se cumple `spec.md` respetando `constitucion.md`.

## 1. Estructura del repositorio

```
nodos_a_mano.py / .md      Parte A: cadena manual, diagramas, pérdida de referencia
lista_arreglo.py           ListaArreglo (actividad 2)
lista_enlazada.py          Parte B: ListaEnlazada
conftest.py                fixture `Lista` parametrizada con las dos clases
test_contrato.py           batería de la actividad 2, SIN modificar
test_extremos.py           Parte C: los cuatro casos límite
benchmark.py               Parte D: medición y costo del día
comparacion.md             Parte D: tablas, cálculo y recomendación
resultados_benchmark.txt   salida completa del benchmark
constitucion.md spec.md plan.md task.md    documentos SDD
```

## 2. Diseño de las estructuras

### ListaArreglo
- Bloque `_datos` (`list` de tamaño fijo usada como arreglo) + contador `_n`.
- Capacidad inicial 4; al llenarse se duplica y se copia con un bucle
  (agregar al final: O(1) amortizado).
- `insertar_al_principio` y `borrar(i)` desplazan con bucles explícitos.
- `obtener(i)`: acceso directo, O(1).

### ListaEnlazada
- `Nodo(dato, siguiente)` con `__slots__`.
- La lista guarda `_cabeza`, `_cola` y `_n`.
- `_cola` existe para que `agregar` sea O(1); es también el punto donde más se
  falla, por eso `test_extremos.py` sigue operando tras cada caso límite.
- `borrar(i)`: rama `i == 0` (actualiza `_cabeza`, y `_cola` si queda vacía) y
  rama general (usa el nodo anterior; actualiza `_cola` si se borra el último).
- Orden de asignaciones siempre «guardar antes de sobrescribir».

## 3. Costos teóricos

| Operación | Arreglo | Enlazada |
|---|---|---|
| Insertar al principio | O(n) | O(1) |
| Agregar al final | O(1) amortizado | O(1) (con cola) |
| Obtener posición i | O(1) | O(i) |
| Borrar posición i | O(n − i) | O(i) |
| Recorrer | O(n) | O(n) |

## 4. Estrategia de pruebas

- Una sola batería, dos implementaciones, vía la fixture `Lista`
  (ids `[arreglo]` y `[enlazada]` en la salida de pytest).
- `test_extremos.py`: cada caso límite tiene su bloque y verifica también la
  operación *posterior* al caso límite.
- Verificación de calidad de las pruebas por mutación manual: se rompe a
  propósito `ListaEnlazada` (no actualizar la cola al borrar el último, no
  anularla al vaciar, no fijarla en la primera inserción, no incrementar `n`) y
  se comprueba que las pruebas fallan.

## 5. Estrategia de medición

- N = 5.000 canciones, lista recién construida para cada corrida.
- Mediana de 7 corridas por operación (`time.perf_counter`).
- Insertar: 100 seguidas; ir a N: 1.000 posiciones al azar con semilla fija;
  borrar la actual: posición central; recorrer: iteración completa.
- Costo del día = Σ frecuencia × costo medido.
- Punto de quiebre: se despeja la frecuencia de inserciones (y de saltos) que
  iguala el costo de ambas estructuras, dejando el resto fijo.

## 6. Riesgos

| Riesgo | Mitigación |
|---|---|
| El costo medido depende de cómo se desplaza el arreglo | Desplazar con bucles en ambas estructuras y declararlo en `comparacion.md` §5 |
| Ruido del reloj | Mediana de 7 corridas; se repitió el benchmark completo 7 veces |
| Punteros de cabeza/cola mal actualizados | Casos límite con pruebas propias + mutación |
