from src.database.connection import Base, engine

from src.entities.empleado import Empleado
from src.entities.usuario import Usuario
from src.entities.cliente import Cliente
from src.entities.mesa import Mesa
from src.entities.reserva import Reserva
from src.entities.inventario import Inventario
from src.entities.plato import Plato
from src.entities.menu import Menu
from src.entities.Pedido import Pedido
from src.entities.Detalle_pedido import DetallePedido
from src.entities.Factura import Factura
from src.entities.domicilio import Domicilio


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas/verificadas correctamente en Neon.")


if __name__ == "__main__":
    init_db()
