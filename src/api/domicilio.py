from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    DomicilioCreate,
    DomicilioList,
    DomicilioPost,
    DomicilioPut,
    DomicilioRead,
    DomicilioUpdate,
)
from src.crud import domicilio_crud

domicilios_router = APIRouter(prefix="/domicilios", tags=["domicilios"])


@domicilios_router.get("/", response_model=DomicilioList)
def listar_domicilios():
    domicilios = domicilio_crud.listar_domicilios()
    if not domicilios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron domicilios",
        )
    return {
        "data": domicilios,
        "status": HTTPStatus.OK.value,
        "message": "Domicilios encontrados",
    }


@domicilios_router.get("/{id_domicilio}", response_model=DomicilioRead)
def obtener_domicilio(id_domicilio: UUID):
    domicilio = domicilio_crud.buscar_domicilio(id_domicilio)
    if domicilio is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Domicilio no encontrado"
        )
    return domicilio


@domicilios_router.post(
    "/", response_model=DomicilioPost, status_code=HTTPStatus.CREATED.value
)
def crear_domicilio(datos: DomicilioCreate):
    domicilio = domicilio_crud.crear_domicilio(**datos.model_dump())
    return {
        "data": domicilio,
        "status": HTTPStatus.CREATED.value,
        "message": "Domicilio creado",
    }


@domicilios_router.put("/{id_domicilio}", response_model=DomicilioPut)
def actualizar_domicilio(id_domicilio: UUID, datos: DomicilioUpdate):
    if domicilio_crud.buscar_domicilio(id_domicilio) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Domicilio no encontrado"
        )
    domicilio = domicilio_crud.actualizar_domicilio(
        id_domicilio,
        datos.id_usuario_edicion,
        **datos.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"}),
    )
    return {
        "data": domicilio,
        "status": HTTPStatus.OK.value,
        "message": "Domicilio actualizado",
    }


@domicilios_router.delete("/{id_domicilio}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_domicilio(id_domicilio: UUID):
    if not domicilio_crud.eliminar_domicilio(id_domicilio):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Domicilio no encontrado"
        )
