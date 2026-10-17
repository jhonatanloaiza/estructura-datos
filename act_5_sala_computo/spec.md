# Especificación — La sala de cómputo

Se escribió antes que el código; si el código y este documento no coinciden,
el que está mal es el código. Ver `constitucion.md` para los principios.

## 1. El caso, tal como llegó

> «La sala de cómputo atiende dos problemas distintos y quiere resolverlos
> con software.»
>
> **Dos.** El servidor de la sala guarda las entregas en carpetas anidadas
> por facultad, programa, curso y semestre. Necesitan poder responder tres
> preguntas: cuántas entregas hay en total bajo una carpeta, cuál es la ruta
> más profunda, y listar todo el contenido nivel por nivel para el informe.

El párrafo **«Uno»**, que describe el primer problema (atención por
prioridad), no se capturó completo en la imagen de la plataforma: la captura
empieza a mitad de esa sección. Lo que sí llegó completo son los entregables
y la rúbrica que lo describen:

- `cola_prioridad.py` con **tres niveles** y «el mecanismo que evita la
  espera indefinida».
- `simulacion.py` que compara **dos estrategias** con dos métricas (tiempo
  medio y peor tiempo de espera).
- El criterio de calificación «Cola de prioridad con espera acotada» exige
  que el mecanismo (envejecimiento, reserva de turnos, u otro) esté
  «implementado y justificado» y «demostrado con un caso de prueba».
- El título de la actividad es «La sala de cómputo: atención por prioridad y
  el árbol de carpetas», y el tema de la semana 9 (la que falta en la
  captura) antecede a «Semana 10: árboles y recorridos […] que necesita una
  cola», lo que indica que la cola simple de la Parte A se construye en la
  semana 9, junto con la cola de prioridad.

## 2. Reconstrucción del problema «Uno» (decisión explícita)

**Decisión:** a falta del párrafo original, se modela así, y queda pendiente
confirmarlo contra el texto real de la plataforma (`task.md`):

> La sala de cómputo recibe solicitudes de turno para usar un computador.
> Cada solicitud llega con un nivel de prioridad:
>
> - **Nivel 1 — Urgente:** una evaluación o sustentación en curso, o un daño
>   que bloquea una clase completa.
> - **Nivel 2 — Prioritaria:** una clase programada que necesita el equipo en
>   los próximos minutos.
> - **Nivel 3 — Normal:** una consulta o práctica libre, sin plazo inmediato.
>
> La sala debe atender siempre que pueda al de mayor prioridad, pero sin
> dejar esperando indefinidamente a quien pidió un turno normal si llega una
> racha sostenida de solicitudes urgentes y prioritarias.

**Por qué esta reconstrucción y no otra:** es la lectura más simple que hace
necesarias, a la vez, las dos piezas que el enunciado exige explícitamente
(tres niveles **y** un mecanismo contra la espera indefinida) sin inventar
requisitos que los entregables no piden (no hay mención a tiempos de servicio
distintos por tipo de trabajo, reservas con antelación, ni autenticación).

## 3. El mecanismo contra la espera indefinida: reserva de turnos

Se eligió **reserva de turnos** (una de las opciones que la rúbrica sugiere)
sobre envejecimiento (aging), por esta razón:

El envejecimiento necesita un reloj o contador de tiempo de espera por
solicitud y un umbral a partir del cual «promueve» su nivel; cuánto deba
envejecer para subir de nivel es un parámetro arbitrario que hay que ajustar
por prueba y error, y la cota de espera resultante es difícil de demostrar
con una prueba corta y determinista.

La reserva de turnos, en cambio, fija un **patrón de atención** que se repite
en ciclos, por ejemplo `(1, 1, 2, 1, 1, 2, 3)`: en cada posición del ciclo hay
un nivel «reservado». Si ese nivel tiene alguien esperando, se le atiende
aunque haya niveles más urgentes esperando también; si no tiene a nadie, se
atiende por prioridad estricta entre los que sí esperan. Esto da una cota
**demostrable sin reloj**: en cualquier ventana de 7 atenciones consecutivas
hay al menos una reservada para el nivel 3, así que el hueco entre dos
atenciones consecutivas de nivel 3 nunca supera `len(patrón) - 1 = 6`
atenciones de otros niveles — nivel 3 nunca deja de avanzar, aunque no
llegue a atender cada solicitud individual en ese plazo si ya hay otras de su
mismo nivel delante en su propia fila (`cola_prioridad.py`, documentado en el
módulo).

