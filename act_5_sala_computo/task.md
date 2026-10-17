# Tareas

Orden de ejecución. `[x]` = hecha y verificada.

## Fase 0 — Especificación
- [x] T0.1 Redactar `constitucion.md`.
- [x] T0.2 Redactar `spec.md`: reconstrucción documentada del problema «Uno»,
      historias de usuario, RF, RNF, casos límite.
- [x] T0.3 Redactar `plan.md`.

## Fase 1 — Parte A: la cola simple
- [x] T1.1 `cola.py`: `Nodo`, `Cola` con nodos enlazados, sin `deque`.
- [x] T1.2 `test_cola.py`: casos normales + cola vacía + un elemento.

## Fase 2 — Parte B: la cola de prioridad
- [x] T2.1 `cola_prioridad.py`: 3 niveles sobre `Cola`, patrón de turnos
      reservados, documentado (por qué da una cota sin reloj).
- [x] T2.2 `test_cola_prioridad.py`: niveles, empates (FIFO dentro del
      nivel), cola vacía, y la prueba de la cota bajo ráfaga sostenida.
- [x] T2.3 `simulacion.py`: estrategia estricta (control) vs. con reserva,
      misma secuencia de llegadas, tabla de tiempo medio y peor caso.
- [x] T2.4 Correr `simulacion.py` y guardar `resultados_simulacion.txt`.

## Fase 3 — Parte C: el árbol de carpetas
- [x] T3.1 `arbol_carpetas.py`: `Carpeta`, `contar_entregas` y
      `ruta_mas_profunda` (recursivas), `listar_por_niveles` (con `Cola`).
- [x] T3.2 `test_arbol_carpetas.py`: árbol vacío, un nodo, árbol con varias
      ramas, empate de profundidad.

## Fase 4 — Parte D: la conexión cola/pila
- [x] T4.1 `pila.py`: misma forma que `cola.py`, para la comparación.
- [x] T4.2 `recorrer_por_niveles_con_pila` en `arbol_carpetas.py`.
- [x] T4.3 `generar_recorridos.py`: árbol de prueba, ambas salidas reales.
- [x] T4.4 `recorridos.md`: árbol dibujado/descrito, salidas capturadas,
      explicación de por qué difieren.

## Fase 5 — Entrega
- [x] T5.1 `python -m pytest` en verde.
- [x] T5.2 `README.md` con cómo correr todo.
- [ ] T5.3 Confirmar el texto real del problema «Uno» contra la plataforma
      (la captura que se compartió no lo incluía completo, `spec.md` §2) y
      ajustar si difiere de lo reconstruido.
- [ ] T5.4 Confirmar si se entrega solo o en equipo, y repartir los commits.
- [ ] T5.5 `git init` / commits / push, cuando se pida.
