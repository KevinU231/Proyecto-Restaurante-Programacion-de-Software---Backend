import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, DateTime, ForeignKey, Table, Column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.connection import Base

menu_plato = Table(
    "menu_plato",
    Base.metadata,
    Column(
        "id_menu", PGUUID(as_uuid=True), ForeignKey("menus.id_menu"), primary_key=True
    ),
    Column(
        "id_plato",
        PGUUID(as_uuid=True),
        ForeignKey("platos.id_plato"),
        primary_key=True,
    ),
)


class Menu(Base):
    __tablename__ = "menus"

    id_menu: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    nombre: Mapped[str] = mapped_column(String(150), nullable=False)
    descripcion: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, default=""
    )

    id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuario_edicion: Mapped[Optional[uuid.UUID]] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    fecha_edicion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    platos: Mapped[List["Plato"]] = relationship(secondary=menu_plato)

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        return f"Menu({self.id_menu}) - {self.nombre}: {len(self.platos)} platos"
