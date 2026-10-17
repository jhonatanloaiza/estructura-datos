# Constitución del proyecto — La sala de cómputo

Principios que gobiernan cualquier decisión de este trabajo. Si una decisión de
`plan.md` o una tarea de `task.md` los contradice, la que está mal es la
decisión.

## 1. Especificar antes de programar

Orden: constitución → spec (historias de usuario, RF, RNF) → plan → tareas →
código. Si el código y `spec.md` no coinciden, el que está mal es el código.

## 2. Cada estructura se construye, no se importa

- La cola simple (`cola.py`, Parte A) es un TAD propio con nodos enlazados:
  nada de `collections.deque` ni de usar una `list` de Python como cola.
- La cola de prioridad (`cola_prioridad.py`, Parte B) se construye sobre esa
  cola simple: nada de `heapq`.
- El recorrido por niveles del árbol (Parte D) usa esa misma cola simple, no
  `collections.deque` ni ninguna otra.
- El árbol de carpetas (`arbol_carpetas.py`, Parte C) sí puede usar una `list`
  de Python para guardar los hijos de un nodo: el enunciado no lo prohíbe y no
  es el objeto de estudio de esta actividad (lo son la recursión y la cola).

## 3. El conteo y la profundidad son recursivos; el listado por niveles no

`contar_entregas` y `ruta_mas_profunda` se resuelven con una función que se
llama a sí misma sobre los hijos de un nodo, con un caso base explícito (nodo
`None` o sin hijos). Un bucle que recorra una lista de rutas ya aplanada no
cuenta como recorrer el árbol. `listar_por_niveles`, en cambio, es
iterativo por definición: usa la cola de la Parte A para ir sacando un nivel
antes que el siguiente.

## 4. El mecanismo contra la espera indefinida se elige y se justifica

Se usa **reserva de turnos** (un patrón fijo de atención que repite un hueco
reservado por nivel) y no envejecimiento (aging), porque la reserva de turnos
da una cota de espera **demostrable sin reloj ni temporizador**: alcanza con
contar atenciones. La razón se explica en `cola_prioridad.py` (docstring) y en
`spec.md`; no es una elección arbitraria.

## 5. La comparación cola-vs-pila es honesta

`recorridos.md` no describe de memoria cómo se vería el recorrido con una
pila: el resultado sale de ejecutar realmente el código sobre el mismo árbol
de prueba y de capturar la salida (igual que `nodos_a_mano.md` en la actividad
3), no de una afirmación teórica sin verificar.

## 6. Las ambigüedades del enunciado se declaran, no se esconden

El problema «Uno» (atención por prioridad) no llegó completo en la captura
que se compartió: solo se vieron los entregables y la rúbrica que lo
describen. La reconstrucción del escenario queda en `spec.md` §2 marcada
explícitamente como una decisión del colaborador, pendiente de confirmar
contra el texto real de la plataforma (`task.md`).

## 7. Reproducible en una máquina limpia

`python -m pytest` pasa sin configuración extra. `python simulacion.py` y
`python generar_recorridos.py` son deterministas (semilla fija) y regeneran
exactamente los archivos de resultados que se entregan.
