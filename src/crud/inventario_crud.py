import uuid
from typing import Optional

from src.database.connection import get_session
from src.entities.inventario import Inventario


def crear_inventario(
    nombre_insumo: str,
    cantidad: float,
    unidad_medida: str,
    id_usuario_creacion: uuid.UUID,
) -> Inventario:
    session = get_session()
    try:
        nuevo = Inventario(
            nombre_insumo=nombre_insumo,
            cantidad=cantidad,
            unidad_medida=unidad_medida,
            id_usuario_creacion=id_usuario_creacion,
        )
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        return nuevo
    finally:
        session.close()


def listar_inventarios() -> list[Inventario]:
    session = get_session()
    try:
        return session.query(Inventario).all()
    finally:
        session.close()


def buscar_inventario(id_insumo: uuid.UUID) -> Optional[Inventario]:
    session = get_session()
    try:
        return session.query(Inventario).filter_by(id_insumo=id_insumo).first()
    finally:
        session.close()


def actualizar_inventario(
    id_insumo: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    nombre_insumo: Optional[str] = None,
    cantidad: Optional[float] = None,
    unidad_medida: Optional[str] = None,
) -> Optional[Inventario]:
    session = get_session()
    try:
        insumo = session.query(Inventario).filter_by(id_insumo=id_insumo).first()
        if insumo is None:
            return None
        if nombre_insumo:
            insumo.nombre_insumo = nombre_insumo
        if cantidad is not None:
            insumo.cantidad = cantidad
        if unidad_medida:
            insumo.unidad_medida = unidad_medida
        insumo.marcar_editado(id_usuario_edicion)
        session.commit()
        session.refresh(insumo)
        return insumo
    finally:
        session.close()


def eliminar_inventario(id_insumo: uuid.UUID) -> bool:
    session = get_session()
    try:
        insumo = session.query(Inventario).filter_by(id_insumo=id_insumo).first()
        if insumo is None:
            return False
        session.delete(insumo)
        session.commit()
        return True
    finally:
        session.close()
