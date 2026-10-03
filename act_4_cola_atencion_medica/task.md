# Tareas

Orden de ejecución. `[x]` = hecha y verificada.

## Fase 0 — Especificación
- [x] T0.1 Redactar `constitucion.md`.
- [x] T0.2 Redactar `spec.md`: sistema de atención, reglas de priorización,
      historias de usuario con criterios de aceptación, RF, RNF, casos límite.
- [x] T0.3 Redactar `plan.md`.

## Fase 1 — Investigación de métodos HTTP
- [x] T1.1 `metodos_http.md`: qué hace cada método (GET, POST, PUT, PATCH,
      DELETE), seguridad/idempotencia, y por qué se eligió cada uno para cada
      endpoint del CDA.

## Fase 2 — Núcleo del CDA
- [x] T2.1 `cola_atencion.py`: `Solicitud`, `ColaAtencion`, montículo a mano
      (`_subir`/`_bajar`), sin `heapq`.
- [x] T2.2 `registrar`, `siguiente`, `atender`, `sacar`, `cuantos_faltan`,
      `listar_pendientes`.
- [x] T2.3 `test_cola_atencion.py`: casos normales + los 4 límite de `spec.md`
      §7 + prueba de drenado tras remociones aleatorias.

## Fase 3 — API
- [x] T3.1 `main.py`: endpoints de la tabla de `plan.md` §3, estilo del
      fragmento de referencia (FastAPI + Pydantic, funciones simples).
- [x] T3.2 Traducir errores del núcleo a códigos HTTP (404/422).
- [x] T3.3 `test_api.py` con `TestClient`: flujo feliz + errores.

## Fase 4 — Entrega
- [x] T4.1 `requirements.txt` y `README.md` (cómo correr API y pruebas).
- [x] T4.2 `python -m pytest` en verde.
- [x] T4.3 `bitacora_ia.md` con el registro real de la interacción.
- [ ] T4.4 Confirmar número/nombre de la actividad y fecha de entrega con la
      guía del curso (no se incluyó una captura de la plataforma para esta
      actividad, a diferencia de la anterior).
- [ ] T4.5 Commit y push al repositorio.
