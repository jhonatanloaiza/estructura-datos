# CDA de atención médica

Cola de prioridad (montículo binario, implementado a mano) para un sistema de
atención médica que registra pacientes y vehículos (ambulancias), expuesta
como API con FastAPI. Documentación completa en [`spec.md`](spec.md); el
razonamiento de diseño en [`plan.md`](plan.md) y [`constitucion.md`](constitucion.md).

## Instalar

```bash
pip install -r requirements.txt
```

## Correr la API

```bash
uvicorn main:app --reload
```

Documentación interactiva en `http://127.0.0.1:8000/docs`.

## Correr las pruebas

```bash
python -m pytest -v
```

42 pruebas: `test_cola_atencion.py` prueba el núcleo sin HTTP (incluidos los
casos límite de `spec.md` §7) y `test_api.py` prueba la API con `TestClient`.

## Endpoints

Ver la tabla completa y el razonamiento de cada método HTTP en
[`metodos_http.md`](metodos_http.md).

| Método | Ruta | Qué hace |
|---|---|---|
| `POST` | `/registrar` | Registra un paciente o vehículo con su nivel de prioridad (1–5) |
| `GET` | `/siguiente` | Consulta quién sigue, sin sacarlo de la cola |
| `POST` | `/atender` | Atiende (retira) al siguiente |
| `DELETE` | `/cola/{id}` | Saca una solicitud puntual sin atenderla |
| `GET` | `/estado` | Cuántos faltan: total, por tipo, por nivel |
| `GET` | `/cola` | Lista las solicitudes pendientes en orden de prioridad |

## Ejemplo rápido

```bash
curl -X POST http://127.0.0.1:8000/registrar -H "Content-Type: application/json" \
  -d '{"tipo":"paciente","nombre":"Ana","identificacion":"CC123","motivo":"dolor torácico","nivel_prioridad":1}'

curl http://127.0.0.1:8000/siguiente
curl -X POST http://127.0.0.1:8000/atender
curl http://127.0.0.1:8000/estado
```
