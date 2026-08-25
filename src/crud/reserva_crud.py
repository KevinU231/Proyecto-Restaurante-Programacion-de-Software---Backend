import uuid
from typing import Optional
from src.entities.reserva import Reserva

reservas: list[Reserva] = []


def crear_reserva(
    id_cliente: uuid.UUID,
    id_mesa: uuid.UUID,
    fecha: str,
    hora: str,
    num_personas: int,
    id_usuario_creacion: uuid.UUID,
    estado: str = "confirmada",
) -> Reserva:
    nueva = Reserva(
        id_cliente,
        id_mesa,
        fecha,
        hora,
        num_personas,
        id_usuario_creacion,
        estado,
    )
    reservas.append(nueva)
    return nueva


def listar_reservas() -> list[Reserva]:
    return reservas


def buscar_reserva(id_reserva: uuid.UUID) -> Optional[Reserva]:
    for reserva in reservas:
        if reserva.id_reserva == id_reserva:
            return reserva
    return None


def actualizar_reserva(
    id_reserva: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    fecha: Optional[str] = None,
    hora: Optional[str] = None,
    num_personas: Optional[int] = None,
    estado: Optional[str] = None,
) -> Optional[Reserva]:
    reserva = buscar_reserva(id_reserva)
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
    reserva.marcar_editado(id_usuario_edicion)
    return reserva


def eliminar_reserva(id_reserva: uuid.UUID) -> bool:
    reserva = buscar_reserva(id_reserva)
    if reserva is None:
        return False
    reservas.remove(reserva)
    return True
