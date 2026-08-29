import uuid
from typing import Optional
from src.entities.inventario import Inventario

inventarios: list[Inventario] = []


def crear_inventario(
    nombre_insumo: str,
    cantidad: float,
    unidad_medida: str,
    id_usuario_creacion: uuid.UUID,
) -> Inventario:
    nuevo = Inventario(nombre_insumo, cantidad, unidad_medida, id_usuario_creacion)
    inventarios.append(nuevo)
    return nuevo


def listar_inventarios() -> list[Inventario]:
    return inventarios


def buscar_inventario(id_insumo: uuid.UUID) -> Optional[Inventario]:
    for insumo in inventarios:
        if insumo.id_insumo == id_insumo:
            return insumo
    return None


def actualizar_inventario(
    id_insumo: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    nombre_insumo: Optional[str] = None,
    cantidad: Optional[float] = None,
    unidad_medida: Optional[str] = None,
) -> Optional[Inventario]:
    insumo = buscar_inventario(id_insumo)
    if insumo is None:
        return None
    if nombre_insumo:
        insumo.nombre_insumo = nombre_insumo
    if cantidad is not None:
        insumo.cantidad = cantidad
    if unidad_medida:
        insumo.unidad_medida = unidad_medida
    insumo.marcar_editado(id_usuario_edicion)
    return insumo


def eliminar_inventario(id_insumo: uuid.UUID) -> bool:
    insumo = buscar_inventario(id_insumo)
    if insumo is None:
        return False
    inventarios.remove(insumo)
    return True