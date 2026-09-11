import uuid

from src.database.connection import get_session
from src.entities.mesa import Mesa
from src.crud.usuario_crud import marcar_editado


def crear_mesa(numero, capacidad, id_usuario_creacion, estado="libre"):
    session = get_session()
    try:
        mesa = Mesa(
            numero=numero,
            capacidad=capacidad,
            estado=estado,
            id_usuario_creacion=id_usuario_creacion,
        )
        session.add(mesa)
        session.commit()
        session.refresh(mesa)
        return mesa
    finally:
        session.close()


def listar_mesas():
    session = get_session()
    try:
        return session.query(Mesa).all()
    finally:
        session.close()


def buscar_mesa(id_mesa: uuid.UUID):
    session = get_session()
    try:
        return session.query(Mesa).filter_by(id_mesa=id_mesa).first()
    finally:
        session.close()


def actualizar_mesa(
    id_mesa, id_usuario_edicion, numero=None, capacidad=None, estado=None
):
    session = get_session()
    try:
        mesa = session.query(Mesa).filter_by(id_mesa=id_mesa).first()
        if mesa is None:
            return None
        if numero is not None:
            mesa.numero = numero
        if capacidad is not None:
            mesa.capacidad = capacidad
        if estado:
            mesa.estado = estado
        marcar_editado(mesa, id_usuario_edicion)
        session.commit()
        session.refresh(mesa)
        return mesa
    finally:
        session.close()


def eliminar_mesa(id_mesa: uuid.UUID) -> bool:
    session = get_session()
    try:
        mesa = session.query(Mesa).filter_by(id_mesa=id_mesa).first()
        if mesa is None:
            return False
        session.delete(mesa)
        session.commit()
        return True
    finally:
        session.close()
