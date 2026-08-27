import uuid
from datetime import datetime
from typing import Optional


class Factura:
    def __init__(
        self,
        id_pedido: uuid.UUID,
        metodo_pago: str,
        total: float,
        id_usuario_creacion: uuid.UUID,
    ) -> None:
        # Genera automáticamente el ID de la factura
        self.id_factura: uuid.UUID = uuid.uuid4()

        # Relaciona la factura con el pedido correspondiente
        self.id_pedido = id_pedido

        self.metodo_pago = metodo_pago.strip()
        self.total = total

        # Datos de auditoría
        self.id_usuario_creacion = id_usuario_creacion
        self.id_usuario_edicion: Optional[uuid.UUID] = None
        self.fecha_creacion: datetime = datetime.now()
        self.fecha_edicion: Optional[datetime] = None

    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        """
        Registra quién realizó una modificación
        y cuándo se realizó.
        """
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def cambiar_metodo_pago(self, nuevo_metodo: str) -> None:
        """
        Permite cambiar el método de pago de la factura.
        """
        self.metodo_pago = nuevo_metodo.strip()

    def __str__(self) -> str:
        """
        Devuelve una representación de la factura
        cuando se imprime.
        """
        return (
            f"Factura({self.id_factura}) - "
            f"Pedido: {self.id_pedido} / "
            f"Total: ${self.total:.2f} / "
            f"Pago: {self.metodo_pago}"
        )
