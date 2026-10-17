# Plan técnico

Cómo se cumple `spec.md` respetando `constitucion.md`.

## 1. Estructura del repositorio

```
cola.py                  Parte A: cola simple (FIFO) con nodos enlazados
cola_prioridad.py        Parte B: cola de prioridad, 3 niveles, reserva de turnos
simulacion.py             Parte B: compara estrategia estricta vs. con reserva
resultados_simulacion.txt salida real de simulacion.py

arbol_carpetas.py        Parte C+D: Carpeta, consultas recursivas, listado por niveles
pila.py                  Parte D: pila (LIFO) solo para la comparación del recorrido
generar_recorridos.py    Parte D: construye el árbol de prueba y captura ambas salidas
recorridos.md             Parte D: árbol de prueba + salidas + explicación
salida_recorridos.txt     salida real de generar_recorridos.py

test_cola.py
test_cola_prioridad.py
test_arbol_carpetas.py

constitucion.md spec.md plan.md task.md    documentos SDD
```

## 2. Parte A — `cola.py`

`Nodo(dato, siguiente)` + `Cola` con `_cabeza`, `_cola`, `_n` (mismo patrón que
`ListaEnlazada` de la actividad 3: nada de `list` de Python por dentro).

- `encolar(x)`: agrega al final. O(1).
- `decolar()`: retira y devuelve la cabeza. O(1). Lanza `ColaVaciaError` si
  está vacía.
- `esta_vacia()`, `__len__`.

Es la única pieza que `cola_prioridad.py` y `arbol_carpetas.py` conocen de
cada una (RNF3): ninguna de las dos sabe cómo está hecha por dentro.

## 3. Parte B — `cola_prioridad.py`

- `Solicitud` (dataclass): `dato`, `nivel` (1–3), `orden_llegada`.
- `ColaPrioridad`:
  - Tres instancias de `Cola` (una por nivel), en un diccionario `{1: Cola(),
    2: Cola(), 3: Cola()}`.
  - `PATRON_TURNOS = (1, 1, 2, 1, 1, 2, 3)` — constante de módulo, documentada
    con la demostración de la cota (`spec.md` §3).
  - `encolar(dato, nivel)`: valida nivel, crea `Solicitud`, la mete en la
    `Cola` de su nivel.
  - `decolar()`: mira `PATRON_TURNOS[indice]`; si esa cola tiene algo, se
    atiende; si no, se busca la de mayor prioridad no vacía. Avanza el índice
    del patrón **siempre** (incluso si el turno reservado estaba vacío), para
    que el ciclo no se alargue por culpa de un nivel momentáneamente sin
    solicitudes.
  - `esta_vacia()`, `cuantos_hay()` (desglose por nivel).

`simulacion.py` importa además una `ColaPrioridadEstricta` que se define en
el propio `simulacion.py` (no es un entregable de `cola_prioridad.py`: es
solo el punto de comparación): mismas tres `Cola`, pero `decolar()` siempre
elige la de mayor prioridad no vacía, sin patrón.

## 4. Parte B — `simulacion.py`

1. Generar una secuencia de 500 instantes con una semilla fija. En cada
   instante, cada nivel tiene una probabilidad independiente de que llegue
   una solicitud (nivel 1: 0.35, nivel 2: 0.30, nivel 3: 0.20), y entre los
   instantes 150 y 250 el nivel 1 sube a 0.65 (una «racha» de solicitudes
   urgentes, como una semana de evaluaciones) — el escenario que de verdad
   pone a prueba el mecanismo.
2. La **misma** secuencia de llegadas se reproduce contra las dos
   estrategias, para que la comparación sea justa.
3. En cada instante se atiende como máximo una solicitud (si hay alguna
   pendiente); se registra `espera = instante_atendido - instante_llegada`.
4. Al final: tiempo medio y peor tiempo de espera por nivel, para cada
   estrategia, en una tabla. Se interpreta el resultado (no solo se reporta):
   se señala si el nivel 3 quedó con una espera mucho mayor en la estrategia
   sin reserva.

## 5. Parte C — `arbol_carpetas.py`

- `Carpeta(nombre, entregas=0, hijos=None)`: `hijos` es una `list` de
  `Carpeta` (permitido, `constitucion.md` §2).
- `contar_entregas(carpeta)`: recursiva, caso base `carpeta is None`.
- `ruta_mas_profunda(carpeta)`: recursiva, caso base `carpeta is None`;
  compara longitudes de ruta entre hijos, se queda con la primera que logra
  superar (no igualar) el máximo, para desempatar por orden de inserción.
- `listar_por_niveles(carpeta)`: iterativa, con `Cola` de la Parte A
  (tuplas `(nodo, nivel)` en la cola).

## 6. Parte D — comparación cola vs. pila

- `pila.py`: `Pila` con la misma forma que `Cola` (nodos enlazados,
  `apilar`/`desapilar`/`esta_vacia`), solo para esta comparación.
- `arbol_carpetas.py` agrega `recorrer_por_niveles_con_pila(carpeta)`: mismo
  algoritmo que `listar_por_niveles`, pero con `Pila` en vez de `Cola` —
  deliberadamente, para que la diferencia de salida sea atribuible solo al
  cambio de estructura, no a un algoritmo distinto.
- `generar_recorridos.py`: construye el árbol de prueba de `spec.md`/
  `recorridos.md`, imprime ambas salidas, y ese texto real (no inventado) es
  el que se copia a `recorridos.md` (igual que `nodos_a_mano.py` →
  `nodos_a_mano.md` en la actividad 3).

## 7. Riesgos

| Riesgo | Mitigación |
|---|---|
| El problema «Uno» reconstruido no coincide con el real | Decisión explícita y marcada como pendiente en `spec.md` §2 y `task.md` |
| El patrón de turnos no da una cota real | Prueba dedicada: ráfaga sostenida de niveles 1/2, se verifica que nivel 3 sale dentro de `len(patrón)-1` atenciones |
| Confundir «recorrido con pila» con una pila de Python (`list`) | `pila.py` construida a mano, misma razón que `cola.py` |
