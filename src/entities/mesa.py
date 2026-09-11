import uuid
from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Mesa(Base):
    __tablename__ = "mesas"

    id_mesa: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    numero: Mapped[int] = mapped_column(Integer)
    capacidad: Mapped[int] = mapped_column(Integer)
    estado: Mapped[str] = mapped_column(String(20), default="libre")

    id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("usuarios.id_usuario")
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    id_usuario_edicion: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_edicion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __str__(self) -> str:
        return f"Mesa({self.id_mesa}) - N°{self.numero} | Capacidad: {self.capacidad} | Estado: {self.estado}"
