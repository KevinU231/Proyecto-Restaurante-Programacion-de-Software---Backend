from sqlalchemy.orm import Session

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


def ejecutar_seeds(db: Session) -> None:
    # EMPLEADO (bootstrap, todavía no existe ningún usuario)
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

    # INVENTARIO (insumos)
    insumo_tomate = db.query(Inventario).filter_by(nombre_insumo="Tomate").first()
    if insumo_tomate is None:
        insumo_tomate = Inventario(
            nombre_insumo="Tomate",
            cantidad=50.0,
            unidad_medida="kg",
            id_usuario_creacion=usuario.id_usuario,
        )
        db.add(insumo_tomate)

    insumo_queso = (
        db.query(Inventario).filter_by(nombre_insumo="Queso mozzarella").first()
    )
    if insumo_queso is None:
        insumo_queso = Inventario(
            nombre_insumo="Queso mozzarella",
            cantidad=20.0,
            unidad_medida="kg",
            id_usuario_creacion=usuario.id_usuario,
        )
        db.add(insumo_queso)

    db.commit()
    db.refresh(insumo_tomate)
    db.refresh(insumo_queso)
    print(f"Inventario seed: {insumo_tomate.id_insumo}, {insumo_queso.id_insumo}")

    # PLATO
    plato = db.query(Plato).filter_by(nombre="Pizza margarita").first()
    if plato is None:
        plato = Plato(
            nombre="Pizza margarita",
            precio=28000.0,
            descripcion="Pizza clásica con tomate y queso mozzarella",
            id_usuario_creacion=usuario.id_usuario,
        )
        plato.insumos.extend([insumo_tomate, insumo_queso])
        db.add(plato)
        db.commit()
        db.refresh(plato)
    print(f"Plato seed: {plato.id_plato}")

    # MENU
    menu = db.query(Menu).filter_by(nombre="Menu del dia").first()
    if menu is None:
        menu = Menu(
            nombre="Menu del dia",
            descripcion="Menú ejecutivo de almuerzo",
            id_usuario_creacion=usuario.id_usuario,
        )
        menu.platos.append(plato)
        db.add(menu)
        db.commit()
        db.refresh(menu)
    print(f"Menu seed: {menu.id_menu}")

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

    # DETALLE DE PEDIDO
    detalle = db.query(DetallePedido).first()
    if detalle is None:
        detalle = DetallePedido(
            id_pedido=pedido.id_pedido,
            id_plato=plato.id_plato,
            cantidad=1,
            precio_unitario=28000.0,
            id_usuario_creacion=usuario.id_usuario,
        )
        db.add(detalle)
        db.commit()
        db.refresh(detalle)
    print(f"DetallePedido seed: {detalle.id_detalle_pedido}")

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

    # DOMICILIO
    domicilio = db.query(Domicilio).first()
    if domicilio is None:
        domicilio = Domicilio(
            id_cliente=cliente.id_cliente,
            direccion_entrega="Calle 10 # 20-30, Medellín",
            estado="pendiente",
            id_usuario_creacion=usuario.id_usuario,
        )
        domicilio.platos.append(plato)
        db.add(domicilio)
        db.commit()
        db.refresh(domicilio)
    print(f"Domicilio seed: {domicilio.id_domicilio}")

    print("\nSeeds ejecutados correctamente.")
