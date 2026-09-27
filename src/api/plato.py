from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    PlatoCreate,
    PlatoList,
    PlatoPost,
    PlatoPut,
    PlatoRead,
    PlatoUpdate,
)
from src.crud import plato_crud

platos_router = APIRouter(prefix="/platos", tags=["platos"])


@platos_router.get("/", response_model=PlatoList)
def listar_platos():
    platos = plato_crud.listar_platos()
    if not platos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron platos"
        )
    return {
        "data": platos,
        "status": HTTPStatus.OK.value,
        "message": "Platos encontrados",
    }


@platos_router.get("/{id_plato}", response_model=PlatoRead)
def obtener_plato(id_plato: UUID):
    plato = plato_crud.buscar_plato(id_plato)
    if plato is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Plato no encontrado"
        )
    return plato


@platos_router.post("/", response_model=PlatoPost, status_code=HTTPStatus.CREATED.value)
def crear_plato(datos: PlatoCreate):
    plato = plato_crud.crear_plato(**datos.model_dump())
    return {
        "data": plato,
        "status": HTTPStatus.CREATED.value,
        "message": f"Plato {plato.nombre} creado",
    }


@platos_router.put("/{id_plato}", response_model=PlatoPut)
def actualizar_plato(id_plato: UUID, datos: PlatoUpdate):
    if plato_crud.buscar_plato(id_plato) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Plato no encontrado"
        )
    plato = plato_crud.actualizar_plato(
        id_plato,
        datos.id_usuario_edicion,
        **datos.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"}),
    )
    return {
        "data": plato,
        "status": HTTPStatus.OK.value,
        "message": f"Plato {plato.nombre} actualizado",
    }


@platos_router.delete("/{id_plato}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_plato(id_plato: UUID):
    if not plato_crud.eliminar_plato(id_plato):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Plato no encontrado"
        )
