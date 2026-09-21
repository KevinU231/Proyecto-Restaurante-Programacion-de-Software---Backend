from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    MesaCreate,
    MesaList,
    MesaPost,
    MesaPut,
    MesaRead,
    MesaUpdate,
)
from src.crud import mesa_crud

mesas_router = APIRouter(prefix="/mesas", tags=["mesas"])


@mesas_router.get("/", response_model=MesaList)
def listar_mesas():
    mesas = mesa_crud.listar_mesas()
    if not mesas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron mesas"
        )
    return {
        "data": mesas,
        "status": HTTPStatus.OK.value,
        "message": "Mesas encontradas",
    }


@mesas_router.get("/{id_mesa}", response_model=MesaRead)
def obtener_mesa(id_mesa: UUID):
    mesa = mesa_crud.buscar_mesa(id_mesa)
    if mesa is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Mesa no encontrada"
        )
    return mesa


@mesas_router.post("/", response_model=MesaPost, status_code=201)
def crear_mesa(datos: MesaCreate):
    mesa = mesa_crud.crear_mesa(**datos.model_dump())
    return {
        "data": mesa,
        "status": HTTPStatus.CREATED.value,
        "message": f"Mesa {mesa.numero} creada",
    }


@mesas_router.put("/{id_mesa}", response_model=MesaPut)
def actualizar_mesa(id_mesa: UUID, datos: MesaUpdate):
    if mesa_crud.buscar_mesa(id_mesa) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Mesa no encontrada"
        )
    mesa = mesa_crud.actualizar_mesa(
        id_mesa,
        datos.id_usuario_edicion,
        **datos.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"}),
    )
    return {
        "data": mesa,
        "status": HTTPStatus.OK.value,
        "message": f"Mesa {mesa.numero} actualizada",
    }


@mesas_router.delete("/{id_mesa}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_mesa(id_mesa: UUID):
    if not mesa_crud.eliminar_mesa(id_mesa):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Mesa no encontrada"
        )
