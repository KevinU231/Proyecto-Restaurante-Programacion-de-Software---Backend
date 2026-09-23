from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    DetallePedidoCreate,
    DetallePedidoList,
    DetallePedidoPost,
    DetallePedidoPut,
    DetallePedidoRead,
    DetallePedidoUpdate,
)
from src.crud.Detalle_Pedido_crud import DetallePedidoCRUD
from src.database.connection import get_session

detalles_pedido_router = APIRouter(
    prefix="/detalles-pedido",
    tags=["detalles-pedido"],
)


def obtener_crud() -> DetallePedidoCRUD:
    db = get_session()
    return DetallePedidoCRUD(db)


@detalles_pedido_router.get(
    "/",
    response_model=DetallePedidoList,
)
def listar_detalles():
    crud = obtener_crud()
    detalles = crud.listar()

    if not detalles:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron detalles de pedido",
        )

    return {
        "data": detalles,
        "status": HTTPStatus.OK.value,
        "message": "Detalles de pedido encontrados",
    }


@detalles_pedido_router.get(
    "/pedido/{id_pedido}",
    response_model=DetallePedidoList,
)
def listar_detalles_por_pedido(id_pedido: UUID):
    crud = obtener_crud()
    detalles = crud.listar_por_pedido(id_pedido)

    if not detalles:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron detalles para este pedido",
        )

    return {
        "data": detalles,
        "status": HTTPStatus.OK.value,
        "message": "Detalles del pedido encontrados",
    }


@detalles_pedido_router.get(
    "/{id_detalle_pedido}",
    response_model=DetallePedidoRead,
)
def obtener_detalle(id_detalle_pedido: UUID):
    crud = obtener_crud()
    detalle = crud.obtener(id_detalle_pedido)

    if detalle is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Detalle de pedido no encontrado",
        )

    return detalle


@detalles_pedido_router.post(
    "/",
    response_model=DetallePedidoPost,
    status_code=HTTPStatus.CREATED.value,
)
def crear_detalle(datos: DetallePedidoCreate):
    crud = obtener_crud()

    detalle = crud.crear(**datos.model_dump())

    return {
        "data": detalle,
        "status": HTTPStatus.CREATED.value,
        "message": f"Detalle {detalle.id_detalle_pedido} creado",
    }


@detalles_pedido_router.put(
    "/{id_detalle_pedido}",
    response_model=DetallePedidoPut,
)
def actualizar_detalle(
    id_detalle_pedido: UUID,
    datos: DetallePedidoUpdate,
):
    crud = obtener_crud()

    if crud.obtener(id_detalle_pedido) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Detalle de pedido no encontrado",
        )

    detalle = crud.actualizar(
        id_detalle_pedido,
        datos.id_usuario_edicion,
        **datos.model_dump(
            exclude_unset=True,
            exclude={"id_usuario_edicion"},
        ),
    )

    return {
        "data": detalle,
        "status": HTTPStatus.OK.value,
        "message": f"Detalle {detalle.id_detalle_pedido} actualizado",
    }


@detalles_pedido_router.delete(
    "/{id_detalle_pedido}",
    status_code=HTTPStatus.NO_CONTENT.value,
)
def eliminar_detalle(id_detalle_pedido: UUID):
    crud = obtener_crud()

    if not crud.eliminar(id_detalle_pedido):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Detalle de pedido no encontrado",
        )
