import uuid
from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Reserva(Base):
    __tablename__ = "reservas"

    id_reserva: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_cliente: Mapped[uuid.UUID] = mapped_column(ForeignKey("clientes.id_cliente"))
    id_mesa: Mapped[uuid.UUID] = mapped_column(ForeignKey("mesas.id_mesa"))
    fecha: Mapped[str] = mapped_column(String(20))
    hora: Mapped[str] = mapped_column(String(10))
    num_personas: Mapped[int] = mapped_column(Integer)
    estado: Mapped[str] = mapped_column(String(20), default="confirmada")

    id_usuario_creacion: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("usuarios.id_usuario")
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    id_usuario_edicion: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_edicion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __str__(self) -> str:
        return (
            f"Reserva({self.id_reserva}) - {self.fecha} {self.hora} "
            f"| Personas: {self.num_personas} | Estado: {self.estado}"
        )
