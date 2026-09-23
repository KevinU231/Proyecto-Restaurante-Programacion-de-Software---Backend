from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException


from src.api.schemas import (
    FacturaCreate,
    FacturaList,
    FacturaPost,
    FacturaPut,
    FacturaRead,
    FacturaUpdate,
)
from src.crud.Factura_crud import FacturaCRUD
from src.database.connection import get_session

facturas_router = APIRouter(
    prefix="/facturas",
    tags=["facturas"],
)


def obtener_crud() -> FacturaCRUD:
    db = get_session()
    return FacturaCRUD(db)


@facturas_router.get("/", response_model=FacturaList)
def listar_facturas():
    crud = obtener_crud()
    facturas = crud.listar()

    if not facturas:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron facturas",
        )

    return {
        "data": facturas,
        "status": HTTPStatus.OK.value,
        "message": "Facturas encontradas",
    }


@facturas_router.get(
    "/pedido/{id_pedido}",
    response_model=FacturaRead,
)
def obtener_factura_por_pedido(id_pedido: UUID):
    crud = obtener_crud()
    factura = crud.obtener_por_pedido(id_pedido)

    if factura is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontró una factura para este pedido",
        )

    return factura


@facturas_router.get(
    "/{id_factura}",
    response_model=FacturaRead,
)
def obtener_factura(id_factura: UUID):
    crud = obtener_crud()
    factura = crud.obtener(id_factura)

    if factura is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Factura no encontrada",
        )

    return factura


@facturas_router.post(
    "/",
    response_model=FacturaPost,
    status_code=HTTPStatus.CREATED.value,
)
def crear_factura(datos: FacturaCreate):
    crud = obtener_crud()
    factura = crud.crear(**datos.model_dump())

    return {
        "data": factura,
        "status": HTTPStatus.CREATED.value,
        "message": f"Factura {factura.id_factura} creada",
    }


@facturas_router.put(
    "/{id_factura}",
    response_model=FacturaPut,
)
def actualizar_factura(
    id_factura: UUID,
    datos: FacturaUpdate,
):
    crud = obtener_crud()

    if crud.obtener(id_factura) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Factura no encontrada",
        )

    factura = crud.actualizar(
        id_factura,
        datos.id_usuario_edicion,
        **datos.model_dump(
            exclude_unset=True,
            exclude={"id_usuario_edicion"},
        ),
    )

    return {
        "data": factura,
        "status": HTTPStatus.OK.value,
        "message": f"Factura {factura.id_factura} actualizada",
    }


@facturas_router.delete(
    "/{id_factura}",
    status_code=HTTPStatus.NO_CONTENT.value,
)
def eliminar_factura(id_factura: UUID):
    crud = obtener_crud()

    if not crud.eliminar(id_factura):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Factura no encontrada",
        )
