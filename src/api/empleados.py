from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    EmpleadoCreate,
    EmpleadoList,
    EmpleadoPost,
    EmpleadoPut,
    EmpleadoRead,
    EmpleadoUpdate,
)
from src.crud.empleado_crud import EmpleadoCRUD
from src.database.connection import get_session


def obtener_crud() -> EmpleadoCRUD:
    db = get_session()
    return EmpleadoCRUD(db)


empleados_router = APIRouter(prefix="/empleados", tags=["empleados"])


@empleados_router.get("/", response_model=EmpleadoList)
def listar_empleados():
    crud = obtener_crud()
    empleados = crud.listar()

    if not empleados:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron empleados",
        )

    return {
        "data": empleados,
        "status": HTTPStatus.OK.value,
        "message": "Empleados encontrados",
    }


@empleados_router.get("/{id_empleado}", response_model=EmpleadoRead)
def obtener_empleado(id_empleado: UUID):
    crud = obtener_crud()
    empleado = crud.obtener(id_empleado)

    if empleado is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Empleado no encontrado"
        )

    return empleado


@empleados_router.post(
    "/", response_model=EmpleadoPost, status_code=HTTPStatus.CREATED.value
)
def crear_empleado(datos: EmpleadoCreate):
    crud = obtener_crud()
    empleado = crud.crear(**datos.model_dump())

    return {
        "data": empleado,
        "status": HTTPStatus.CREATED.value,
        "message": f"Empleado {empleado.nombre} creado",
    }


@empleados_router.put("/{id_empleado}", response_model=EmpleadoPut)
def actualizar_empleado(id_empleado: UUID, datos: EmpleadoUpdate):
    crud = obtener_crud()
    if crud.obtener(id_empleado) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Empleado no encontrado"
        )

    empleado = crud.actualizar(id_empleado, **datos.model_dump())

    return {
        "data": empleado,
        "status": HTTPStatus.OK.value,
        "message": f"Empleado {empleado.nombre} actualizado",
    }


@empleados_router.delete("" "/{id_empleado}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_empleado(id_empleado: UUID):
    crud = obtener_crud()
    if not crud.eliminar(id_empleado):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Empleado no encontrado"
        )
