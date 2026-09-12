import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, ForeignKey  # agregar ForeignKey al import
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Empleado(Base):
    __tablename__ = "empleados"

    id_empleado: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    nombre: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str] = mapped_column(String(20))
    correo: Mapped[str] = mapped_column(String(100))
    cargo: Mapped[str] = mapped_column(String(100))
    id_usuario_creacion: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    id_usuario_edicion: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("usuarios.id_usuario"), nullable=True
    )
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    fecha_edicion: Mapped[Optional[datetime]] = mapped_column(DateTime)

    def __init__(
        self,
        nombre: str,
        telefono: str,
        correo: str,
        cargo: str,
        id_usuario_creacion: Optional[uuid.UUID],
    ) -> None:
        # Genera automáticamente un ID único para el empleado
        self.id_empleado: uuid.UUID = uuid.uuid4()

        # strip() elimina espacios innecesarios al principio y al final
        self.nombre = nombre.strip()
        self.telefono = telefono.strip()
        self.correo = correo.strip()
        self.cargo = cargo.strip()

        # Datos utilizados para saber quién creó el registro
        self.id_usuario_creacion = id_usuario_creacion

        # Estos datos permanecen vacíos hasta que el empleado sea editado
        self.id_usuario_edicion: Optional[uuid.UUID] = None
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_edicion: Optional[datetime] = None

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        """
        Registra quién realizó la última edición
        y cuándo se realizó.
        """
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        """
        Devuelve una representación sencilla del empleado
        cuando se imprime.
        """
        return f"Empleado({self.id_empleado}) - {self.nombre} / Cargo: {self.cargo}"
