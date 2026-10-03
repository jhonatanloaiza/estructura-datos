# Bitácora de interacción con la IA

Registro real de las interacciones con el asistente de IA durante la
construcción del CDA de atención médica. Es un registro de uso de la
herramienta, no un reemplazo de la autoría del trabajo: cada decisión de
diseño quedó documentada y justificada en `spec.md`, `plan.md` y
`constitucion.md`; aquí se deja constancia de **cómo** se llegó a ellas.

## 1. Encargo inicial

**2026-10-02.** Se entregó al asistente el enunciado de la actividad (tal
como lo dio el curso, pegado en el chat) junto con un fragmento de código de
referencia: un `main.py` de FastAPI con un modelo `Datos` (Pydantic) y cuatro
rutas de ejemplo (`/`, `/items/{item_id}`, `/consulta/{nombre}`, `/guardar`).

El encargo, resumido:

- Construir un CDA (cola de atención) expuesto en una API, para un sistema de
  atención médica.
- Definir el sistema de atención y las reglas de priorización.
- La API debe permitir: registrar, consultar quién sigue, atender (paciente o
  vehículo), sacar de la cola, y mostrar cuántos faltan.
- Seguir metodología SDD: analizar el requerimiento, historias de usuario con
  criterios de aceptación, RF/RNF, constitución, plan, tareas.
- Llevar esta bitácora de interacción con la IA.
- Se pidió explícitamente no incluir referencias, menciones ni coautoría de la
  herramienta en el código ni en los commits.

## 2. Qué decidió el asistente y por qué (ambigüedades resueltas)

El enunciado no especifica varios detalles. El asistente los resolvió y los
dejó registrados como decisiones explícitas en `spec.md`, no escondidos en el
código:

| Ambigüedad del enunciado | Decisión tomada | Dónde quedó documentada |
|---|---|---|
| Qué es un «CDA» | Cola de prioridad («Cola de Atención»): montículo binario que mezcla pacientes y vehículos en una sola fila ordenada por urgencia | `spec.md` §1–§2 |
| Reglas de priorización no dadas | Escala de 5 niveles estilo triaje hospitalario (1 = resucitación … 5 = no urgente), desempate por orden de llegada | `spec.md` §3 |
| «Atender a un vehículo o a un paciente» | Una sola cola, un solo criterio de orden; el tipo es un dato informativo para el personal, no altera la prioridad | `constitucion.md` §4 |
| «Sacar de la cola» vs. «atender» | Dos operaciones distintas: atender marca la solicitud como atendida, sacar la retira sin esa marca (se fue, la trasladaron, error de registro) | `spec.md` HU3 vs. HU4 |
| Estructura de datos interna | Montículo binario (min-heap) escrito a mano, sin `heapq`, para practicar la estructura en vez de usar la de la librería estándar | `constitucion.md` §2 |
| Persistencia | En memoria, sin base de datos (no se pidió) | `spec.md` §8 |

## 3. Orden de trabajo seguido

El asistente respetó el orden que exige el propio proyecto (`constitucion.md`
§1: especificar antes de programar):

1. `constitucion.md` — principios del proyecto.
2. `spec.md` — sistema de atención, reglas de priorización, historias de
   usuario con criterios de aceptación, RF, RNF, casos límite, fuera de
   alcance.
3. `plan.md` — diseño técnico del montículo y de la API.
4. `task.md` — checklist de tareas por fase.
5. `metodos_http.md` — investigación de los métodos HTTP pedida por el
   enunciado, y el porqué de cada método elegido para cada endpoint.
6. Código: `cola_atencion.py` (núcleo, sin FastAPI) y luego `main.py` (API),
   siguiendo el estilo minimalista del fragmento de referencia (`app =
   FastAPI()`, modelo `BaseModel`, funciones que devuelven diccionarios).
7. Pruebas: `test_cola_atencion.py` (núcleo) y `test_api.py` (API).

## 4. Verificación hecha durante la construcción

