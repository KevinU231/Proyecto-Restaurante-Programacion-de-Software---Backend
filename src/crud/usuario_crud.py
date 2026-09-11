import uuid
from datetime import datetime

from src.database.connection import get_session
from src.entities.usuario import Usuario


def nombre_completo(usuario: Usuario) -> str:
    partes = [
        usuario.primer_nombre,
        usuario.segundo_nombre,
        usuario.primer_apellido,
        usuario.segundo_apellido,
    ]
    return " ".join(parte for parte in partes if parte)


def marcar_editado(objeto, id_usuario_edicion: uuid.UUID) -> None:
    objeto.id_usuario_edicion = id_usuario_edicion
    objeto.fecha_edicion = datetime.now()


def crear_usuario(
    nombre_usuario,
    primer_nombre,
    segundo_nombre,
    primer_apellido,
    segundo_apellido,
    clave,
    id_empleado,
    id_usuario_creacion=None,
):
    session = get_session()
    try:
        usuario = Usuario(
            nombre_usuario=nombre_usuario,
            primer_nombre=primer_nombre,
            segundo_nombre=segundo_nombre,
            primer_apellido=primer_apellido,
            segundo_apellido=segundo_apellido,
            clave=clave,
            id_empleado=id_empleado,
            id_usuario_creacion=id_usuario_creacion,
        )
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario
    finally:
        session.close()


def listar_usuarios():
    session = get_session()
    try:
        return session.query(Usuario).all()
    finally:
        session.close()


def buscar_usuario(id_usuario: uuid.UUID):
    session = get_session()
    try:
        return session.query(Usuario).filter_by(id_usuario=id_usuario).first()
    finally:
        session.close()


def iniciar_sesion(nombre_usuario: str, clave: str):
    session = get_session()
    try:
        return (
            session.query(Usuario)
            .filter_by(nombre_usuario=nombre_usuario, clave=clave)
            .first()
        )
    finally:
        session.close()


def actualizar_usuario(
    id_usuario, id_usuario_edicion, nombre_usuario=None, primer_nombre=None, clave=None
):
    session = get_session()
    try:
        usuario = session.query(Usuario).filter_by(id_usuario=id_usuario).first()
        if usuario is None:
            return None
        if nombre_usuario:
            usuario.nombre_usuario = nombre_usuario
        if primer_nombre:
            usuario.primer_nombre = primer_nombre
        if clave:
            usuario.clave = clave
        marcar_editado(usuario, id_usuario_edicion)
        session.commit()
        session.refresh(usuario)
        return usuario
    finally:
        session.close()


def eliminar_usuario(id_usuario: uuid.UUID) -> bool:
    session = get_session()
    try:
        usuario = session.query(Usuario).filter_by(id_usuario=id_usuario).first()
        if usuario is None:
            return False
        session.delete(usuario)
        session.commit()
        return True
    finally:
        session.close()
