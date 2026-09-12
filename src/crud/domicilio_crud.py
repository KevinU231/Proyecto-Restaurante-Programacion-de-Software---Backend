import uuid
from typing import Optional

from sqlalchemy.orm import selectinload

from src.database.connection import get_session
from src.entities.domicilio import Domicilio
from src.entities.plato import Plato


def crear_domicilio(
    id_cliente: uuid.UUID,
    direccion_entrega: str,
    ids_platos: list[uuid.UUID],
    id_usuario_creacion: uuid.UUID,
    estado: str = "pendiente",
) -> Domicilio:
    session = get_session()
    try:
        nuevo = Domicilio(
            id_cliente=id_cliente,
            direccion_entrega=direccion_entrega,
            estado=estado,
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


def listar_domicilios() -> list[Domicilio]:
    session = get_session()
    try:
        return (
            session.query(Domicilio)
            .options(selectinload(Domicilio.platos))
            .all()
        )
    finally:
        session.close()


def buscar_domicilio(id_domicilio: uuid.UUID) -> Optional[Domicilio]:
    session = get_session()
    try:
        return (
            session.query(Domicilio)
            .options(selectinload(Domicilio.platos))
            .filter_by(id_domicilio=id_domicilio)
            .first()
        )
    finally:
        session.close()


def actualizar_domicilio(
    id_domicilio: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    direccion_entrega: Optional[str] = None,
    ids_platos: Optional[list[uuid.UUID]] = None,
    estado: Optional[str] = None,
) -> Optional[Domicilio]:
    session = get_session()
    try:
        domicilio = (
            session.query(Domicilio)
            .filter_by(id_domicilio=id_domicilio)
            .first()
        )
        if domicilio is None:
            return None
        if direccion_entrega:
            domicilio.direccion_entrega = direccion_entrega
        if ids_platos is not None:
            platos = (
                session.query(Plato)
                .filter(Plato.id_plato.in_(ids_platos))
                .all()
            )
            domicilio.platos = platos
        if estado:
            domicilio.estado = estado
        domicilio.marcar_editado(id_usuario_edicion)
        session.commit()
        session.refresh(domicilio)
        _ = domicilio.platos
        return domicilio
    finally:
        session.close()


def eliminar_domicilio(id_domicilio: uuid.UUID) -> bool:
    session = get_session()
    try:
        domicilio = (
            session.query(Domicilio)
            .filter_by(id_domicilio=id_domicilio)
            .first()
        )
        if domicilio is None:
            return False
        session.delete(domicilio)
        session.commit()
        return True
    finally:
        session.close()
