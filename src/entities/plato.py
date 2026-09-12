import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Float, DateTime, ForeignKey, Table, Column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base

# Tabla de asociación Plato <-> Inventario (muchos a muchos)
plato_insumo = Table(
    "plato_insumo",
    Base.metadata,
    Column(
        "id_plato",
        PGUUID(as_uuid=True),
        ForeignKey("platos.id_plato"),
        primary_key=True,
    ),
    Column(
        "id_insumo",
        PGUUID(as_uuid=True),
        ForeignKey("inventario.id_insumo"),
        primary_key=True,
    ),
)


class Plato(Base):
    __tablename__ = "platos"

    id_plato: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edicion: Mapped[Optional[uuid.UUID]] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    fecha_edicion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    insumos: Mapped[List["Inventario"]] = relationship(
        secondary=plato_insumo, back_populates="platos"
    )

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        return f"Plato({self.id_plato}) - {self.nombre}: ${self.precio}"
