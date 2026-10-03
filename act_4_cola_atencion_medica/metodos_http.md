# Métodos HTTP y su uso en este proyecto

Investigación previa a diseñar la API (`plan.md` §3). Un método HTTP le dice
al servidor **qué intención** tiene la petición sobre un recurso; la URL dice
**sobre cuál** recurso.

## 1. Los métodos

| Método | Para qué sirve | ¿Seguro? | ¿Idempotente? | ¿Tiene cuerpo de petición? |
|---|---|---|---|---|
| `GET` | Leer un recurso, sin cambiar nada en el servidor | Sí | Sí | No (no se usa) |
| `POST` | Crear un recurso nuevo, o ejecutar una acción que cambia estado y no es solo «poner un valor» | No | No | Sí |
| `PUT` | Reemplazar **por completo** un recurso existente (o crearlo en una URL conocida) | No | Sí | Sí |
| `PATCH` | Modificar **parcialmente** un recurso existente | No | No (en general) | Sí |
| `DELETE` | Eliminar un recurso | No | Sí | Normalmente no |
| `HEAD` | Como `GET`, pero solo pide las cabeceras (sin cuerpo de respuesta) | Sí | Sí | No |
| `OPTIONS` | Preguntar qué métodos admite una ruta (lo usan los navegadores para CORS) | Sí | Sí | No |

**Seguro** quiere decir que la petición no modifica el estado del servidor (se
puede repetir, cachear, precargar, sin consecuencias). **Idempotente** quiere
decir que hacer la misma petición una vez o cien veces dos deja el servidor en
el mismo estado que hacerla una sola vez (no que la respuesta sea idéntica).

Por eso `DELETE /cola/7` es idempotente (borrar algo que ya no existe no
cambia nada más que la primera vez), pero no es seguro (si existía, el
servidor cambió). Y `POST` nunca es idempotente porque cada llamada se asume
que produce un efecto nuevo (otra solicitud registrada, otra atención).

## 2. Por qué cada endpoint del CDA usa el método que usa

| Endpoint | Método elegido | Razón |
|---|---|---|
| `POST /registrar` | `POST` | Crea una solicitud **nueva** cada vez que se llama; dos llamadas idénticas deben producir dos solicitudes distintas (no es idempotente por diseño: cada registro es un evento real). |
| `GET /siguiente` | `GET` | Solo lee la raíz del montículo, no cambia la cola. Se puede llamar cuantas veces se quiera sin efecto. |
| `POST /atender` | `POST` | Aunque no lleva cuerpo, **cambia el estado** (retira el elemento de mayor prioridad): dos llamadas seguidas atienden a dos personas distintas, así que no puede ser `GET` (violaría «seguro») ni tiene sentido como `PUT`/`PATCH` (no se está reemplazando ni editando un recurso con una URL propia, se está consumiendo el siguiente de una cola). |
| `DELETE /cola/{id}` | `DELETE` | Elimina un recurso identificado por su `id` en la URL. Llamarlo dos veces sobre el mismo `id` d: la primera lo saca, la segunda responde 404 porque ya no existe — el estado final es el mismo, por eso es idempotente. |
| `GET /estado` | `GET` | Solo lee contadores, no cambia nada. |
| `GET /cola` | `GET` | Solo lista lo pendiente, no cambia nada. |

## 3. Por qué no se usaron `PUT` ni `PATCH`

El proyecto no tiene una operación de «reemplazar» o «editar» una solicitud ya
registrada (`spec.md` §8, fuera de alcance: no hay forma de cambiar el nivel
de prioridad de algo que ya está en la cola). Si esa operación se agregara en
el futuro, el método correcto sería `PATCH /cola/{id}` (cambia solo el campo
`nivel_prioridad`, no reemplaza la solicitud completa), no `PUT`, porque
`PUT` exigiría reenviar el recurso entero y no tiene sentido reemplazar
`orden_llegada` o `id`, que no deberían cambiar nunca.

## 4. Códigos de estado que la API usa junto con estos métodos

| Código | Cuándo | Con qué método aparece aquí |
|---|---|---|
| `200 OK` | Operación exitosa con cuerpo de respuesta | `GET`, `DELETE`, `POST /atender` |
| `201 Created` | Se creó un recurso nuevo | `POST /registrar` |
| `404 Not Found` | Cola vacía (`/siguiente`, `/atender`) o `id` inexistente (`/cola/{id}`) | `GET`, `POST`, `DELETE` |
| `422 Unprocessable Entity` | El cuerpo de la petición no cumple el esquema (`tipo` inválido, `nivel_prioridad` fuera de 1–5) | `POST /registrar` |