## 4. Historias de usuario

### HU1 — Pedir un turno

Como usuario de la sala, quiero registrar mi solicitud con su nivel de
prioridad, para entrar a la cola de atención.

**Criterios de aceptación**
- Dado un nivel 1, 2 o 3 válido, cuando registro, entonces mi solicitud entra
  a la cola de su nivel, en el orden en que llegué dentro de ese nivel.
- Dado un nivel fuera de {1, 2, 3}, cuando intento registrar, entonces se
  rechaza y la cola no cambia.

### HU2 — Atender el siguiente turno

Como operador de la sala, quiero atender siempre al siguiente turno según la
regla de prioridad y el patrón de reserva, para no dejar a nadie esperando
indefinidamente.

**Criterios de aceptación**
- Dado que hay solicitudes de nivel 1 o 2 esperando y el turno actual del
  patrón no está reservado para el nivel 3, cuando atiendo, entonces se
  atiende la de mayor prioridad disponible.
- Dado que el turno actual del patrón está reservado para el nivel 3 y hay
  alguien de nivel 3 esperando, cuando atiendo, entonces se atiende a esa
  persona, aunque haya niveles 1 o 2 esperando también.
- Dado que la cola está vacía, cuando intento atender, entonces recibo un
  error claro y la cola sigue vacía.

### HU3 — Medir si el mecanismo funciona

Como coordinador, quiero simular una jornada con una racha de solicitudes
urgentes y comparar el tiempo de espera con y sin el mecanismo de reserva de
turnos, para decidir si vale la pena aplicarlo.

**Criterios de aceptación**
- Dado un mismo flujo de llegadas, cuando simulo con la cola estricta (sin
  reserva) y con la cola de prioridad (con reserva), entonces obtengo el
  tiempo medio y el peor tiempo de espera por nivel en ambas.
- Dado el resultado, el peor caso del nivel 3 con reserva de turnos es
  **menor o igual** que sin reserva (el mecanismo no puede empeorar el peor
  caso que dice resolver).

### HU4 — Contar las entregas bajo una carpeta

Como administrador del servidor, quiero saber cuántas entregas hay en total
bajo una carpeta (incluyendo subcarpetas), para generar el informe.

**Criterios de aceptación**
- Dado un árbol de carpetas con entregas en distintos niveles, cuando cuento
  desde la raíz, entonces obtengo la suma de todas las entregas del árbol.
- Dado un nodo sin hijos, cuando cuento desde ahí, entonces obtengo solo sus
  propias entregas.
- Dado un árbol vacío (`None`), cuando cuento, entonces obtengo 0.

### HU5 — Encontrar la ruta más profunda

Como administrador, quiero saber cuál es la ruta más profunda del árbol, para
saber qué tan anidada está la estructura real.

**Criterios de aceptación**
- Dado un árbol con ramas de distinta profundidad, cuando pido la ruta más
  profunda, entonces obtengo la lista de nombres desde la raíz hasta el nodo
  más profundo, por la rama más larga.
- Dado un árbol de un solo nodo, cuando pido la ruta más profunda, entonces
  obtengo una ruta con ese único nombre.
- Dado un árbol vacío, cuando pido la ruta más profunda, entonces obtengo una
  ruta vacía.
- Dado un empate entre dos ramas de igual profundidad, se reporta la primera
  encontrada recorriendo los hijos en su orden de inserción (decisión
  explícita: el enunciado no dice cómo desempatar).

### HU6 — Listar el árbol nivel por nivel

Como administrador, quiero ver el árbol listado nivel por nivel, para
incluirlo en el informe tal como se organiza realmente la jerarquía.

