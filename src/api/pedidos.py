from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    PedidoCreate,
    PedidoList,
    PedidoPost,
    PedidoPut,
    PedidoRead,
    PedidoUpdate,
)
from src.crud.Pedido_crud import PedidoCRUD
from src.database.connection import get_session

pedidos_router = APIRouter(prefix="/pedidos", tags=["pedidos"])


def obtener_crud() -> PedidoCRUD:
    db = get_session()
    return PedidoCRUD(db)


@pedidos_router.get("/", response_model=PedidoList)
def listar_pedidos():
    crud = obtener_crud()
    pedidos = crud.listar()

    if not pedidos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron pedidos",
        )

    return {
        "data": pedidos,
        "status": HTTPStatus.OK.value,
        "message": "Pedidos encontrados",
    }


@pedidos_router.get("/{id_pedido}", response_model=PedidoRead)
def obtener_pedido(id_pedido: UUID):
    crud = obtener_crud()
    pedido = crud.obtener(id_pedido)

    if pedido is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Pedido no encontrado",
        )

    return pedido


@pedidos_router.post(
    "/",
    response_model=PedidoPost,
    status_code=HTTPStatus.CREATED.value,
)
def crear_pedido(datos: PedidoCreate):
    crud = obtener_crud()

    pedido = crud.crear(**datos.model_dump())

    return {
        "data": pedido,
        "status": HTTPStatus.CREATED.value,
        "message": f"Pedido {pedido.id_pedido} creado",
    }


@pedidos_router.put("/{id_pedido}", response_model=PedidoPut)
def actualizar_pedido(id_pedido: UUID, datos: PedidoUpdate):
    crud = obtener_crud()

    if crud.obtener(id_pedido) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Pedido no encontrado",
        )

    pedido = crud.actualizar(
        id_pedido,
        datos.id_usuario_edicion,
        **datos.model_dump(
            exclude_unset=True,
            exclude={"id_usuario_edicion"},
        ),
    )

    return {
        "data": pedido,
        "status": HTTPStatus.OK.value,
        "message": f"Pedido {pedido.id_pedido} actualizado",
    }


@pedidos_router.delete(
    "/{id_pedido}",
    status_code=HTTPStatus.NO_CONTENT.value,
)
def eliminar_pedido(id_pedido: UUID):
    crud = obtener_crud()

    if not crud.eliminar(id_pedido):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Pedido no encontrado",
        )
