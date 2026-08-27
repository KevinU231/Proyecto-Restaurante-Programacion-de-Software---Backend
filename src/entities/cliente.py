import uuid
from datetime import datetime
from typing import Optional


class Cliente:
    def __init__(
        self,
        nombre: str,
        telefono: str,
        correo: str,
        id_usuario_creacion: uuid.UUID,
        direccion: str = "",
    ) -> None:
        self.id_cliente: uuid.UUID = uuid.uuid4()
        self.nombre = nombre.strip()
        self.telefono = telefono.strip()
        self.correo = correo.strip()
        self.direccion = direccion.strip()

        # id usuario edicion y fecha edicion son None hasta que alguien edite al cliente por primera vez
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion: Optional[uuid.UUID] = None
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_edicion: Optional[datetime] = None

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        return f"Cliente({self.id_cliente}) - {self.nombre} / Tel: {self.telefono}"
