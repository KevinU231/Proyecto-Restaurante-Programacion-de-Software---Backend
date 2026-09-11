import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.Pedido import Pedido


class PedidoCRUD:
    """
    CRUD para gestionar los pedidos.

    CRUD significa:
    - Create: crear
    - Read: consultar
    - Update: actualizar
    - Delete: eliminar
    """

    def __init__(self, db: Session) -> None:
        """
        Recibe una sesión de SQLAlchemy.
        """
        self.db = db

    def crear(
        self,
        id_empleado: uuid.UUID,
        id_cliente: uuid.UUID,
        estado: str,
        total: float,
        id_usuario_creacion: uuid.UUID | None,
        id_mesa: uuid.UUID | None = None,
    ) -> Pedido:
        """
        Crea un nuevo pedido y lo guarda en la base de datos.
        """

        pedido = Pedido(
            id_empleado=id_empleado,
            id_cliente=id_cliente,
            estado=estado.strip(),
            total=total,
            id_usuario_creacion=id_usuario_creacion,
            id_mesa=id_mesa,
        )

        self.db.add(pedido)
        self.db.commit()
        self.db.refresh(pedido)

        return pedido

    def obtener(
        self,
        id_pedido: uuid.UUID,
    ) -> Pedido | None:
        """
        Busca un pedido por su ID.
        """

        consulta = select(Pedido).where(Pedido.id_pedido == id_pedido)

        return self.db.scalar(consulta)

    def listar(self) -> list[Pedido]:
        """
        Obtiene todos los pedidos registrados.
        """

        consulta = select(Pedido)

        return list(self.db.scalars(consulta).all())

    def actualizar(
        self,
        id_pedido: uuid.UUID,
        id_usuario_edicion: uuid.UUID,
        id_empleado: uuid.UUID | None = None,
        id_cliente: uuid.UUID | None = None,
        id_mesa: uuid.UUID | None = None,
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

        if id_cliente is not None:
            pedido.id_cliente = id_cliente

        if id_mesa is not None:
            pedido.id_mesa = id_mesa

        if estado is not None:
            pedido.estado = estado.strip()

        if total is not None:
            pedido.total = total

        pedido.marcar_editado(id_usuario_edicion)

        self.db.commit()
        self.db.refresh(pedido)

        return pedido

    def eliminar(
        self,
        id_pedido: uuid.UUID,
    ) -> bool:
        """
        Elimina un pedido por su ID.
        """

        pedido = self.obtener(id_pedido)

        if pedido is None:
            return False

        self.db.delete(pedido)
        self.db.commit()

        return True