- Se corrió `python -m pytest -v`: en la primera corrida falló una prueba de
  la API (`test_estado_desglosa_por_tipo_y_nivel`) porque esperaba una clave
  entera (`cuerpo["por_nivel"][1]`) en una respuesta JSON, donde las claves de
  objeto siempre son texto (`"1"`). Se corrigió la **prueba**, no el código de
  la API, porque el comportamiento de la API era el correcto. Tras el ajuste,
  las 42 pruebas pasaron.
- Se hicieron **pruebas de mutación manuales** sobre `cola_atencion.py`: se
  rompió a propósito la lógica del montículo de cinco maneras distintas (no
  actualizar el índice al intercambiar nodos, subir sin comparar, ignorar el
  hijo derecho al bajar, no decidir entre subir/bajar tras eliminar, ignorar
  el desempate por orden de llegada) y se confirmó que cada mutación hacía
  fallar al menos una prueba existente, antes de descartar los cambios.

## 5. Publicación y reconciliación del repositorio

**2026-10-02/03.** Tras terminar el código, se pidió al asistente iniciar git
y subir el trabajo a `https://github.com/jhonatanloaiza/estructura-datos`.
Apareció una complicación que no era de código sino de control de versiones,
y se resolvió en conjunto con quien pidió el trabajo (los comandos de git los
ejecutó esa persona en un Codespace de GitHub, al que el asistente no tiene
acceso; el asistente solo pudo diagnosticar y guiar desde la copia local en
Windows):

1. Al hacer `git push`, el repositorio remoto ya tenía historial propio
   (`clase1`, `clase2`, `ejercicio_carrito` de actividades previas). El
   asistente integró los commits de `act_3`/`act_4` **encima** de ese
   historial remoto (`git rebase --onto origin/main --root`) en vez de
   sobrescribirlo, y el push fue un avance normal (fast-forward).
2. Días después, al abrir un Codespace de GitHub para el mismo repositorio,
   las carpetas `act_3_lista_reproduccion` y `act_4_cola_atencion_medica` no
   aparecían. El diagnóstico: ese Codespace tenía su **propio historial local**
   (su propio `git init`, con commits desde `Initial commit` hasta
   `agrego clase 1 y 2`), sin ningún ancestro en común con lo que había en
   GitHub — dos historiales genuinamente no relacionados (`git log --not
   origin/main` lo confirmó: 5 commits locales que GitHub no tenía).
3. El asistente explicó la causa y guio, paso a paso, la reconciliación sin
   perder trabajo: conservar primero el trabajo sin confirmar de `semana8`
   (`git commit`), fusionar con `git pull origin main --allow-unrelated-histories`,
   y sellar el commit de mezcla con `git commit --no-edit`. La fusión se
   resolvió sola, sin conflictos de archivo.
4. Una vez confirmado el `push` final, el asistente verificó desde su propia
   copia (`git fetch`, `git log --graph`, `git ls-tree`) que el árbol
   resultante tenía las seis carpetas esperadas sin duplicados, y corrió
   `pytest` sobre `act_3` y `act_4` desde ese estado fusionado: 96 y 42
   pruebas, respectivamente, siguieron pasando.
5. Quedó un detalle cosmético sin corregir (a petición de quien pidió el
   trabajo, por no tener impacto real): el mensaje del commit de mezcla
   `fc0e452` incluye el texto de ayuda de git que debía descartarse como
   comentario y no se descartó.

## 6. Qué quedó pendiente (no resuelto por la IA)

- Confirmar con la guía real del curso el número y nombre exacto de esta
  actividad (no se adjuntó una captura de la plataforma, a diferencia de la
  actividad anterior).
- Decidir si el proyecto se entrega solo o en equipo, y repartir los commits
  en ese caso.
- Desplegar o ejecutar la API fuera de la máquina local, si el curso lo pide.
- Limpiar el mensaje del commit de mezcla `fc0e452` (ver §5.5), si se decide
  que vale la pena reescribir historial ya publicado.
