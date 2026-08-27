import uuid
from typing import Optional
from src.entities.mesa import Mesa

mesas: list[Mesa] = []


def crear_mesa(
    numero: int,
    capacidad: int,
    id_usuario_creacion: uuid.UUID,
    estado: str = "libre",
) -> Mesa:
    nueva = Mesa(numero, capacidad, id_usuario_creacion, estado)
    mesas.append(nueva)
    return nueva


def listar_mesas() -> list[Mesa]:
    return mesas


def buscar_mesa(id_mesa: uuid.UUID) -> Optional[Mesa]:
    for mesa in mesas:
        if mesa.id_mesa == id_mesa:
            return mesa
    return None


def actualizar_mesa(
    id_mesa: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    numero: Optional[int] = None,
    capacidad: Optional[int] = None,
    estado: Optional[str] = None,
) -> Optional[Mesa]:
    mesa = buscar_mesa(id_mesa)
    if mesa is None:
        return None
    if numero is not None:
        mesa.numero = numero
    if capacidad is not None:
        mesa.capacidad = capacidad
    if estado:
        mesa.estado = estado
    mesa.marcar_editado(id_usuario_edicion)
    return mesa


def eliminar_mesa(id_mesa: uuid.UUID) -> bool:
    mesa = buscar_mesa(id_mesa)
    if mesa is None:
        return False
    mesas.remove(mesa)
    return True
