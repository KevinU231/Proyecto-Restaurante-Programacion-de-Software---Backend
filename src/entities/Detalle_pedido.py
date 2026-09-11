import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Numeric, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.database.connection import Base


class DetallePedido(Base):
    __tablename__ = "detalles_pedido"

    id_detalle_pedido: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    id_pedido: Mapped[uuid.UUID] = mapped_column(ForeignKey("pedidos.id_pedido"))
    id_plato: Mapped[uuid.UUID] = mapped_column(ForeignKey("platos.id_plato"))
    cantidad: Mapped[int] = mapped_column()
    precio_unitario: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    subtotal: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    id_usuario_creacion: Mapped[Optional[uuid.UUID]] = mapped_column(nullable=True)
    id_usuario_edicion: Mapped[Optional[uuid.UUID]] = mapped_column(nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    fecha_edicion: Mapped[Optional[datetime]] = mapped_column(DateTime)

    def __init__(
        self,
        id_pedido: uuid.UUID,
        id_plato: uuid.UUID,
        cantidad: int,
        precio_unitario: float,
        id_usuario_creacion: Optional[uuid.UUID],
    ) -> None:
        # ID único del detalle
        self.id_detalle_pedido: uuid.UUID = uuid.uuid4()

        # ID que relacionan este detalle
        # con el pedido y el producto correspondiente
        self.id_pedido = id_pedido
        self.id_plato = id_plato

        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

        # Calcula automáticamente el subtotal
        self.subtotal: float = cantidad * precio_unitario

        # Datos de auditoría
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion: Optional[uuid.UUID] = None
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_edicion: Optional[datetime] = None

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        """
        Registra quién modificó el detalle y cuándo lo hizo.
        """
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def actualizar_cantidad(self, nueva_cantidad: int) -> None:
        """
        Cambia la cantidad del producto y recalcula
        automáticamente el subtotal.
        """
        self.cantidad = nueva_cantidad
        self.subtotal = self.cantidad * self.precio_unitario

    def __str__(self) -> str:
        """
        Devuelve una representación del detalle del pedido.
        """
        return (
            f"DetallePedido({self.id_detalle_pedido}) - "
            f"Cantidad: {self.cantidad} / "
            f"Subtotal: ${self.subtotal:.2f}"
        )
