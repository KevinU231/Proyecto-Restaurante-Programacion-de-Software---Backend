import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    id_empleado: Mapped[uuid.UUID] = mapped_column(ForeignKey("empleados.id_empleado"))
    id_cliente: Mapped[uuid.UUID] = mapped_column(ForeignKey("clientes.id_cliente"))
    id_mesa: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("mesas.id_mesa"))
    estado: Mapped[str] = mapped_column(String(100))
    total: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
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
        id_empleado: uuid.UUID,
        # es obligatorio id_cliente ya que todo pedido pertenece a un cliente
        id_cliente: uuid.UUID,
        estado: str,
        total: float,
        id_usuario_creacion: Optional[uuid.UUID],
        id_mesa: Optional[uuid.UUID] = None,
    ) -> None:
        # Genera automáticamente el ID del pedido
        self.id_pedido: uuid.UUID = uuid.uuid4()

        # Guarda el empleado que tomó el pedido
        self.id_empleado = id_empleado

        self.id_cliente = id_cliente
        self.id_mesa = id_mesa
        self.estado = estado.strip()
        self.total = total

        # Datos de auditoría
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion: Optional[uuid.UUID] = None
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_edicion: Optional[datetime] = None

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        """
        Registra el usuario que modificó el pedido
        y la fecha en que se realizó la modificación.
        """
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def cambiar_estado(self, nuevo_estado: str) -> None:
        """
        Permite cambiar el estado actual del pedido.
        """
        self.estado = nuevo_estado.strip()

    def __str__(self) -> str:
        """
        Devuelve una representación del pedido
        cuando se imprime el objeto.
        """
        mesa_texto = str(self.id_mesa) if self.id_mesa else "Domicilio"
        return (
            f"Pedido({self.id_pedido}) - "
            f"Cliente: {self.id_cliente} / Mesa: {mesa_texto} / "
            f"Estado: {self.estado} / Total: ${self.total:.2f}"
        )
