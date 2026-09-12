import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Table, Column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base

domicilio_plato = Table(
    "domicilio_plato",
    Base.metadata,
    Column("id_domicilio", PGUUID(as_uuid=True), ForeignKey("domicilios.id_domicilio"), primary_key=True),
    Column("id_plato", PGUUID(as_uuid=True), ForeignKey("platos.id_plato"), primary_key=True),
)

class Domicilio(Base):
    __tablename__ = "domicilios"

    id_domicilio: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_cliente: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)  # referencia a Cliente (otro compañero)
    direccion_entrega: Mapped[str] = mapped_column(String(255), nullable=False)
    estado: Mapped[str] = mapped_column(String(30), nullable=False, default="pendiente")

    id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    id_usuario_edicion: Mapped[Optional[uuid.UUID]] = mapped_column(PGUUID(as_uuid=True), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    fecha_edicion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    platos: Mapped[List["Plato"]] = relationship(secondary=domicilio_plato)

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        return f"Domicilio({self.id_domicilio}) - Cliente: {self.id_cliente} / Estado: {self.estado}"