**Criterios de aceptación**
- Dado cualquier árbol no vacío, cuando listo por niveles, entonces obtengo
  una lista de listas, una por profundidad, con los nombres en el orden en
  que se visitaron.
- Dado un árbol vacío, cuando listo por niveles, entonces obtengo una lista
  vacía, no un error.
- El listado usa la cola de la Parte A (`cola.py`), no una pila ni
  `collections.deque` (`constitucion.md` §2).

## 5. Requisitos funcionales

- **RF1.** Registrar una solicitud con nivel 1, 2 o 3 (HU1).
- **RF2.** Rechazar niveles fuera de {1, 2, 3} sin modificar la cola (HU1).
- **RF3.** Atender respetando prioridad estricta salvo en los turnos
  reservados del patrón, que priorizan el nivel reservado si tiene a alguien
  esperando (HU2).
- **RF4.** Reportar un error al atender o consultar con la cola vacía, sin
  modificarla (HU2).
- **RF5.** Simular una secuencia de llegadas contra dos estrategias (con y
  sin reserva de turnos) y reportar tiempo medio y peor tiempo de espera por
  nivel en cada una (HU3).
- **RF6.** Contar recursivamente las entregas bajo cualquier nodo del árbol
  de carpetas (HU4).
- **RF7.** Calcular recursivamente la ruta más profunda del árbol (HU5).
- **RF8.** Listar el árbol nivel por nivel usando la cola propia (HU6).

## 6. Requisitos no funcionales

- **RNF1 — Determinismo.** `simulacion.py` y `generar_recorridos.py` usan una
  semilla fija: la misma corrida produce siempre el mismo resultado.
- **RNF2 — Cota demostrable.** El mecanismo de reserva de turnos se puede
  verificar con una prueba corta y determinista (sin reloj real), no solo
  describir en prosa.
- **RNF3 — Independencia de estructuras.** `cola.py` no sabe que existe
  `cola_prioridad.py` ni `arbol_carpetas.py`; estos la importan y la usan
  como una caja negra (interfaz `encolar`/`decolar`/`esta_vacia`).
- **RNF4 — Recursión con caso base explícito.** Toda función recursiva sobre
  el árbol maneja el árbol vacío y el nodo sin hijos sin casos especiales
  fuera de la propia recursión.
- **RNF5 — Reproducibilidad.** `python -m pytest` pasa en cualquier máquina
  con Python 3.10+ y sin dependencias externas (todo el proyecto es
  biblioteca estándar + `pytest`).

## 7. Casos límite exigidos

**Cola de prioridad**
1. Cola vacía (atender, consultar).
2. Un solo nivel con solicitudes, los otros vacíos.
3. Ráfaga sostenida de niveles 1 y 2 mientras alguien de nivel 3 espera: debe
   salir dentro de la cota del patrón, no quedar indefinidamente atrás.

**Árbol de carpetas**
4. Árbol vacío (`None`) en las tres consultas.
5. Árbol de un solo nodo (sin hijos) en las tres consultas.
6. Empate de profundidad entre dos ramas (HU5, desempate documentado).

## 8. Fuera de alcance

- Tiempo de servicio distinto según el nivel o el tipo de solicitud (se
  asume que atender a cualquiera toma 1 unidad de tiempo).
- Reservar un turno con antelación o cancelar una solicitud ya registrada.
- Persistencia en disco del árbol de carpetas o de la cola.
- Un algoritmo que asigne el nivel de prioridad automáticamente: lo asigna
  quien registra la solicitud.

## 9. Criterios de aceptación del proyecto

- `pytest` pasa: `test_cola.py`, `test_cola_prioridad.py`,
  `test_arbol_carpetas.py`.
- `simulacion.py` produce la tabla de tiempo medio y peor caso para las dos
  estrategias (HU3), capturada en `resultados_simulacion.txt`.
- `recorridos.md` muestra la salida real (no inventada) del recorrido por
  niveles con cola y con pila sobre el mismo árbol de prueba, con la
  explicación de por qué difieren.
- El árbol de prueba está dibujado o descrito en `recorridos.md` para que se
  pueda verificar a mano.
