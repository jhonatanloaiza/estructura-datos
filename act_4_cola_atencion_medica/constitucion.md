# Constitución del proyecto — CDA de atención médica

Principios que gobiernan cualquier decisión de este trabajo. Si una decisión de
`plan.md` o una tarea de `task.md` los contradice, la que está mal es la
decisión.

## 1. Especificar antes de programar

Orden de trabajo: constitución → spec (historias de usuario, RF, RNF) → plan →
tareas → código. Si el código y `spec.md` no coinciden, el que está mal es el
código.

## 2. El CDA es una estructura, no un framework

La Cola de Atención (CDA) es un montículo binario (min-heap) implementado a
mano sobre un arreglo (`list` de Python usada solo como bloque indexable, sin
`heapq` ni ninguna otra cola de prioridad de la librería estándar). Subir y
bajar elementos se escriben con comparaciones e índices explícitos
(`2*i+1`, `2*i+2`, `(i-1)//2`), igual que en la actividad anterior se prohibió
`list.insert`/`list.pop` para desplazar un arreglo.

## 3. El CDA no sabe que existe HTTP

`cola_atencion.py` es una clase de Python que se puede importar y probar sin
levantar ningún servidor. `main.py` (FastAPI) es una capa delgada que solo
traduce peticiones HTTP a llamadas de esa clase y sus excepciones a códigos de
estado. Ninguna regla de priorización ni de negocio vive en `main.py`.

## 4. La prioridad no distingue paciente de vehículo

El criterio de orden de atención es `(nivel_prioridad, orden_llegada)`. Un
vehículo (ambulancia) y un paciente con el mismo nivel de triaje compiten en
pie de igualdad y gana el que llegó primero. El campo `tipo` es un dato
descriptivo para que el personal sepa cómo proceder al atender, no un criterio
de orden.

## 5. Toda entrada se valida en el borde

Un nivel de prioridad fuera de 1–5, un tipo que no sea `paciente` o `vehiculo`,
o un campo vacío se rechazan **antes** de entrar al CDA: con `ValueError` en el
núcleo y con `422` en la API (vía `Field`/`Literal` de Pydantic). El CDA nunca
queda en un estado a medio registrar.

## 6. Los casos límite se prueban por separado

Cola vacía, un solo elemento, empate de prioridad, y remoción de un nodo
intermedio del montículo tienen pruebas propias, igual que en la actividad de
listas. Cada prueba de remoción comprueba además que el montículo **siga
ordenado correctamente después** de la operación (se drena y se verifica que
sale en orden no decreciente de prioridad).

## 7. La bitácora de IA es honesta

`bitacora_ia.md` registra las interacciones reales con la IA durante este
trabajo: qué se pidió, qué decisiones se tomaron y por qué, sin inventar
contenido ni atribuir autoría del trabajo a la herramienta.

## 8. Reproducible en una máquina limpia

`python -m pytest` pasa sin configuración extra más allá de
`pip install -r requirements.txt`. `uvicorn main:app --reload` levanta la API
documentada en `spec.md` y `metodos_http.md`.
