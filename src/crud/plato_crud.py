import uuid
from typing import Optional
from src.entities.plato import Plato

platos: list[Plato] = []


def crear_plato(
    nombre: str,
    precio: float,
    descripcion: str,
    ids_insumos: list[uuid.UUID],
    id_usuario_creacion: uuid.UUID,
) -> Plato:
    nuevo = Plato(nombre, precio, descripcion, ids_insumos, id_usuario_creacion)
    platos.append(nuevo)
    return nuevo


def listar_platos() -> list[Plato]:
    return platos


def buscar_plato(id_plato: uuid.UUID) -> Optional[Plato]:
    for plato in platos:
        if plato.id_plato == id_plato:
            return plato
    return None


def actualizar_plato(
    id_plato: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    nombre: Optional[str] = None,
    precio: Optional[float] = None,
    descripcion: Optional[str] = None,
    ids_insumos: Optional[list[uuid.UUID]] = None,
) -> Optional[Plato]:
    plato = buscar_plato(id_plato)
    if plato is None:
        return None
    if nombre:
        plato.nombre = nombre
    if precio is not None:
        plato.precio = precio
    if descripcion:
        plato.descripcion = descripcion
    if ids_insumos is not None:
        plato.ids_insumos = ids_insumos
    plato.marcar_editado(id_usuario_edicion)
    return plato


def eliminar_plato(id_plato: uuid.UUID) -> bool:
    plato = buscar_plato(id_plato)
    if plato is None:
        return False
    platos.remove(plato)
    return True