import uuid
from typing import Optional
from src.entities.domicilio import Domicilio

domicilios: list[Domicilio] = []


def crear_domicilio(
    id_cliente: uuid.UUID,
    direccion_entrega: str,
    ids_platos: list[uuid.UUID],
    id_usuario_creacion: uuid.UUID,
    estado: str = "pendiente",
) -> Domicilio:
    nuevo = Domicilio(id_cliente, direccion_entrega, ids_platos, id_usuario_creacion, estado)
    domicilios.append(nuevo)
    return nuevo


def listar_domicilios() -> list[Domicilio]:
    return domicilios


def buscar_domicilio(id_domicilio: uuid.UUID) -> Optional[Domicilio]:
    for domicilio in domicilios:
        if domicilio.id_domicilio == id_domicilio:
            return domicilio
    return None


def actualizar_domicilio(
    id_domicilio: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    direccion_entrega: Optional[str] = None,
    ids_platos: Optional[list[uuid.UUID]] = None,
    estado: Optional[str] = None,
) -> Optional[Domicilio]:
    domicilio = buscar_domicilio(id_domicilio)
    if domicilio is None:
        return None
    if direccion_entrega:
        domicilio.direccion_entrega = direccion_entrega
    if ids_platos is not None:
        domicilio.ids_platos = ids_platos
    if estado:
        domicilio.estado = estado
    domicilio.marcar_editado(id_usuario_edicion)
    return domicilio


def eliminar_domicilio(id_domicilio: uuid.UUID) -> bool:
    domicilio = buscar_domicilio(id_domicilio)
    if domicilio is None:
        return False
    domicilios.remove(domicilio)
    return True