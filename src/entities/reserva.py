import uuid
from datetime import datetime
from typing import Optional


class Reserva:
    def __init__(
        self,
        fecha: str,
        hora: str,
        num_personas: int,
        id_usuario_creacion: uuid.UUID,
        id_cliente: uuid.UUID,  # Llave foranea, referencia al uuid de Cliente
        id_mesa: uuid.UUID,  # Llave foranea, referencia al uuid de Mesa
        estado: str = "confirmada",
    ) -> None:
        self.id_reserva: uuid.UUID = uuid.uuid4()
        self.fecha = fecha.strip()
        self.hora = hora.strip()
        self.num_personas = num_personas.strip()
        self.estado = estado.strip()  # Confirmada, Cancelada, Culminada
        self.id_cliente = id_cliente
        self.id_mesa = id_mesa

        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion: Optional[uuid.UUID] = None
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_edicion: Optional[datetime] = None

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self):
        return (
            f"Reserva({self.id_reserva}) - {self.fecha} {self.hora}"
            f"/ Personas: {self.num_personas} / Estado: {self.estado}"
        )
