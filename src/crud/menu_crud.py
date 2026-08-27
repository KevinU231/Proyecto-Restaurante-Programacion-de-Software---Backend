import uuid
from typing import Optional
from src.entities.menu import Menu

menus: list[Menu] = []


def crear_menu(
    nombre: str,
    ids_platos: list[uuid.UUID],
    id_usuario_creacion: uuid.UUID,
    descripcion: str = "",
) -> Menu:
    nuevo = Menu(nombre, ids_platos, id_usuario_creacion, descripcion)
    menus.append(nuevo)
    return nuevo


def listar_menus() -> list[Menu]:
    return menus


def buscar_menu(id_menu: uuid.UUID) -> Optional[Menu]:
    for menu in menus:
        if menu.id_menu == id_menu:
            return menu
    return None


def actualizar_menu(
    id_menu: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    nombre: Optional[str] = None,
    ids_platos: Optional[list[uuid.UUID]] = None,
    descripcion: Optional[str] = None,
) -> Optional[Menu]:
    menu = buscar_menu(id_menu)
    if menu is None:
        return None
    if nombre:
        menu.nombre = nombre
    if ids_platos is not None:
        menu.ids_platos = ids_platos
    if descripcion:
        menu.descripcion = descripcion
    menu.marcar_editado(id_usuario_edicion)
    return menu


def eliminar_menu(id_menu: uuid.UUID) -> bool:
    menu = buscar_menu(id_menu)
    if menu is None:
        return False
    menus.remove(menu)
    return True