import uuid

from src.database.connection import get_session
from src.entities.reserva import Reserva
from src.crud.usuario_crud import marcar_editado


def crear_reserva(
    id_cliente,
    id_mesa,
    fecha,
    hora,
    num_personas,
    id_usuario_creacion,
    estado="confirmada",
):
    session = get_session()
    try:
        reserva = Reserva(
            id_cliente=id_cliente,
            id_mesa=id_mesa,
            fecha=fecha,
            hora=hora,
            num_personas=num_personas,
            estado=estado,
            id_usuario_creacion=id_usuario_creacion,
        )
        session.add(reserva)
        session.commit()
        session.refresh(reserva)
        return reserva
    finally:
        session.close()


def listar_reservas():
    session = get_session()
    try:
        return session.query(Reserva).all()
    finally:
        session.close()


def buscar_reserva(id_reserva: uuid.UUID):
    session = get_session()
    try:
        return session.query(Reserva).filter_by(id_reserva=id_reserva).first()
    finally:
        session.close()


def actualizar_reserva(
    id_reserva,
    id_usuario_edicion,
    fecha=None,
    hora=None,
    num_personas=None,
    estado=None,
):
    session = get_session()
    try:
        reserva = session.query(Reserva).filter_by(id_reserva=id_reserva).first()
        if reserva is None:
            return None
        if fecha:
            reserva.fecha = fecha
        if hora:
            reserva.hora = hora
        if num_personas is not None:
            reserva.num_personas = num_personas
        if estado:
            reserva.estado = estado
        marcar_editado(reserva, id_usuario_edicion)
        session.commit()
        session.refresh(reserva)
        return reserva
    finally:
        session.close()


def eliminar_reserva(id_reserva: uuid.UUID) -> bool:
    session = get_session()
    try:
        reserva = session.query(Reserva).filter_by(id_reserva=id_reserva).first()
        if reserva is None:
            return False
        session.delete(reserva)
        session.commit()
        return True
    finally:
        session.close()
