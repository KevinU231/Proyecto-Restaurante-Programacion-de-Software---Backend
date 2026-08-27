import uuid
from src.entities.Pedido import Pedido


class PedidoCRUD:
    def __init__(self) -> None:
        # Lista donde se almacenan los pedidos
        self.pedidos: list[Pedido] = []

    def crear(
        self,
        id_empleado: uuid.UUID,
        estado: str,
        total: float,
        id_usuario_creacion: uuid.UUID,
    ) -> Pedido:
        """
        Crea un nuevo pedido y lo agrega a la lista.
        """
        pedido = Pedido(
            id_empleado=id_empleado,
            estado=estado,
            total=total,
            id_usuario_creacion=id_usuario_creacion,
        )

        self.pedidos.append(pedido)
        return pedido

    def obtener(self, id_pedido: uuid.UUID) -> Pedido | None:
        """
        Busca un pedido por su ID.
        """
        for pedido in self.pedidos:
            if pedido.id_pedido == id_pedido:
                return pedido

        return None

    def listar(self) -> list[Pedido]:
        """
        Retorna todos los pedidos registrados.
        """
        return self.pedidos

    def actualizar(
        self,
        id_pedido: uuid.UUID,
        id_usuario_edicion: uuid.UUID,
        id_empleado: uuid.UUID | None = None,
        estado: str | None = None,
        total: float | None = None,
    ) -> Pedido | None:
        """
        Actualiza los datos de un pedido.
        """
        pedido = self.obtener(id_pedido)

        if pedido is None:
            return None

        if id_empleado is not None:
            pedido.id_empleado = id_empleado

        if estado is not None:
            pedido.estado = estado.strip()

        if total is not None:
            pedido.total = total

        pedido.marcar_editado(id_usuario_edicion)

        return pedido

    def eliminar(self, id_pedido: uuid.UUID) -> bool:
        """
        Elimina un pedido por su ID.
        """
        pedido = self.obtener(id_pedido)

        if pedido is None:
            return False

        self.pedidos.remove(pedido)
        return True
