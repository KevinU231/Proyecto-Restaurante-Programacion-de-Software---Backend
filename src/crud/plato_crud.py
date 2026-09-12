import uuid
from typing import Optional

from sqlalchemy.orm import selectinload

from src.database.connection import get_session
from src.entities.plato import Plato
from src.entities.inventario import Inventario


def crear_plato(
    nombre: str,
    precio: float,
    descripcion: str,
    ids_insumos: list[uuid.UUID],
    id_usuario_creacion: uuid.UUID,
) -> Plato:
    session = get_session()
    try:
        nuevo = Plato(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            id_usuario_creacion=id_usuario_creacion,
        )
        if ids_insumos:
            insumos = (
                session.query(Inventario)
                .filter(Inventario.id_insumo.in_(ids_insumos))
                .all()
            )
            nuevo.insumos = insumos
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        _ = nuevo.insumos  # fuerza la carga de la relacion antes de cerrar sesion
        return nuevo
    finally:
        session.close()


def listar_platos() -> list[Plato]:
    session = get_session()
    try:
        return (
            session.query(Plato)
            .options(selectinload(Plato.insumos))
            .all()
        )
    finally:
        session.close()


def buscar_plato(id_plato: uuid.UUID) -> Optional[Plato]:
    session = get_session()
    try:
        return (
            session.query(Plato)
            .options(selectinload(Plato.insumos))
            .filter_by(id_plato=id_plato)
            .first()
        )
    finally:
        session.close()


def actualizar_plato(
    id_plato: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    nombre: Optional[str] = None,
    precio: Optional[float] = None,
    descripcion: Optional[str] = None,
    ids_insumos: Optional[list[uuid.UUID]] = None,
) -> Optional[Plato]:
    session = get_session()
    try:
        plato = session.query(Plato).filter_by(id_plato=id_plato).first()
        if plato is None:
            return None
        if nombre:
            plato.nombre = nombre
        if precio is not None:
            plato.precio = precio
        if descripcion:
            plato.descripcion = descripcion
        if ids_insumos is not None:
            insumos = (
                session.query(Inventario)
                .filter(Inventario.id_insumo.in_(ids_insumos))
                .all()
            )
            plato.insumos = insumos
        plato.marcar_editado(id_usuario_edicion)
        session.commit()
        session.refresh(plato)
        _ = plato.insumos
        return plato
    finally:
        session.close()


def eliminar_plato(id_plato: uuid.UUID) -> bool:
    session = get_session()
    try:
        plato = session.query(Plato).filter_by(id_plato=id_plato).first()
        if plato is None:
            return False
        session.delete(plato)
        session.commit()
        return True
    finally:
        session.close()
