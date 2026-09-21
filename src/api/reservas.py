from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    ReservaCreate,
    ReservaList,
    ReservaPost,
    ReservaPut,
    ReservaRead,
    ReservaUpdate,
)
from src.crud import reserva_crud

reservas_router = APIRouter(prefix="/reservas", tags=["reservas"])


@reservas_router.get("/", response_model=ReservaList)
def listar_reservas():
    reservas = reserva_crud.listar_reservas()
    if not reservas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron reservas"
        )
    return {
        "data": reservas,
        "status": HTTPStatus.OK.value,
        "message": "Reservas encontradas",
    }


@reservas_router.get("/{id_reserva}", response_model=ReservaRead)
def obtener_reserva(id_reserva: UUID):
    reserva = reserva_crud.buscar_reserva(id_reserva)
    if reserva is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Reserva no encontrada"
        )
    return reserva


@reservas_router.post("/", response_model=ReservaPost, status_code=201)
def crear_reserva(datos: ReservaCreate):
    reserva = reserva_crud.crear_reserva(**datos.model_dump())
    return {
        "data": reserva,
        "status": HTTPStatus.CREATED.value,
        "message": "Reserva creada",
    }


@reservas_router.put("/{id_reserva}", response_model=ReservaPut)
def actualizar_reserva(id_reserva: UUID, datos: ReservaUpdate):
    if reserva_crud.buscar_reserva(id_reserva) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Reserva no encontrada"
        )
    reserva = reserva_crud.actualizar_reserva(
        id_reserva,
        datos.id_usuario_edicion,
        **datos.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"})
    )
    return {
        "data": reserva,
        "status": HTTPStatus.OK.value,
        "message": "Reserva actualizada",
    }


@reservas_router.delete("/{id_reserva}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_reserva(id_reserva: UUID):
    if not reserva_crud.eliminar_reserva(id_reserva):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Reserva no encontrada"
        )
