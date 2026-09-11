import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.Factura import Factura


class FacturaCRUD:
    """
    CRUD para gestionar las facturas.
    """

    def __init__(self, db: Session) -> None:
        """
        Recibe una sesión de SQLAlchemy.
        """
        self.db = db

    def crear(
        self,
        id_pedido: uuid.UUID,
        metodo_pago: str,
        total: float,
        id_usuario_creacion: uuid.UUID | None,
    ) -> Factura:
        """
        Crea una nueva factura y la guarda en la base de datos.
        """

        factura = Factura(
            id_pedido=id_pedido,
            metodo_pago=metodo_pago.strip(),
            total=total,
            id_usuario_creacion=id_usuario_creacion,
        )

        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)

        return factura

    def obtener(
        self,
        id_factura: uuid.UUID,
    ) -> Factura | None:
        """
        Busca una factura por su ID.
        """

        consulta = select(Factura).where(Factura.id_factura == id_factura)

        return self.db.scalar(consulta)

    def obtener_por_pedido(
        self,
        id_pedido: uuid.UUID,
    ) -> Factura | None:
        """
        Busca la factura asociada a un pedido específico.
        """

        consulta = select(Factura).where(Factura.id_pedido == id_pedido)

        return self.db.scalar(consulta)

    def listar(self) -> list[Factura]:
        """
        Obtiene todas las facturas registradas.
        """

        consulta = select(Factura)

        return list(self.db.scalars(consulta).all())

    def actualizar(
        self,
        id_factura: uuid.UUID,
        id_usuario_edicion: uuid.UUID,
        id_pedido: uuid.UUID | None = None,
        metodo_pago: str | None = None,
        total: float | None = None,
    ) -> Factura | None:
        """
        Actualiza los datos de una factura.
        """

        factura = self.obtener(id_factura)

        if factura is None:
            return None

        if id_pedido is not None:
            factura.id_pedido = id_pedido

        if metodo_pago is not None:
            factura.metodo_pago = metodo_pago.strip()

        if total is not None:
            factura.total = total

        factura.marcar_editado(id_usuario_edicion)

        self.db.commit()
        self.db.refresh(factura)

        return factura

    def eliminar(
        self,
        id_factura: uuid.UUID,
    ) -> bool:
        """
        Elimina una factura por su ID.
        """

        factura = self.obtener(id_factura)

        if factura is None:
            return False

        self.db.delete(factura)
        self.db.commit()

        return True
