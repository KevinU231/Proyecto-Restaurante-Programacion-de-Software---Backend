import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base
from src.entities.plato import plato_insumo

class Inventario(Base):
    __tablename__ = "inventario"

    id_insumo: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_insumo: Mapped[str] = mapped_column(String(150), nullable=False)
    cantidad: Mapped[float] = mapped_column(Float, nullable=False)
    unidad_medida: Mapped[str] = mapped_column(String(50), nullable=False)

    id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    id_usuario_edicion: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    fecha_edicion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    platos: Mapped[List["Plato"]] = relationship(secondary=plato_insumo, back_populates="insumos")

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        return f"Inventario({self.id_insumo}) - {self.nombre_insumo}: {self.cantidad} {self.unidad_medida}"