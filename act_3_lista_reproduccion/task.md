# Tareas

Orden de ejecución. `[x]` = hecha y verificada.

## Fase 0 — Especificación
- [x] T0.1 Redactar `constitucion.md`.
- [x] T0.2 Redactar `spec.md` (contrato, decisiones, casos límite).
- [x] T0.3 Redactar `plan.md`.

## Fase 1 — Parte A: la cadena a mano
- [x] T1.1 `nodos_a_mano.py`: tres nodos enlazados y recorrido con `while`.
- [x] T1.2 Mostrar el error de reasignar el enlace antes de guardar el segundo
      (comprobado con `weakref`).
- [x] T1.3 `nodos_a_mano.md` con diagramas, salida real y la regla general.

## Fase 2 — Contrato y arreglo (actividad 2)
- [x] T2.1 `lista_arreglo.py` según `spec.md`.
- [x] T2.2 `test_contrato.py` (batería del contrato) + `conftest.py`.
- [x] T2.3 Ver la batería pasar con `ListaArreglo`.

## Fase 3 — Parte B: la lista enlazada
- [x] T3.1 `lista_enlazada.py` (sin ninguna `list` dentro).
- [x] T3.2 Pasar `test_contrato.py` **sin modificarlo**.

## Fase 4 — Parte C: los cuatro extremos
- [x] T4.1 Lista vacía (5 pruebas).
- [x] T4.2 Lista de un elemento (5 pruebas).
- [x] T4.3 Borrar el primero (5 pruebas).
- [x] T4.4 Borrar el último (6 pruebas).
- [x] T4.5 Mutación: 4 fallas típicas introducidas a propósito, las 4 detectadas.

## Fase 5 — Parte D: la decisión
- [x] T5.1 `benchmark.py`: las cuatro operaciones en las dos estructuras, N = 5.000.
- [x] T5.2 Costo del día con las frecuencias reales.
- [x] T5.3 Punto de quiebre de inserciones y de saltos.
- [x] T5.4 `comparacion.md`: tabla teórico vs. medido, cálculo, recomendación y
      qué cambiaría.

## Fase 6 — Entrega
- [x] T6.1 `python -m pytest` en verde (96 pruebas).
- [ ] T6.2 Verificar `pytest` en una máquina/entorno limpio.
- [ ] T6.3 Subir a GitHub con commits que muestren la contribución de cada integrante.
- [ ] T6.4 Enlazar el repositorio en D2L antes del domingo de la semana 6, 23:59.
