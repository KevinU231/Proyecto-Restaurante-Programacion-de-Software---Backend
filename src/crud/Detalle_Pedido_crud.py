import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.Detalle_pedido import DetallePedido


class DetallePedidoCRUD:
    """
    CRUD para gestionar los detalles de los pedidos.
    """

    def __init__(self, db: Session) -> None:
        """
        Recibe una sesión de SQLAlchemy.
        """
        self.db = db

    def crear(
        self,
        id_pedido: uuid.UUID,
        id_plato: uuid.UUID,
        cantidad: int,
        precio_unitario: float,
        id_usuario_creacion: uuid.UUID | None,
    ) -> DetallePedido:
        """
        Crea un nuevo detalle de pedido.
        El subtotal se calcula automáticamente en la entidad.
        """

        detalle = DetallePedido(
            id_pedido=id_pedido,
            id_plato=id_plato,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            id_usuario_creacion=id_usuario_creacion,
        )

        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)

        return detalle

    def obtener(
        self,
        id_detalle_pedido: uuid.UUID,
    ) -> DetallePedido | None:
        """
        Busca un detalle de pedido por su ID.
        """

        consulta = select(DetallePedido).where(
            DetallePedido.id_detalle_pedido == id_detalle_pedido
        )

        return self.db.scalar(consulta)

    def listar(self) -> list[DetallePedido]:
        """
        Obtiene todos los detalles registrados.
        """

        consulta = select(DetallePedido)

        return list(self.db.scalars(consulta).all())

    def listar_por_pedido(
        self,
        id_pedido: uuid.UUID,
    ) -> list[DetallePedido]:
        """
        Obtiene todos los detalles pertenecientes
        a un pedido específico.
        """

        consulta = select(DetallePedido).where(DetallePedido.id_pedido == id_pedido)

        return list(self.db.scalars(consulta).all())

    def actualizar(
        self,
        id_detalle_pedido: uuid.UUID,
        id_usuario_edicion: uuid.UUID,
        id_pedido: uuid.UUID | None = None,
        id_plato: uuid.UUID | None = None,
        cantidad: int | None = None,
        precio_unitario: float | None = None,
    ) -> DetallePedido | None:
        """
        Actualiza los datos del detalle.
        Si cambia la cantidad o el precio, recalcula el subtotal.
        """

        detalle = self.obtener(id_detalle_pedido)

        if detalle is None:
            return None

        if id_pedido is not None:
            detalle.id_pedido = id_pedido

        if id_plato is not None:
            detalle.id_plato = id_plato

        if cantidad is not None:
            detalle.cantidad = cantidad

        if precio_unitario is not None:
            detalle.precio_unitario = precio_unitario

        detalle.subtotal = detalle.cantidad * detalle.precio_unitario

        detalle.marcar_editado(id_usuario_edicion)

        self.db.commit()
        self.db.refresh(detalle)

        return detalle

    def eliminar(
        self,
        id_detalle_pedido: uuid.UUID,
    ) -> bool:
        """
        Elimina un detalle de pedido por su ID.
        """

        detalle = self.obtener(id_detalle_pedido)

        if detalle is None:
            return False

        self.db.delete(detalle)
        self.db.commit()

        return True
