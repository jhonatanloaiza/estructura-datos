# Parte D — La conexión: por qué una pila no sirve para esto

Salida real de [`generar_recorridos.py`](generar_recorridos.py) (capturada en
[`salida_recorridos.txt`](salida_recorridos.txt), nada escrito de memoria),
sobre el árbol de prueba que también usa
[`test_arbol_carpetas.py`](test_arbol_carpetas.py).

## El árbol de prueba

```
Ingenieria
├── Sistemas
│   ├── EDD (2 entregas)
│   │   └── 2026-1 (3 entregas)
│   └── BD (1 entrega)
└── Industrial
    └── Procesos
        └── 2025-2 (4 entregas)
```

8 nodos, 4 niveles de profundidad (0 a 3). `contar_entregas(Ingenieria)` da
10 (2+3+1+4); `ruta_mas_profunda(Ingenieria)` es
`["Ingenieria", "Sistemas", "EDD", "2026-1"]` (verificado en
`test_arbol_carpetas.py`).

## Recorrido con la `Cola` de la Parte A (correcto: nivel por nivel)

```
nivel 0: ['Ingenieria']
nivel 1: ['Sistemas', 'Industrial']
nivel 2: ['EDD', 'BD', 'Procesos']
nivel 3: ['2026-1', '2025-2']

orden de visita: ['Ingenieria', 'Sistemas', 'Industrial', 'EDD', 'BD',
                   'Procesos', '2026-1', '2025-2']
```

Cada nivel completo se visita antes de pasar al siguiente: primero la raíz,
después sus dos hijos, después los tres nietos, y al final los dos
bisnietos. Es el recorrido que de verdad sirve para el informe de la sala
(`spec.md` HU6): se puede cortar en cualquier nivel y el resultado sigue
siendo «todo lo que hay hasta esa profundidad».

## El mismo algoritmo, cambiando `Cola` por `Pila`

```
visita: 'Ingenieria' (nivel 0)
visita: 'Industrial'  (nivel 1)
visita: 'Procesos'    (nivel 2)
visita: '2025-2'      (nivel 3)
visita: 'Sistemas'    (nivel 1)
visita: 'BD'          (nivel 2)
visita: 'EDD'         (nivel 2)
visita: '2026-1'      (nivel 3)

orden de visita: ['Ingenieria', 'Industrial', 'Procesos', '2025-2',
                   'Sistemas', 'BD', 'EDD', '2026-1']
```

Mismos 8 nodos (`set(orden_cola) == set(orden_pila)` es `True`), pero en un
orden completamente distinto (`orden_cola == orden_pila` es `False`).

## Por qué difieren, aunque el código es idéntico salvo la estructura

El algoritmo de `listar_por_niveles`/`recorrer_por_niveles_con_pila` es el
mismo en los dos casos: sacar un nodo, registrarlo, meter a sus hijos. La
diferencia la pone **qué nodo sale primero** de cada estructura:

- La **cola** es FIFO: lo primero que entró es lo primero que sale. Cuando se
  procesa `Ingenieria` se encolan `Sistemas` e `Industrial`, en ese orden —
  y como la cola respeta ese orden, `Sistemas` sale antes que `Industrial`,
  y los hijos de ambos quedan **detrás** de los dos en la cola. Por eso el
  recorrido nunca baja de nivel sin haber agotado el nivel anterior.

- La **pila** es LIFO: lo último que entró es lo primero que sale. Al
  procesar `Ingenieria` se apilan `Sistemas` e `Industrial` en ese orden,
  pero como la pila invierte, `Industrial` (el último en entrar) es el
  siguiente en salir — **no** `Sistemas`. Y en cuanto sale `Industrial`, se
  apila `Procesos`, que queda en el tope: se desapila antes que `Sistemas`,
  que lleva más tiempo esperando. El resultado es que la pila se mete por
  una sola rama hasta el fondo (`Ingenieria → Industrial → Procesos →
  2025-2`) antes de volver a subir a `Sistemas`: es un recorrido en
  profundidad, no un recorrido por niveles.

En una palabra: el orden de salida de la estructura auxiliar **es** el orden
del recorrido. Una cola lo mantiene por niveles porque no deja que nada se
adelante a lo que ya estaba esperando; una pila, al revés, siempre le da el
turno a lo último que llegó, así que la rama que se visitó de último es la
que se termina de explorar primero.
