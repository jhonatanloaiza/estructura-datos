from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Datos(BaseModel):
    nombre: str
    telefono: str
    edad : int
    correo : str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}/{q}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/consulta/{nombre}")
def consulta(nombre: str):
    return {"nombre": nombre}

@app.post("/guardar")
def guardar(datos: Datos):
    return {"nombre": datos.nombre, "telefono": datos.telefono, "edad":datos.edad, "correo":datos.correo}
