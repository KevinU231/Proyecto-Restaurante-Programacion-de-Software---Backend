import uuid
from typing import Optional

from sqlalchemy.orm import selectinload

from src.database.connection import get_session
from src.entities.menu import Menu
from src.entities.plato import Plato


def crear_menu(
    nombre: str,
    ids_platos: list[uuid.UUID],
    id_usuario_creacion: uuid.UUID,
    descripcion: str = "",
) -> Menu:
    session = get_session()
    try:
        nuevo = Menu(
            nombre=nombre,
            descripcion=descripcion,
            id_usuario_creacion=id_usuario_creacion,
        )
        if ids_platos:
            platos = (
                session.query(Plato)
                .filter(Plato.id_plato.in_(ids_platos))
                .all()
            )
            nuevo.platos = platos
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        _ = nuevo.platos
        return nuevo
    finally:
        session.close()


def listar_menus() -> list[Menu]:
    session = get_session()
    try:
        return (
            session.query(Menu)
            .options(selectinload(Menu.platos))
            .all()
        )
    finally:
        session.close()


def buscar_menu(id_menu: uuid.UUID) -> Optional[Menu]:
    session = get_session()
    try:
        return (
            session.query(Menu)
            .options(selectinload(Menu.platos))
            .filter_by(id_menu=id_menu)
            .first()
        )
    finally:
        session.close()


def actualizar_menu(
    id_menu: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    nombre: Optional[str] = None,
    ids_platos: Optional[list[uuid.UUID]] = None,
    descripcion: Optional[str] = None,
) -> Optional[Menu]:
    session = get_session()
    try:
        menu = session.query(Menu).filter_by(id_menu=id_menu).first()
        if menu is None:
            return None
        if nombre:
            menu.nombre = nombre
        if ids_platos is not None:
            platos = (
                session.query(Plato)
                .filter(Plato.id_plato.in_(ids_platos))
                .all()
            )
            menu.platos = platos
        if descripcion:
            menu.descripcion = descripcion
        menu.marcar_editado(id_usuario_edicion)
        session.commit()
        session.refresh(menu)
        _ = menu.platos
        return menu
    finally:
        session.close()


def eliminar_menu(id_menu: uuid.UUID) -> bool:
    session = get_session()
    try:
        menu = session.query(Menu).filter_by(id_menu=id_menu).first()
        if menu is None:
            return False
        session.delete(menu)
        session.commit()
        return True
    finally:
        session.close()
