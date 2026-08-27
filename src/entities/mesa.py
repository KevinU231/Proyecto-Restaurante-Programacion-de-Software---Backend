import uuid
from datetime import datetime
from typing import Optional


class Mesa:
    def __init__(
        self,
        numero: int,
        capacidad: int,
        id_usuario_creacion: uuid.UUID,
        estado: str = "libre",
    ) -> None:
        self.id_mesa: uuid.UUID = uuid.uuid4()
        self.numero = numero.strip()
        self.capacidad = capacidad.strip()
        self.estado = estado.strip()  # Libre, ocupada, reservada

        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion: Optional[uuid.UUID] = None
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_edicion: Optional[datetime] = None

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        return f"Mesa({self.id_mesa}) - Numero: {self.numero} / Capacidad: {self.capacidad}"
