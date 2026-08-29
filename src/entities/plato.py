import uuid
from datetime import datetime
from typing import Optional


class Plato:
    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        ids_insumos: list[uuid.UUID],
        id_usuario_creacion: uuid.UUID,
    ) -> None:
        self.id_plato: uuid.UUID = uuid.uuid4()
        self.nombre = nombre.strip()
        self.precio = precio
        self.descripcion = descripcion.strip()
        self.ids_insumos = ids_insumos  # relación con Inventario: ids de los insumos que usa este plato

        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion: Optional[uuid.UUID] = None
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_edicion: Optional[datetime] = None

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        return f"Plato({self.id_plato}) - {self.nombre}: ${self.precio}"