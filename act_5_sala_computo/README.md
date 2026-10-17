# La sala de cómputo: atención por prioridad y el árbol de carpetas

Dos TAD construidos a mano (cola simple y cola de prioridad con reserva de
turnos) y un árbol de carpetas recorrido de dos formas, sobre el mismo
servidor de entregas. Documentación completa en [`spec.md`](spec.md); el
razonamiento de diseño en [`plan.md`](plan.md) y
[`constitucion.md`](constitucion.md).

> **Nota:** la captura de la plataforma que dio origen a este trabajo no
> incluía completo el párrafo del problema «Uno» (atención por prioridad).
> `spec.md` §2 documenta cómo se reconstruyó a partir de los entregables y la
> rúbrica, y queda pendiente confirmarlo contra el enunciado real
> (`task.md`).

## Instalar

Sin dependencias externas más allá de `pytest`:

```bash
pip install pytest
```

## Correr las pruebas

```bash
python -m pytest -v
```

35 pruebas: `test_cola.py` (Parte A), `test_cola_prioridad.py` (Parte B, con
la demostración de la cota contra la espera indefinida), y
`test_arbol_carpetas.py` (Partes C y D).

## Reproducir la simulación (Parte B)

```bash
python simulacion.py
```

Compara, con la misma secuencia de llegadas, una cola de prioridad estricta
contra la cola con reserva de turnos, y reporta tiempo medio y peor caso por
nivel. Salida capturada en
[`resultados_simulacion.txt`](resultados_simulacion.txt).

## Reproducir la comparación cola-vs-pila (Parte D)

```bash
python generar_recorridos.py
```

Construye el árbol de prueba y muestra el recorrido por niveles con la cola
propia y el mismo recorrido con una pila. Salida capturada en
[`salida_recorridos.txt`](salida_recorridos.txt) y explicada en
[`recorridos.md`](recorridos.md).

## Archivos

| Archivo | Qué es |
|---|---|
| `cola.py` | Parte A: cola FIFO con nodos enlazados |
| `cola_prioridad.py` | Parte B: cola de prioridad, 3 niveles, reserva de turnos |
| `simulacion.py` | Parte B: compara con/sin reserva de turnos |
| `pila.py` | Parte D: pila LIFO, solo para la comparación |
| `arbol_carpetas.py` | Partes C y D: `Carpeta` y las tres consultas |
| `generar_recorridos.py` | Parte D: genera la salida real de `recorridos.md` |
