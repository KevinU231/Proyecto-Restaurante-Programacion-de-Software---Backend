import uuid

from sqlalchemy.orm import Session

from src.entities.empleado import Empleado
from src.entities.usuario import Usuario
from src.entities.cliente import Cliente
from src.entities.mesa import Mesa
from src.entities.Pedido import Pedido
from src.entities.Detalle_pedido import DetallePedido
from src.entities.Factura import Factura
from src.entities.reserva import Reserva


def ejecutar_seeds(db: Session) -> None:
    """
    Crea datos iniciales de prueba para las entidades
    que actualmente están configuradas como modelos
    de SQLAlchemy.

    Los datos se crean respetando las relaciones
    entre las entidades.
    """

    # EMPLEADO

    empleado = db.query(Empleado).first()

    if empleado is None:
        empleado = Empleado(
            nombre="Carlos Rodríguez",
            telefono="3001234567",
            correo="carlos@restaurante.com",
            cargo="Mesero",
            id_usuario_creacion=None,
        )

        db.add(empleado)
        db.commit()
        db.refresh(empleado)

    print(f"Empleado seed: {empleado.id_empleado}")

    # USUARIO

    usuario = db.query(Usuario).first()

    if usuario is None:
        usuario = Usuario(
            id_empleado=empleado.id_empleado,
            nombre_usuario="mesero1",
            primer_nombre="Carlos",
            segundo_nombre="",
            primer_apellido="Rodríguez",
            segundo_apellido="",
            clave="123456",
            id_usuario_creacion=None,
        )

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

    print(f"Usuario seed: {usuario.id_usuario}")

    # CLIENTE

    cliente = db.query(Cliente).first()

    if cliente is None:
        cliente = Cliente(
            nombre="Juan Pérez",
            telefono="3109876543",
            correo="juan@gmail.com",
            direccion="Calle 50 # 40-20",
            id_usuario_creacion=usuario.id_usuario,
        )

        db.add(cliente)
        db.commit()
        db.refresh(cliente)

    print(f"Cliente seed: {cliente.id_cliente}")

    # MESA

    mesa = db.query(Mesa).first()

    if mesa is None:
        mesa = Mesa(
            numero=1,
            capacidad=4,
            estado="libre",
            id_usuario_creacion=usuario.id_usuario,
        )

        db.add(mesa)
        db.commit()
        db.refresh(mesa)

    print(f"Mesa seed: {mesa.id_mesa}")

    # PEDIDO

    pedido = db.query(Pedido).first()

    if pedido is None:
        pedido = Pedido(
            id_empleado=empleado.id_empleado,
            id_cliente=cliente.id_cliente,
            id_mesa=mesa.id_mesa,
            estado="pendiente",
            total=25000,
            id_usuario_creacion=usuario.id_usuario,
        )

        db.add(pedido)
        db.commit()
        db.refresh(pedido)

    print(f"Pedido seed: {pedido.id_pedido}")

    # RESERVA

    reserva = db.query(Reserva).first()

    if reserva is None:
        reserva = Reserva(
            id_cliente=cliente.id_cliente,
            id_mesa=mesa.id_mesa,
            fecha="2026-09-15",
            hora="19:00",
            num_personas=4,
            estado="confirmada",
            id_usuario_creacion=usuario.id_usuario,
        )

        db.add(reserva)
        db.commit()
        db.refresh(reserva)

    print(f"Reserva seed: {reserva.id_reserva}")

    # DETALLE DE PEDIDO

    print(
        "DetallePedido: pendiente hasta que la entidad Plato sea convertido "
        "queda pendiente hasta que la entidad Plato sea convertido a SQLAlchemy"
    )

    # FACTURA

    factura = db.query(Factura).first()

    if factura is None:
        factura = Factura(
            id_pedido=pedido.id_pedido,
            metodo_pago="efectivo",
            total=25000,
            id_usuario_creacion=usuario.id_usuario,
        )

        db.add(factura)
        db.commit()
        db.refresh(factura)

    print(f"Factura seed: {factura.id_factura}")

    print("\nSeeds ejecutados correctamente.")
