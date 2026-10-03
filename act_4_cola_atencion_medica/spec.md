# Especificación — CDA de atención médica

Se escribió antes que el código; si el código y este documento no coinciden,
el que está mal es el código. Ver `constitucion.md` para los principios.

## 1. El requerimiento, tal como llegó

> «Realizar un CDA en una API para un sistema de atención médica. Definir el
> sistema de atención y las reglas de priorización. La API debe permitir
> guardar datos o registrarse, consultar quién es el siguiente, atender a un
> vehículo o a un paciente, sacar a alguien de la cola, y mostrar cuántos
> faltan / cuántos hay por atender.»

El enunciado trae cinco verbos (registrar, consultar, atender, sacar, mostrar)
pero no dice qué es exactamente un «CDA», cómo se calcula la prioridad entre un
paciente y un vehículo, ni qué significa «atender». Antes de programar se fija
cada punto.

## 2. El sistema de atención

Es el punto de ingreso de una urgencia médica (una sala de triaje). Llegan dos
tipos de solicitudes:

- **Paciente**: una persona que se presenta por sus propios medios o es
  remitida, y necesita ser evaluada.
- **Vehículo**: una ambulancia (u otro vehículo de traslado) que trae un
  paciente y necesita que el personal lo reciba en el andén de urgencias.

Un encargado de triaje registra la solicitud con un **nivel de prioridad**
(§3). El personal médico consulta repetidamente «quién sigue» y, cuando puede
recibir a alguien, lo **atiende**: lo saca de la cola y queda constancia de que
fue atendido. Una solicitud también puede salir de la cola sin ser atendida
(por ejemplo, el paciente se retiró, o fue remitido a otra sede): eso es
«sacar de la cola», una operación distinta de «atender».

## 3. Reglas de priorización

Escala de 5 niveles, inspirada en los sistemas de triaje hospitalario (número
más bajo = atención más urgente):

| Nivel | Nombre | Significado | Tiempo esperado |
|---|---|---|---|
| 1 | Resucitación | Riesgo vital inmediato | Atención inmediata |
| 2 | Emergencia | Riesgo vital alto, no inmediato | Minutos |
| 3 | Urgente | Requiere atención pronta | Hasta 1 hora |
| 4 | Menos urgente | Puede esperar | Varias horas |
| 5 | No urgente | Consulta de rutina | Sin apremio |

**Orden de atención:** primero por `nivel_prioridad` ascendente (1 antes que
5); en caso de empate, por **orden de llegada** (quien se registró primero,
sale primero). El nivel lo asigna quien registra (el enunciado no describe un
algoritmo clínico de triaje; automatizarlo está fuera de alcance, ver §8).

**Pacientes y vehículos compiten por igual**: el tipo no altera el orden, solo
describe cómo debe proceder el personal al atender (ver `constitucion.md` §4).

## 4. Historias de usuario

### HU1 — Registrar una solicitud

Como encargado de triaje, quiero registrar a un paciente o un vehículo con su
nivel de prioridad, para que entre a la cola de atención.

**Criterios de aceptación**
- Dado que relleno nombre, identificación, motivo, tipo (`paciente` o
  `vehiculo`) y nivel de prioridad (1 a 5) válidos, cuando registro, entonces
  la solicitud queda en la cola y recibo su identificador y su posición actual.
- Dado un nivel de prioridad fuera de 1–5, cuando intento registrar, entonces
  la solicitud se rechaza y la cola no cambia.
- Dado un tipo distinto de `paciente`/`vehiculo`, cuando intento registrar,
  entonces la solicitud se rechaza.

### HU2 — Consultar quién es el siguiente

Como personal médico, quiero ver quién sigue sin sacarlo de la cola, para
decidir si ya puedo atenderlo.

**Criterios de aceptación**
- Dado que hay al menos una solicitud pendiente, cuando consulto el siguiente,
  entonces obtengo la de mayor prioridad (y más antigua en caso de empate) sin
  que la cola cambie de tamaño.
- Dado que la cola está vacía, cuando consulto el siguiente, entonces recibo un
  error claro (404), no una solicitud inventada.

### HU3 — Atender a la siguiente solicitud

Como personal médico, quiero atender a la siguiente solicitud (paciente o
vehículo) para quitarla de la cola y registrar que fue atendida.

**Criterios de aceptación**
- Dado que hay al menos una solicitud pendiente, cuando atiendo, entonces se
  retira la de mayor prioridad y la respuesta indica su `tipo`, para que el
  personal sepa si debe recibir un vehículo o evaluar un paciente.
- Dado que la cola está vacía, cuando intento atender, entonces recibo un error
  (404) y la cola sigue vacía.

