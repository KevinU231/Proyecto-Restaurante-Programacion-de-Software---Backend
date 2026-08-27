import uuid
from src.entities.Factura import Factura


class FacturaCRUD:
    def __init__(self) -> None:
        # Lista donde se almacenan las facturas
        self.facturas: list[Factura] = []

    def crear(
        self,
        id_pedido: uuid.UUID,
        metodo_pago: str,
        total: float,
        id_usuario_creacion: uuid.UUID,
    ) -> Factura:
        """
        Crea una nueva factura y la agrega a la lista.
        """
        factura = Factura(
            id_pedido=id_pedido,
            metodo_pago=metodo_pago,
            total=total,
            id_usuario_creacion=id_usuario_creacion,
        )

        self.facturas.append(factura)
        return factura

    def obtener(self, id_factura: uuid.UUID) -> Factura | None:
        """
        Busca una factura por su ID.
        """
        for factura in self.facturas:
            if factura.id_factura == id_factura:
                return factura

        return None

    def obtener_por_pedido(
        self,
        id_pedido: uuid.UUID,
    ) -> Factura | None:
        """
        Busca la factura asociada a un pedido específico.
        """
        for factura in self.facturas:
            if factura.id_pedido == id_pedido:
                return factura

        return None

    def listar(self) -> list[Factura]:
        """
        Retorna todas las facturas registradas.
        """
        return self.facturas

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

        return factura

    def eliminar(self, id_factura: uuid.UUID) -> bool:
        """
        Elimina una factura por su ID.
        """
        factura = self.obtener(id_factura)

        if factura is None:
            return False

        self.facturas.remove(factura)
        return True
