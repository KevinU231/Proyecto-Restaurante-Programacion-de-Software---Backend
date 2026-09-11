import uuid

from src.database.connection import get_session
from src.entities.cliente import Cliente
from src.crud.usuario_crud import marcar_editado


def crear_cliente(nombre, telefono, correo, id_usuario_creacion, direccion=""):
    session = get_session()
    try:
        cliente = Cliente(
            nombre=nombre,
            telefono=telefono,
            correo=correo,
            direccion=direccion,
            id_usuario_creacion=id_usuario_creacion,
        )
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente
    finally:
        session.close()


def listar_clientes():
    session = get_session()
    try:
        return session.query(Cliente).all()
    finally:
        session.close()


def buscar_cliente(id_cliente: uuid.UUID):
    session = get_session()
    try:
        return session.query(Cliente).filter_by(id_cliente=id_cliente).first()
    finally:
        session.close()


def actualizar_cliente(
    id_cliente,
    id_usuario_edicion,
    nombre=None,
    telefono=None,
    correo=None,
    direccion=None,
):
    session = get_session()
    try:
        cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
        if cliente is None:
            return None
        if nombre:
            cliente.nombre = nombre
        if telefono:
            cliente.telefono = telefono
        if correo:
            cliente.correo = correo
        if direccion:
            cliente.direccion = direccion
        marcar_editado(cliente, id_usuario_edicion)
        session.commit()
        session.refresh(cliente)
        return cliente
    finally:
        session.close()


def eliminar_cliente(id_cliente: uuid.UUID) -> bool:
    session = get_session()
    try:
        cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
        if cliente is None:
            return False
        session.delete(cliente)
        session.commit()
        return True
    finally:
        session.close()
