"""API del CDA de atención médica.

Capa delgada sobre `cola_atencion.ColaAtencion`: aquí solo se traducen
peticiones HTTP a llamadas del núcleo y sus errores a códigos de estado
(`constitucion.md` §3). Ninguna regla de priorización vive en este archivo.

Correr:  uvicorn main:app --reload
Docs:    http://127.0.0.1:8000/docs
"""

from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from cola_atencion import ColaAtencion, ColaVaciaError, SolicitudNoEncontradaError

app = FastAPI(title="CDA — Atención médica")

cola = ColaAtencion()


class RegistroEntrada(BaseModel):
    tipo: Literal["paciente", "vehiculo"]
    nombre: str = Field(min_length=1)
    identificacion: str = Field(min_length=1)
    motivo: str = Field(min_length=1)
    nivel_prioridad: int = Field(ge=1, le=5)


@app.get("/")
def read_root():
    return {"servicio": "CDA de atención médica", "endpoints": [
        "POST /registrar", "GET /siguiente", "POST /atender",
        "DELETE /cola/{id}", "GET /estado", "GET /cola",
    ]}


@app.post("/registrar", status_code=201)
def registrar(datos: RegistroEntrada):
    solicitud = cola.registrar(
        tipo=datos.tipo,
        nombre=datos.nombre,
        identificacion=datos.identificacion,
        motivo=datos.motivo,
        nivel_prioridad=datos.nivel_prioridad,
    )
    return {
        "solicitud": solicitud.to_dict(),
        "posicion_en_cola": cola.posicion(solicitud.id),
    }


@app.get("/siguiente")
def siguiente():
    try:
        return cola.siguiente().to_dict()
    except ColaVaciaError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/atender")
def atender():
    try:
        return cola.atender().to_dict()
    except ColaVaciaError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/cola/{id}")
def sacar(id: int):
    try:
        return cola.sacar(id).to_dict()
    except SolicitudNoEncontradaError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/estado")
def estado():
    return cola.cuantos_faltan()


@app.get("/cola")
def listar():
    return {"pendientes": [s.to_dict() for s in cola.listar_pendientes()]}
