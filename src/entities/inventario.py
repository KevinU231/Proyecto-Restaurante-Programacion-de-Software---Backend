import uuid
from datetime import datetime
from typing import Optional


class Inventario:
    def __init__(
        self,
        nombre_insumo: str,
        cantidad: float,
        unidad_medida: str,
        id_usuario_creacion: uuid.UUID,
    ) -> None:
        self.id_insumo: uuid.UUID = uuid.uuid4()
        self.nombre_insumo = nombre_insumo.strip()
        self.cantidad = cantidad
        self.unidad_medida = unidad_medida.strip()

        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion: Optional[uuid.UUID] = None
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_edicion: Optional[datetime] = None

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        return f"Inventario({self.id_insumo}) - {self.nombre_insumo}: {self.cantidad} {self.unidad_medida}"