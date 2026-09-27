from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    MenuCreate,
    MenuList,
    MenuPost,
    MenuPut,
    MenuRead,
    MenuUpdate,
)
from src.crud import menu_crud

menus_router = APIRouter(prefix="/menus", tags=["menus"])


@menus_router.get("/", response_model=MenuList)
def listar_menus():
    menus = menu_crud.listar_menus()
    if not menus:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="No se encontraron menus"
        )
    return {
        "data": menus,
        "status": HTTPStatus.OK.value,
        "message": "Menus encontrados",
    }


@menus_router.get("/{id_menu}", response_model=MenuRead)
def obtener_menu(id_menu: UUID):
    menu = menu_crud.buscar_menu(id_menu)
    if menu is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Menu no encontrado"
        )
    return menu


@menus_router.post("/", response_model=MenuPost, status_code=HTTPStatus.CREATED.value)
def crear_menu(datos: MenuCreate):
    menu = menu_crud.crear_menu(**datos.model_dump())
    return {
        "data": menu,
        "status": HTTPStatus.CREATED.value,
        "message": f"Menu {menu.nombre} creado",
    }


@menus_router.put("/{id_menu}", response_model=MenuPut)
def actualizar_menu(id_menu: UUID, datos: MenuUpdate):
    if menu_crud.buscar_menu(id_menu) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Menu no encontrado"
        )
    menu = menu_crud.actualizar_menu(
        id_menu,
        datos.id_usuario_edicion,
        **datos.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"}),
    )
    return {
        "data": menu,
        "status": HTTPStatus.OK.value,
        "message": f"Menu {menu.nombre} actualizado",
    }


@menus_router.delete("/{id_menu}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_menu(id_menu: UUID):
    if not menu_crud.eliminar_menu(id_menu):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Menu no encontrado"
        )
