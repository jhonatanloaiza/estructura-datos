# Plan técnico

Cómo se cumple `spec.md` respetando `constitucion.md`.

## 1. Estructura del repositorio

```
cola_atencion.py        el CDA: montículo binario a mano (Solicitud, ColaAtencion, errores)
main.py                 API FastAPI: capa delgada sobre ColaAtencion
test_cola_atencion.py   pruebas del núcleo (casos límite incluidos)
test_api.py             pruebas de la API con TestClient
metodos_http.md         investigación de métodos HTTP y su mapeo a los endpoints
bitacora_ia.md          registro de interacción con la IA
requirements.txt        dependencias (fastapi, uvicorn, pytest, httpx)
README.md               cómo correr la API y las pruebas
constitucion.md spec.md plan.md task.md   documentos SDD
```

## 2. Diseño del CDA (`cola_atencion.py`)

### `Solicitud` (dataclass)
Campos: `id`, `tipo` (`"paciente"` | `"vehiculo"`), `nombre`, `identificacion`,
`motivo`, `nivel_prioridad` (1–5), `orden_llegada`, `registrado_en`
(timestamp ISO), `atendido` (`bool`), `atendido_en` (timestamp o `None`).

### `ColaAtencion`
- Almacenamiento: `self._datos` (lista usada como arreglo del montículo) +
  `self._indice` (dict `id -> posición`, para que `sacar(id)` ubique el nodo
  en O(1) y solo el restablecimiento del montículo sea O(log n)).
- Comparación: `_clave(s) = (s.nivel_prioridad, s.orden_llegada)`, menor es
  más urgente (min-heap).
- `registrar(tipo, nombre, identificacion, motivo, nivel_prioridad)`: valida,
  crea `Solicitud`, `_subir` desde el final. O(log n).
- `siguiente()`: `self._datos[0]` sin modificar. O(1). Lanza `ColaVaciaError`
  si está vacía.
- `atender()`: guarda la raíz, mueve el último elemento a la raíz, `_bajar`.
  O(log n). Marca `atendido=True`.
- `sacar(id)`: ubica el índice con `self._indice`, lo reemplaza por el último
  elemento y decide `_subir` o `_bajar` según corresponda. O(log n) una vez
  ubicado.
- `cuantos_faltan()`: recorre `self._datos` una vez (O(n)) y arma el desglose
  por tipo y por nivel; no requiere que el montículo esté ordenado porque solo
  cuenta, no compara.
- `esta_vacia()`, `listar_pendientes()` (orden de prioridad, para mostrar en
  pantalla, no solo contar).
- `_subir(i)` / `_bajar(i)`: aritmética de índices (`(i-1)//2`, `2*i+1`,
  `2*i+2`), sin `heapq`.

### Errores
`ColaVaciaError` (consultar/atender con la cola vacía) y
`SolicitudNoEncontradaError` (`sacar` con un id que no existe): ambas
subclases de una `ColaAtencionError` base, para que `main.py` las traduzca a
HTTP sin conocer los detalles del núcleo.

## 3. Diseño de la API (`main.py`)

Mismo estilo que el fragmento de referencia: `app = FastAPI()`, un modelo
`BaseModel` para la entrada, funciones decoradas que devuelven diccionarios
directamente (sin capa de repositorio ni routers separados, porque el
proyecto es de un solo recurso).

| Método | Ruta | Acción | Historia |
|---|---|---|---|
| `GET` | `/` | información del servicio | — |
| `POST` | `/registrar` | registrar paciente o vehículo | HU1 |
| `GET` | `/siguiente` | consultar el próximo a atender | HU2 |
| `POST` | `/atender` | atender y retirar al próximo | HU3 |
| `DELETE` | `/cola/{id}` | sacar una solicitud puntual | HU4 |
| `GET` | `/estado` | cuántos faltan (total, por tipo, por nivel) | HU5 |
| `GET` | `/cola` | listar las solicitudes pendientes en orden | (extra, apoya HU5) |

Las excepciones del núcleo se capturan en cada endpoint y se traducen:
`ColaVaciaError` / `SolicitudNoEncontradaError` → `HTTPException(404, …)`;
errores de validación de Pydantic (`Literal`, `Field(ge=1, le=5)`) → `422`
automático de FastAPI.

## 4. Estrategia de pruebas

- **Núcleo (`test_cola_atencion.py`):** registrar/consultar/atender/sacar en
  escenarios normales, más los cuatro casos límite de `spec.md` §7, más una
  prueba de «drenado»: insertar N solicitudes con niveles y órdenes mezclados,
  sacar algunas al azar, atender todas las restantes y comprobar que la
  secuencia resultante es no decreciente en `(nivel_prioridad, orden_llegada)`.
- **API (`test_api.py`):** con `TestClient`, un flujo feliz completo (registrar
  dos o tres solicitudes, consultar siguiente, atender, sacar, ver estado) y
  los errores (`404` en cola vacía o id inexistente, `422` en datos inválidos).

## 5. Riesgos

| Riesgo | Mitigación |
|---|---|
| `sacar` en un nodo intermedio rompe el orden del montículo | Prueba de drenado tras remociones aleatorias (§4) |
| Confundir «atender» con «sacar» en la API | Historias separadas (HU3 vs HU4) con criterios de aceptación distintos |
| Mezclar lógica de negocio en `main.py` | Constitución §3: el núcleo no conoce HTTP, se prueba aparte |
