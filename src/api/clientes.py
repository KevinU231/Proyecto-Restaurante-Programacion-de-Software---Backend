from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    ClienteCreate,
    ClienteList,
    ClientePost,
    ClientePut,
    ClienteRead,
    ClienteUpdate,
)
from src.crud import cliente_crud

clientes_router = APIRouter(prefix="/clientes", tags=["clientes"])


@clientes_router.get("/", response_model=ClienteList)
def listar_clientes():
    clientes = cliente_crud.listar_clientes()
    if not clientes:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron clientes"
        )
    return {
        "data": clientes,
        "status": HTTPStatus.OK.value,
        "message": "Clientes encontrados",
    }


@clientes_router.get("/{id_cliente}", response_model=ClienteRead)
def obtener_cliente(id_cliente: UUID):
    cliente = cliente_crud.buscar_cliente(id_cliente)
    if cliente is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Cliente no encontrado"
        )
    return cliente


@clientes_router.post("/", response_model=ClientePost, status_code=201)
def crear_cliente(datos: ClienteCreate):
    cliente = cliente_crud.crear_cliente(**datos.model_dump())
    return {
        "data": cliente,
        "status": HTTPStatus.CREATED.value,
        "message": f"Cliente {cliente.nombre} creado",
    }


@clientes_router.put("/{id_cliente}", response_model=ClientePut)
def actualizar_cliente(id_cliente: UUID, datos: ClienteUpdate):
    if cliente_crud.buscar_cliente(id_cliente) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Cliente no encontrado"
        )
    cliente = cliente_crud.actualizar_cliente(
        id_cliente,
        datos.id_usuario_edicion,
        **datos.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"}),
    )
    return {
        "data": cliente,
        "status": HTTPStatus.OK.value,
        "message": f"Cliente {cliente.nombre} actualizado",
    }


@clientes_router.delete("/{id_cliente}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_cliente(id_cliente: UUID):
    if not cliente_crud.eliminar_cliente(id_cliente):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Cliente no encontrado"
        )
