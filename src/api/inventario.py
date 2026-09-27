from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    InventarioCreate,
    InventarioList,
    InventarioPost,
    InventarioPut,
    InventarioRead,
    InventarioUpdate,
)
from src.crud import inventario_crud

inventario_router = APIRouter(prefix="/inventario", tags=["inventario"])


@inventario_router.get("/", response_model=InventarioList)
def listar_inventario():
    insumos = inventario_crud.listar_inventarios()
    if not insumos:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron insumos"
        )
    return {
        "data": insumos,
        "status": HTTPStatus.OK.value,
        "message": "Insumos encontrados",
    }


@inventario_router.get("/{id_insumo}", response_model=InventarioRead)
def obtener_insumo(id_insumo: UUID):
    insumo = inventario_crud.buscar_inventario(id_insumo)
    if insumo is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Insumo no encontrado"
        )
    return insumo


@inventario_router.post(
    "/", response_model=InventarioPost, status_code=HTTPStatus.CREATED.value
)
def crear_insumo(datos: InventarioCreate):
    insumo = inventario_crud.crear_inventario(**datos.model_dump())
    return {
        "data": insumo,
        "status": HTTPStatus.CREATED.value,
        "message": f"Insumo {insumo.nombre_insumo} creado",
    }


@inventario_router.put("/{id_insumo}", response_model=InventarioPut)
def actualizar_insumo(id_insumo: UUID, datos: InventarioUpdate):
    if inventario_crud.buscar_inventario(id_insumo) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Insumo no encontrado"
        )
    insumo = inventario_crud.actualizar_inventario(
        id_insumo,
        datos.id_usuario_edicion,
        **datos.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"}),
    )
    return {
        "data": insumo,
        "status": HTTPStatus.OK.value,
        "message": f"Insumo {insumo.nombre_insumo} actualizado",
    }


@inventario_router.delete("/{id_insumo}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_insumo(id_insumo: UUID):
    if not inventario_crud.eliminar_inventario(id_insumo):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Insumo no encontrado"
        )
