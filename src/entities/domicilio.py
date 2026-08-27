import uuid
from datetime import datetime
from typing import Optional


class Domicilio:
    def __init__(
        self,
        id_cliente: uuid.UUID,
        direccion_entrega: str,
        ids_platos: list[uuid.UUID],
        id_usuario_creacion: uuid.UUID,
        estado: str = "pendiente",
    ) -> None:
        self.id_domicilio: uuid.UUID = uuid.uuid4()
        self.id_cliente = id_cliente  # relación con Cliente (entidad de otro compañero)
        self.direccion_entrega = direccion_entrega.strip()
        self.ids_platos = ids_platos  # relación con Plato: platos que se van a entregar
        self.estado = estado  # ej: pendiente, en_camino, entregado

        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion: Optional[uuid.UUID] = None
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_edicion: Optional[datetime] = None

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        return f"Domicilio({self.id_domicilio}) - Cliente: {self.id_cliente} / Estado: {self.estado}"