### HU4 — Sacar a alguien de la cola sin atenderlo

Como encargado de triaje, quiero sacar una solicitud específica de la cola
(sin que cuente como atendida), para reflejar que se retiró, fue trasladada o
se registró por error.

**Criterios de aceptación**
- Dado un identificador que existe en la cola, cuando lo saco, entonces
  desaparece de la cola y el resto conserva su orden de prioridad.
- Dado un identificador que no existe (o ya fue atendido/sacado antes),
  cuando intento sacarlo, entonces recibo un error (404) y la cola no cambia.

### HU5 — Ver cuántos faltan

Como coordinador de urgencias, quiero ver cuántas solicitudes hay pendientes
en total y por tipo, para dimensionar al personal disponible.

**Criterios de aceptación**
- Dado cualquier estado de la cola, cuando consulto el estado, entonces
  obtengo el total pendiente, el desglose por tipo (`paciente`/`vehiculo`) y el
  desglose por nivel de prioridad.
- Dado que la cola está vacía, cuando consulto el estado, entonces el total es
  0 y no es un error.

## 5. Requisitos funcionales

- **RF1.** El sistema permite registrar una solicitud con tipo, nombre,
  identificación, motivo y nivel de prioridad (HU1).
- **RF2.** El sistema asigna a cada solicitud un identificador único y un
  orden de llegada al momento de registrarla.
- **RF3.** El sistema permite consultar la siguiente solicitud a atender sin
  retirarla de la cola (HU2).
- **RF4.** El sistema permite atender la siguiente solicitud, retirándola de
  la cola (HU3).
- **RF5.** El sistema permite retirar una solicitud puntual por su
  identificador, sin marcarla como atendida (HU4).
- **RF6.** El sistema reporta cuántas solicitudes quedan pendientes, en total,
  por tipo y por nivel de prioridad (HU5).
- **RF7.** El orden de atención respeta `(nivel_prioridad, orden_llegada)` en
  todo momento, sin importar el tipo de solicitud (§3).
- **RF8.** Toda operación sobre una cola vacía o sobre un identificador
  inexistente se rechaza con un error explícito, sin modificar la cola.

## 6. Requisitos no funcionales

- **RNF1 — Rendimiento.** Registrar, consultar el siguiente y atender son
  O(log n) respecto al número de solicitudes pendientes (montículo binario).
  Sacar una solicitud puntual es O(n) (buscar su posición) + O(log n)
  (restaurar el montículo); se documenta como costo aceptado, no oculto.
- **RNF2 — Validación de entradas.** Ningún dato inválido (tipo fuera de
  catálogo, prioridad fuera de 1–5, texto vacío) llega a crear una solicitud.
- **RNF3 — Independencia de capas.** El CDA (`cola_atencion.py`) se puede
  importar y probar sin levantar un servidor HTTP (`constitucion.md` §3).
- **RNF4 — Pruebas automatizadas.** El núcleo y la API tienen pruebas propias;
  los casos límite de §7 están cubiertos uno por uno.
- **RNF5 — Reproducibilidad.** `python -m pytest` y `uvicorn main:app` corren
  igual en cualquier máquina con las dependencias de `requirements.txt`.

## 7. Casos límite exigidos

1. Cola vacía (consultar siguiente, atender, sacar, estado).
2. Un solo elemento (registrar, consultar, atender, vuelve a quedar vacía).
3. Empate de nivel de prioridad (dos solicitudes con el mismo nivel: gana la
   que llegó primero).
4. Sacar un nodo que no es la raíz del montículo (del medio o una hoja), y
   comprobar que el resto sigue saliendo en orden correcto al drenar la cola.

## 8. Fuera de alcance

- Un algoritmo clínico que calcule el nivel de prioridad a partir de síntomas:
  el nivel lo asigna una persona al registrar.
- Autenticación/autorización de quién puede registrar o atender.
- Persistencia en disco o base de datos: el estado vive en memoria del
  proceso y se reinicia con el servidor.
- Historial de solicitudes ya atendidas o sacadas (no se exige una bitácora de
  atenciones pasadas, solo el estado de la cola pendiente).
- Reordenar la prioridad de una solicitud ya registrada (no hay «actualizar»).

## 9. Criterios de aceptación del proyecto

- `pytest` pasa: pruebas del núcleo (`test_cola_atencion.py`) y de la API
  (`test_api.py`).
- Los cinco verbos del enunciado (guardar/registrar, consultar siguiente,
  atender, sacar, mostrar cuántos faltan) están expuestos como endpoints
  documentados en `metodos_http.md`.
- `constitucion.md`, `spec.md`, `plan.md`, `task.md` y `bitacora_ia.md` están
  completos.
