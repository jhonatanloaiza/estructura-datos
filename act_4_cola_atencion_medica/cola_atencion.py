"""CDA — Cola de Atención: TAD de cola de prioridad para un sistema de
atención médica (pacientes y vehículos).

El montículo binario (min-heap) se implementa a mano sobre un arreglo
(`list` de Python usada solo como bloque indexable): sin `heapq` ni ninguna
otra cola de prioridad de la librería estándar. Subir y bajar un elemento se
escriben con aritmética de índices explícita, igual que en la actividad
anterior se prohibió `list.insert`/`list.pop` para desplazar un arreglo.

Contrato completo: ver `spec.md`. Este módulo no sabe que existe HTTP
(`constitucion.md` §3): `main.py` es la única capa que conoce FastAPI.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

NIVELES_VALIDOS = {1, 2, 3, 4, 5}
TIPOS_VALIDOS = {"paciente", "vehiculo"}


class ColaAtencionError(Exception):
    """Base de los errores propios del CDA."""


class ColaVaciaError(ColaAtencionError):
    """Se pidió `siguiente()` o `atender()` con la cola vacía."""


class SolicitudNoEncontradaError(ColaAtencionError):
    """Se pidió `sacar(id)` con un id que no está en la cola."""


def _ahora() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Solicitud:
    id: int
    tipo: str                      # "paciente" | "vehiculo"
    nombre: str
    identificacion: str
    motivo: str
    nivel_prioridad: int           # 1 (más urgente) .. 5 (menos urgente)
    orden_llegada: int             # desempate: menor = llegó antes
    registrado_en: str = field(default_factory=_ahora)
    atendido: bool = False
    atendido_en: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tipo": self.tipo,
            "nombre": self.nombre,
            "identificacion": self.identificacion,
            "motivo": self.motivo,
            "nivel_prioridad": self.nivel_prioridad,
            "orden_llegada": self.orden_llegada,
            "registrado_en": self.registrado_en,
            "atendido": self.atendido,
            "atendido_en": self.atendido_en,
        }


class ColaAtencion:
    """Montículo binario de `Solicitud`, ordenado por
    `(nivel_prioridad, orden_llegada)` ascendente: la raíz es siempre la
    solicitud que debe atenderse primero.
    """

    def __init__(self):
        self._datos: list[Solicitud] = []
        self._indice: dict[int, int] = {}   # id -> posición en _datos
        self._siguiente_id = 1
        self._siguiente_orden = 0

    # -- consulta -----------------------------------------------------------

    def __len__(self):
        return len(self._datos)

    def esta_vacia(self) -> bool:
        return len(self._datos) == 0

    def siguiente(self) -> Solicitud:
        if self.esta_vacia():
            raise ColaVaciaError("la cola de atención está vacía")
        return self._datos[0]

    def listar_pendientes(self) -> list[Solicitud]:
        """Copia de las solicitudes pendientes, ordenadas por prioridad.

        No es simplemente `list(self._datos)`: el arreglo del montículo solo
        garantiza que la raíz es la mínima, no que esté totalmente ordenado.
        """
        return sorted(self._datos, key=self._clave)

    def cuantos_faltan(self) -> dict:
        por_tipo = {"paciente": 0, "vehiculo": 0}
        por_nivel = {n: 0 for n in sorted(NIVELES_VALIDOS)}
        for s in self._datos:
            por_tipo[s.tipo] += 1
            por_nivel[s.nivel_prioridad] += 1
        return {"total": len(self._datos), "por_tipo": por_tipo, "por_nivel": por_nivel}

    # -- modificación ---------------------------------------------------------

    def registrar(self, tipo: str, nombre: str, identificacion: str,
                   motivo: str, nivel_prioridad: int) -> Solicitud:
        if tipo not in TIPOS_VALIDOS:
            raise ValueError(f"tipo inválido: {tipo!r} (debe ser 'paciente' o 'vehiculo')")
        if nivel_prioridad not in NIVELES_VALIDOS:
            raise ValueError(f"nivel_prioridad inválido: {nivel_prioridad!r} (debe ser 1..5)")
        if not nombre.strip() or not identificacion.strip() or not motivo.strip():
            raise ValueError("nombre, identificación y motivo no pueden estar vacíos")

        solicitud = Solicitud(
            id=self._siguiente_id,
            tipo=tipo,
            nombre=nombre,
            identificacion=identificacion,
            motivo=motivo,
            nivel_prioridad=nivel_prioridad,
            orden_llegada=self._siguiente_orden,
        )
        self._siguiente_id += 1
        self._siguiente_orden += 1

        self._datos.append(solicitud)
        i = len(self._datos) - 1
        self._indice[solicitud.id] = i
        self._subir(i)
        return solicitud

    def atender(self) -> Solicitud:
        if self.esta_vacia():
            raise ColaVaciaError("la cola de atención está vacía")
        atendida = self._eliminar_en(0)
        atendida.atendido = True
        atendida.atendido_en = _ahora()
        return atendida

    def sacar(self, id: int) -> Solicitud:
        if id not in self._indice:
            raise SolicitudNoEncontradaError(f"no existe una solicitud pendiente con id={id}")
        i = self._indice[id]
        return self._eliminar_en(i)

    def posicion(self, id: int) -> int:
        """Posición (1 = siguiente a atender) de `id` entre los pendientes."""
        pendientes = self.listar_pendientes()
        for pos, s in enumerate(pendientes, start=1):
            if s.id == id:
                return pos
        raise SolicitudNoEncontradaError(f"no existe una solicitud pendiente con id={id}")

    # -- internos: montículo -------------------------------------------------

    @staticmethod
    def _clave(s: Solicitud):
        return (s.nivel_prioridad, s.orden_llegada)

    def _eliminar_en(self, i: int) -> Solicitud:
        """Quita el nodo en la posición `i` y restaura la propiedad de montículo."""
        n = len(self._datos)
        victima = self._datos[i]
        ultimo = n - 1

        if i == ultimo:
            self._datos.pop()
            del self._indice[victima.id]
            return victima

        self._mover(ultimo, i)       # el último ocupa el hueco de `i`
        self._datos.pop()
        del self._indice[victima.id]

        # el elemento que bajó a `i` puede necesitar subir o bajar
        if i < len(self._datos):
            padre = (i - 1) // 2
            if i > 0 and self._clave(self._datos[i]) < self._clave(self._datos[padre]):
                self._subir(i)
            else:
                self._bajar(i)
        return victima

    def _mover(self, origen: int, destino: int):
        self._datos[destino] = self._datos[origen]
        self._indice[self._datos[destino].id] = destino

    def _intercambiar(self, i: int, j: int):
        self._datos[i], self._datos[j] = self._datos[j], self._datos[i]
        self._indice[self._datos[i].id] = i
        self._indice[self._datos[j].id] = j

    def _subir(self, i: int):
        while i > 0:
            padre = (i - 1) // 2
            if self._clave(self._datos[i]) < self._clave(self._datos[padre]):
                self._intercambiar(i, padre)
                i = padre
            else:
                break

    def _bajar(self, i: int):
        n = len(self._datos)
        while True:
            izq, der = 2 * i + 1, 2 * i + 2
            menor = i
            if izq < n and self._clave(self._datos[izq]) < self._clave(self._datos[menor]):
                menor = izq
            if der < n and self._clave(self._datos[der]) < self._clave(self._datos[menor]):
                menor = der
            if menor == i:
                break
            self._intercambiar(i, menor)
            i = menor
