import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_empleado: Mapped[uuid.UUID] = mapped_column(ForeignKey("empleados.id_empleado"))
    nombre_usuario: Mapped[str] = mapped_column(String(80), unique=True)
    primer_nombre: Mapped[str] = mapped_column(String(80))
    segundo_nombre: Mapped[str] = mapped_column(String(80), default="")
    primer_apellido: Mapped[str] = mapped_column(String(80))
    segundo_apellido: Mapped[str] = mapped_column(String(80), default="")
    clave: Mapped[str] = mapped_column(String(255))

    id_usuario_creacion: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    id_usuario_edicion: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_edicion: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    def __str__(self) -> str:
        return f"Usuario({self.id_usuario}) - {self.primer_nombre} {self.primer_apellido} - {self.nombre_usuario}"
