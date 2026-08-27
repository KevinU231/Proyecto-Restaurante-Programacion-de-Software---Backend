import uuid
from src.entities.Detalle_pedido import DetallePedido


class DetallePedidoCRUD:
    def __init__(self) -> None:
        # Lista donde se almacenan los detalles de los pedidos
        self.detalles: list[DetallePedido] = []

    def crear(
        self,
        id_pedido: uuid.UUID,
        id_producto: uuid.UUID,
        cantidad: int,
        precio_unitario: float,
        id_usuario_creacion: uuid.UUID,
    ) -> DetallePedido:
        """
        Crea un nuevo detalle de pedido.
        El subtotal se calcula automáticamente en la entidad.
        """
        detalle = DetallePedido(
            id_pedido=id_pedido,
            id_producto=id_producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            id_usuario_creacion=id_usuario_creacion,
        )

        self.detalles.append(detalle)
        return detalle

    def obtener(
        self,
        id_detalle_pedido: uuid.UUID,
    ) -> DetallePedido | None:
        """
        Busca un detalle de pedido por su ID.
        """
        for detalle in self.detalles:
            if detalle.id_detalle_pedido == id_detalle_pedido:
                return detalle

        return None

    def listar(self) -> list[DetallePedido]:
        """
        Retorna todos los detalles registrados.
        """
        return self.detalles

    def listar_por_pedido(
        self,
        id_pedido: uuid.UUID,
    ) -> list[DetallePedido]:
        """
        Retorna todos los detalles pertenecientes a un pedido específico.
        """
        return [detalle for detalle in self.detalles if detalle.id_pedido == id_pedido]

    def actualizar(
        self,
        id_detalle_pedido: uuid.UUID,
        id_usuario_edicion: uuid.UUID,
        id_pedido: uuid.UUID | None = None,
        id_producto: uuid.UUID | None = None,
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

        if id_producto is not None:
            detalle.id_producto = id_producto

        if cantidad is not None:
            detalle.cantidad = cantidad

        if precio_unitario is not None:
            detalle.precio_unitario = precio_unitario

        # Recalcula el subtotal con los valores actualizados
        detalle.subtotal = detalle.cantidad * detalle.precio_unitario

        detalle.marcar_editado(id_usuario_edicion)

        return detalle

    def eliminar(self, id_detalle_pedido: uuid.UUID) -> bool:
        """
        Elimina un detalle de pedido por su ID.
        """
        detalle = self.obtener(id_detalle_pedido)

        if detalle is None:
            return False

        self.detalles.remove(detalle)
        return True
