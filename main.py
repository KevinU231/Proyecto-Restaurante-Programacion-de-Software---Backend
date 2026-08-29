import uuid
from src.crud.empleado_crud import EmpleadoCRUD
from src.crud.Pedido_crud import PedidoCRUD
from src.crud.Detalle_Pedido_crud import DetallePedidoCRUD
from src.crud.Factura_crud import FacturaCRUD

from src.crud import usuario_crud, cliente_crud, mesa_crud, reserva_crud
from src.crud import plato_crud, menu_crud, inventario_crud, domicilio_crud

# INSTANCIAS DE LOS CRUD
empleado_crud = EmpleadoCRUD()
pedido_crud = PedidoCRUD()
detalle_crud = DetallePedidoCRUD()
factura_crud = FacturaCRUD()

usuario_actual = None


# solicita un UUID al usuario y verifica que sea válido
def obtener_uuid(mensaje):
    """
    Solicita un UUID al usuario y verifica que sea válido.
    """
    while True:
        try:
            return uuid.UUID(input(mensaje).strip())
        except ValueError:
            print("El ID ingresado no es válido.")


def cargar_datos_semilla():
    """
    Crea el primer empleado y usuario administrador del sistema.
    Rompe la dependencia circular: sin un usuario no hay login,
    y sin login no se puede crear un usuario. id_usuario_creacion
    queda en None solo aquí, porque nadie más existía todavía
    para haber creado este primer registro.
    """
    admin_empleado = empleado_crud.crear(
        nombre="Administrador",
        telefono="3000000000",
        correo="admin@restaurante.com",
        cargo="admin",
        id_usuario_creacion=None,
    )
    usuario_crud.crear_usuario(
        nombre_usuario="admin",
        primer_nombre="Administrador",
        segundo_nombre="",
        primer_apellido="Sistema",
        segundo_apellido="",
        clave="admin123",
        id_empleado=admin_empleado.id_empleado,
        id_usuario_creacion=None,
    )
    print("Datos semilla cargados. Usuario inicial -> usuario: admin | clave: admin123")


def pantalla_login():
    """
    Pide usuario y clave hasta que el login sea correcto.
    Guarda el usuario logueado en usuario_actual (variable global),
    que luego se usa automáticamente en todo el programa para las
    columnas de auditoría (id_usuario_creacion / id_usuario_edicion).
    """
    global usuario_actual
    print("\n=== SISTEMA DE GESTIÓN - RESTAURANTE ===")
    while usuario_actual is None:
        print("\n1. Iniciar sesión")
        print("2. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            nombre_usuario = input("Usuario: ").strip()
            clave = input("Clave: ").strip()
            encontrado = usuario_crud.iniciar_sesion(nombre_usuario, clave)
            if encontrado:
                usuario_actual = encontrado
                print(f"\nBienvenido, {encontrado.nombre_completo()}.")
            else:
                print("Usuario o clave incorrectos.")
        elif opcion == "2":
            print("Hasta pronto.")
            raise SystemExit
        else:
            print("Opción no válida.")


# EMPLEADOS
def crear_empleado():
    """
    Solicita los datos necesarios y crea un empleado.
    """
    print("\n--- CREAR EMPLEADO ---")

    nombre = input("Nombre: ")
    telefono = input("Teléfono: ")
    correo = input("Correo: ")
    cargo = input("Cargo: ")
    empleado = empleado_crud.crear(
        nombre=nombre,
        telefono=telefono,
        correo=correo,
        cargo=cargo,
        id_usuario_creacion=usuario_actual.id_usuario,
    )

    print("\nEmpleado creado correctamente.")
    print(empleado)


def listar_empleados():
    """
    Muestra todos los empleados registrados.
    """
    empleados = empleado_crud.listar()

    print("\n--- EMPLEADOS ---")

    if not empleados:
        print("No hay empleados registrados.")
        return

    for empleado in empleados:
        print(empleado)


def buscar_empleado():
    """
    Busca un empleado mediante su ID.
    """
    id_empleado = obtener_uuid("ID del empleado: ")

    empleado = empleado_crud.obtener(id_empleado)

    if empleado:
        print("\n--- EMPLEADO ENCONTRADO ---")
        print(empleado)
    else:
        print("\nEmpleado no encontrado.")


def actualizar_empleado():
    """
    Actualiza los datos de un empleado.
    """
    id_empleado = obtener_uuid("ID del empleado a actualizar: ")
    empleado = empleado_crud.obtener(id_empleado)
    if empleado is None:
        print("\nEmpleado no encontrado.")
        return
    print("\nDeje vacío un campo si no desea modificarlo.")
    nombre = input("Nuevo nombre: ").strip()
    telefono = input("Nuevo teléfono: ").strip()
    correo = input("Nuevo correo: ").strip()
    cargo = input("Nuevo cargo: ").strip()
    empleado = empleado_crud.actualizar(
        id_empleado=id_empleado,
        id_usuario_edicion=usuario_actual.id_usuario,
        nombre=nombre if nombre else None,
        telefono=telefono if telefono else None,
        correo=correo if correo else None,
        cargo=cargo if cargo else None,
    )
    print("\nEmpleado actualizado.")
    print(empleado)


def eliminar_empleado():
    """
    Elimina un empleado mediante su ID.
    """
    id_empleado = obtener_uuid("ID del empleado a eliminar: ")

    if empleado_crud.eliminar(id_empleado):
        print("\nEmpleado eliminado correctamente.")
    else:
        print("\nEmpleado no encontrado.")


# PEDIDOS
def crear_pedido():
    """
    Crea un pedido verificando que el empleado exista.
    """
    print("\n--- CREAR PEDIDO ---")

    id_empleado = obtener_uuid("ID del empleado que tomó el pedido: ")
    if empleado_crud.obtener(id_empleado) is None:
        print("\nEl empleado no existe.")
        return

    id_cliente = obtener_uuid("ID del cliente: ")
    if cliente_crud.buscar_cliente(id_cliente) is None:
        print("\nEl cliente no existe.")
        return

    es_domicilio = input("¿Es domicilio? (si/no): ").strip().lower()
    id_mesa = None
    if es_domicilio != "si":
        id_mesa = obtener_uuid("ID de la mesa: ")
        if mesa_crud.buscar_mesa(id_mesa) is None:
            print("\nLa mesa no existe.")
            return

    estado = input("Estado del pedido: ")
    total = float(input("Total del pedido: "))
    pedido = pedido_crud.crear(
        id_empleado=id_empleado,
        id_cliente=id_cliente,
        id_mesa=id_mesa,
        estado=estado,
        total=total,
        id_usuario_creacion=usuario_actual.id_usuario,
    )
    print("\nPedido creado correctamente.")
    print(pedido)


def listar_pedidos():
    """
    Muestra todos los pedidos registrados.
    """
    pedidos = pedido_crud.listar()

    print("\n--- PEDIDOS ---")

    if not pedidos:
        print("No hay pedidos registrados.")
        return

    for pedido in pedidos:
        print(pedido)


def buscar_pedido():
    """
    Busca un pedido mediante su ID.
    """
    id_pedido = obtener_uuid("ID del pedido: ")

    pedido = pedido_crud.obtener(id_pedido)

    if pedido:
        print("\n--- PEDIDO ENCONTRADO ---")
        print(pedido)
    else:
        print("\nPedido no encontrado.")


def actualizar_pedido():
    """
    Actualiza los datos de un pedido.
    """
    id_pedido = obtener_uuid("ID del pedido a actualizar: ")

    pedido = pedido_crud.obtener(id_pedido)

    if pedido is None:
        print("\nPedido no encontrado.")
        return
    print("\nDeje vacío un campo si no desea modificarlo.")

    estado = input("Nuevo estado: ").strip()
    total_texto = input("Nuevo total: ").strip()
    total = float(total_texto) if total_texto else None

    pedido = pedido_crud.actualizar(
        id_pedido=id_pedido,
        id_usuario_edicion=usuario_actual.id_usuario,
        estado=estado if estado else None,
        total=total,
    )
    print("\nPedido actualizado.")
    print(pedido)


def eliminar_pedido():
    """
    Elimina un pedido mediante su ID.
    """
    id_pedido = obtener_uuid("ID del pedido a eliminar: ")

    if pedido_crud.eliminar(id_pedido):
        print("\nPedido eliminado correctamente.")
    else:
        print("\nPedido no encontrado.")


# DETALLES DE PEDIDO
def crear_detalle():
    """
    Crea un detalle verificando que el pedido exista.
    """
    print("\n--- CREAR DETALLE DE PEDIDO ---")

    id_pedido = obtener_uuid("ID del pedido: ")

    if pedido_crud.obtener(id_pedido) is None:
        print("\nEl pedido no existe.")
        return
    id_producto = obtener_uuid("ID del producto: ")

    cantidad = int(input("Cantidad: "))
    precio_unitario = float(input("Precio unitario: "))

    detalle = detalle_crud.crear(
        id_pedido=id_pedido,
        id_producto=id_producto,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        id_usuario_creacion=usuario_actual.id_usuario,
    )

    print("\nDetalle creado correctamente.")
    print(detalle)


def listar_detalles():
    """
    Muestra todos los detalles de pedidos.
    """
    detalles = detalle_crud.listar()

    print("\n--- DETALLES DE PEDIDO ---")

    if not detalles:
        print("No hay detalles registrados.")
        return

    for detalle in detalles:
        print(detalle)


def buscar_detalle():
    """
    Busca un detalle de pedido mediante su ID.
    """
    id_detalle = obtener_uuid("ID del detalle: ")

    detalle = detalle_crud.obtener(id_detalle)

    if detalle:
        print("\n--- DETALLE ENCONTRADO ---")
        print(detalle)
    else:
        print("\nDetalle no encontrado.")


def listar_detalles_por_pedido():
    """
    Muestra todos los detalles pertenecientes a un pedido.
    """
    id_pedido = obtener_uuid("ID del pedido: ")

    detalles = detalle_crud.listar_por_pedido(id_pedido)

    print("\n--- DETALLES DEL PEDIDO ---")

    if not detalles:
        print("No hay detalles para este pedido.")
        return

    for detalle in detalles:
        print(detalle)


def actualizar_detalle():
    """
    Actualiza los datos de un detalle de pedido.
    """
    id_detalle = obtener_uuid("ID del detalle a actualizar: ")

    detalle = detalle_crud.obtener(id_detalle)

    if detalle is None:
        print("\nDetalle no encontrado.")
        return

    print("\nDeje vacío un campo si no desea modificarlo.")

    cantidad_texto = input("Nueva cantidad: ").strip()
    precio_texto = input("Nuevo precio unitario: ").strip()

    cantidad = int(cantidad_texto) if cantidad_texto else None

    precio_unitario = float(precio_texto) if precio_texto else None
    detalle = detalle_crud.actualizar(
        id_detalle_pedido=id_detalle,
        id_usuario_edicion=usuario_actual.id_usuario,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
    )

    print("\nDetalle actualizado.")
    print(detalle)


def eliminar_detalle():
    """
    Elimina un detalle de pedido mediante su ID.
    """
    id_detalle = obtener_uuid("ID del detalle a eliminar: ")

    if detalle_crud.eliminar(id_detalle):
        print("\nDetalle eliminado correctamente.")
    else:
        print("\nDetalle no encontrado.")


# FACTURAS
def crear_factura():
    """
    Crea una factura verificando que el pedido exista.
    """
    print("\n--- CREAR FACTURA ---")

    id_pedido = obtener_uuid("ID del pedido: ")

    if pedido_crud.obtener(id_pedido) is None:
        print("\nEl pedido no existe.")
        return
    metodo_pago = input("Método de pago: ")

    total = float(input("Total de la factura: "))
    factura = factura_crud.crear(
        id_pedido=id_pedido,
        metodo_pago=metodo_pago,
        total=total,
        id_usuario_creacion=usuario_actual.id_usuario,
    )

    print("\nFactura creada correctamente.")
    print(factura)


def listar_facturas():
    """
    Muestra todas las facturas registradas.
    """
    facturas = factura_crud.listar()

    print("\n--- FACTURAS ---")

    if not facturas:
        print("No hay facturas registradas.")
        return

    for factura in facturas:
        print(factura)


def buscar_factura():
    """
    Busca una factura mediante su ID.
    """
    id_factura = obtener_uuid("ID de la factura: ")

    factura = factura_crud.obtener(id_factura)

    if factura:
        print("\n--- FACTURA ENCONTRADA ---")
        print(factura)
    else:
        print("\nFactura no encontrada.")


def buscar_factura_por_pedido():
    """
    Busca la factura asociada a un pedido.
    """
    id_pedido = obtener_uuid("ID del pedido: ")

    factura = factura_crud.obtener_por_pedido(id_pedido)

    if factura:
        print("\n--- FACTURA DEL PEDIDO ---")
        print(factura)
    else:
        print("\nNo existe una factura para ese pedido.")


def actualizar_factura():
    """
    Actualiza los datos de una factura.
    """
    id_factura = obtener_uuid("ID de la factura a actualizar: ")

    factura = factura_crud.obtener(id_factura)
    if factura is None:
        print("\nFactura no encontrada.")
        return
    print("\nDeje vacío un campo si no desea modificarlo.")

    metodo_pago = input("Nuevo método de pago: ").strip()

    total_texto = input("Nuevo total: ").strip()

    total = float(total_texto) if total_texto else None

    factura = factura_crud.actualizar(
        id_factura=id_factura,
        id_usuario_edicion=usuario_actual.id_usuario,
        metodo_pago=(metodo_pago if metodo_pago else None),
        total=total,
    )
    print("\nFactura actualizada.")
    print(factura)


def eliminar_factura():
    """
    Elimina una factura mediante su ID.
    """
    id_factura = obtener_uuid("ID de la factura a eliminar: ")

    if factura_crud.eliminar(id_factura):
        print("\nFactura eliminada correctamente.")
    else:
        print("\nFactura no encontrada.")


# USUARIOS
def crear_usuario():
    print("\n--- CREAR USUARIO ---")
    nombre_usuario = input("Nombre de usuario: ").strip()
    primer_nombre = input("Primer nombre: ").strip()
    segundo_nombre = input("Segundo nombre (Enter si no tiene): ").strip()
    primer_apellido = input("Primer apellido: ").strip()
    segundo_apellido = input("Segundo apellido (Enter si no tiene): ").strip()
    clave = input("Clave: ").strip()
    id_empleado = obtener_uuid("ID del empleado dueño del usuario: ")
    usuario = usuario_crud.crear_usuario(
        nombre_usuario,
        primer_nombre,
        segundo_nombre,
        primer_apellido,
        segundo_apellido,
        clave,
        id_empleado,
        usuario_actual.id_usuario,
    )
    print("\nUsuario creado correctamente.")
    print(usuario)


def listar_usuarios():
    usuarios = usuario_crud.listar_usuarios()
    print("\n--- USUARIOS ---")
    if not usuarios:
        print("No hay usuarios registrados.")
        return
    for usuario in usuarios:
        print(usuario)


def buscar_usuario():
    id_usuario = obtener_uuid("ID del usuario: ")
    usuario = usuario_crud.buscar_usuario(id_usuario)
    if usuario:
        print("\n--- USUARIO ENCONTRADO ---")
        print(usuario)
    else:
        print("\nUsuario no encontrado.")


def actualizar_usuario():
    id_usuario = obtener_uuid("ID del usuario a actualizar: ")
    if usuario_crud.buscar_usuario(id_usuario) is None:
        print("\nUsuario no encontrado.")
        return
    print("\nDeje vacío un campo si no desea modificarlo.")
    primer_nombre = input("Nuevo primer nombre: ").strip()
    clave = input("Nueva clave: ").strip()
    usuario = usuario_crud.actualizar_usuario(
        id_usuario,
        usuario_actual.id_usuario,
        primer_nombre=primer_nombre if primer_nombre else None,
        clave=clave if clave else None,
    )
    print("\nUsuario actualizado.")
    print(usuario)


def eliminar_usuario():
    id_usuario = obtener_uuid("ID del usuario a eliminar: ")
    if usuario_crud.eliminar_usuario(id_usuario):
        print("\nUsuario eliminado correctamente.")
    else:
        print("\nUsuario no encontrado.")


# CLIENTES
def crear_cliente():
    print("\n--- CREAR CLIENTE ---")
    nombre = input("Nombre: ").strip()
    telefono = input("Teléfono: ").strip()
    correo = input("Correo: ").strip()
    direccion = input("Dirección: ").strip()
    cliente = cliente_crud.crear_cliente(
        nombre, telefono, correo, usuario_actual.id_usuario, direccion
    )
    print("\nCliente creado correctamente.")
    print(cliente)


def listar_clientes():
    clientes = cliente_crud.listar_clientes()
    print("\n--- CLIENTES ---")
    if not clientes:
        print("No hay clientes registrados.")
        return
    for cliente in clientes:
        print(cliente)


def buscar_cliente():
    id_cliente = obtener_uuid("ID del cliente: ")
    cliente = cliente_crud.buscar_cliente(id_cliente)
    if cliente:
        print("\n--- CLIENTE ENCONTRADO ---")
        print(cliente)
    else:
        print("\nCliente no encontrado.")


def actualizar_cliente():
    id_cliente = obtener_uuid("ID del cliente a actualizar: ")
    if cliente_crud.buscar_cliente(id_cliente) is None:
        print("\nCliente no encontrado.")
        return
    print("\nDeje vacío un campo si no desea modificarlo.")
    nombre = input("Nuevo nombre: ").strip()
    telefono = input("Nuevo teléfono: ").strip()
    cliente = cliente_crud.actualizar_cliente(
        id_cliente,
        usuario_actual.id_usuario,
        nombre if nombre else None,
        telefono if telefono else None,
    )
    print("\nCliente actualizado.")
    print(cliente)


def eliminar_cliente():
    id_cliente = obtener_uuid("ID del cliente a eliminar: ")
    if cliente_crud.eliminar_cliente(id_cliente):
        print("\nCliente eliminado correctamente.")
    else:
        print("\nCliente no encontrado.")


# MESAS
def crear_mesa():
    print("\n--- CREAR MESA ---")
    numero = int(input("Número de mesa: "))
    capacidad = int(input("Capacidad: "))
    mesa = mesa_crud.crear_mesa(numero, capacidad, usuario_actual.id_usuario)
    print("\nMesa creada correctamente.")
    print(mesa)


def listar_mesas():
    mesas = mesa_crud.listar_mesas()
    print("\n--- MESAS ---")
    if not mesas:
        print("No hay mesas registradas.")
        return
    for mesa in mesas:
        print(mesa)


def buscar_mesa():
    id_mesa = obtener_uuid("ID de la mesa: ")
    mesa = mesa_crud.buscar_mesa(id_mesa)
    if mesa:
        print("\n--- MESA ENCONTRADA ---")
        print(mesa)
    else:
        print("\nMesa no encontrada.")


def actualizar_mesa():
    id_mesa = obtener_uuid("ID de la mesa a actualizar: ")
    if mesa_crud.buscar_mesa(id_mesa) is None:
        print("\nMesa no encontrada.")
        return
    estado = input("Nuevo estado (libre/ocupada/reservada): ").strip()
    mesa = mesa_crud.actualizar_mesa(
        id_mesa, usuario_actual.id_usuario, estado=estado if estado else None
    )
    print("\nMesa actualizada.")
    print(mesa)


def eliminar_mesa():
    id_mesa = obtener_uuid("ID de la mesa a eliminar: ")
    if mesa_crud.eliminar_mesa(id_mesa):
        print("\nMesa eliminada correctamente.")
    else:
        print("\nMesa no encontrada.")


# RESERVAS
def crear_reserva():
    print("\n--- CREAR RESERVA ---")
    id_cliente = obtener_uuid("ID del cliente: ")
    id_mesa = obtener_uuid("ID de la mesa: ")
    fecha = input("Fecha (AAAA-MM-DD): ").strip()
    hora = input("Hora (HH:MM): ").strip()
    num_personas = int(input("Número de personas: "))
    reserva = reserva_crud.crear_reserva(
        id_cliente, id_mesa, fecha, hora, num_personas, usuario_actual.id_usuario
    )
    print("\nReserva creada correctamente.")
    print(reserva)


def listar_reservas():
    reservas = reserva_crud.listar_reservas()
    print("\n--- RESERVAS ---")
    if not reservas:
        print("No hay reservas registradas.")
        return
    for reserva in reservas:
        print(reserva)


def buscar_reserva():
    id_reserva = obtener_uuid("ID de la reserva: ")
    reserva = reserva_crud.buscar_reserva(id_reserva)
    if reserva:
        print("\n--- RESERVA ENCONTRADA ---")
        print(reserva)
    else:
        print("\nReserva no encontrada.")


def actualizar_reserva():
    id_reserva = obtener_uuid("ID de la reserva a actualizar: ")
    if reserva_crud.buscar_reserva(id_reserva) is None:
        print("\nReserva no encontrada.")
        return
    estado = input("Nuevo estado (confirmada/cancelada/cumplida): ").strip()
    reserva = reserva_crud.actualizar_reserva(
        id_reserva, usuario_actual.id_usuario, estado=estado if estado else None
    )
    print("\nReserva actualizada.")
    print(reserva)


def eliminar_reserva():
    id_reserva = obtener_uuid("ID de la reserva a eliminar: ")
    if reserva_crud.eliminar_reserva(id_reserva):
        print("\nReserva eliminada correctamente.")
    else:
        print("\nReserva no encontrada.")


# PLATOS
def crear_plato():
    print("\n--- CREAR PLATO ---")
    nombre = input("Nombre: ").strip()
    precio = float(input("Precio: "))
    descripcion = input("Descripción: ").strip()
    ids_texto = input("IDs de insumos usados (separados por coma, Enter si ninguno): ").strip()
    ids_insumos = [uuid.UUID(x.strip()) for x in ids_texto.split(",") if x.strip()]
    plato = plato_crud.crear_plato(
        nombre, precio, descripcion, ids_insumos, usuario_actual.id_usuario
    )
    print("\nPlato creado correctamente.")
    print(plato)


def listar_platos():
    platos = plato_crud.listar_platos()
    print("\n--- PLATOS ---")
    if not platos:
        print("No hay platos registrados.")
        return
    for plato in platos:
        print(plato)


def buscar_plato():
    id_plato = obtener_uuid("ID del plato: ")
    plato = plato_crud.buscar_plato(id_plato)
    if plato:
        print("\n--- PLATO ENCONTRADO ---")
        print(plato)
    else:
        print("\nPlato no encontrado.")


def actualizar_plato():
    id_plato = obtener_uuid("ID del plato a actualizar: ")
    if plato_crud.buscar_plato(id_plato) is None:
        print("\nPlato no encontrado.")
        return
    print("\nDeje vacío un campo si no desea modificarlo.")
    nombre = input("Nuevo nombre: ").strip()
    precio_texto = input("Nuevo precio: ").strip()
    precio = float(precio_texto) if precio_texto else None
    descripcion = input("Nueva descripción: ").strip()
    plato = plato_crud.actualizar_plato(
        id_plato,
        usuario_actual.id_usuario,
        nombre=nombre if nombre else None,
        precio=precio,
        descripcion=descripcion if descripcion else None,
    )
    print("\nPlato actualizado.")
    print(plato)


def eliminar_plato():
    id_plato = obtener_uuid("ID del plato a eliminar: ")
    if plato_crud.eliminar_plato(id_plato):
        print("\nPlato eliminado correctamente.")
    else:
        print("\nPlato no encontrado.")


# MENÚS
def crear_menu():
    print("\n--- CREAR MENÚ ---")
    nombre = input("Nombre: ").strip()
    ids_texto = input("IDs de platos que contiene (separados por coma): ").strip()
    ids_platos = [uuid.UUID(x.strip()) for x in ids_texto.split(",") if x.strip()]
    descripcion = input("Descripción (Enter si no tiene): ").strip()
    menu = menu_crud.crear_menu(
        nombre, ids_platos, usuario_actual.id_usuario, descripcion
    )
    print("\nMenú creado correctamente.")
    print(menu)


def listar_menus():
    menus = menu_crud.listar_menus()
    print("\n--- MENÚS ---")
    if not menus:
        print("No hay menús registrados.")
        return
    for menu in menus:
        print(menu)


def buscar_menu():
    id_menu = obtener_uuid("ID del menú: ")
    menu = menu_crud.buscar_menu(id_menu)
    if menu:
        print("\n--- MENÚ ENCONTRADO ---")
        print(menu)
    else:
        print("\nMenú no encontrado.")


def actualizar_menu():
    id_menu = obtener_uuid("ID del menú a actualizar: ")
    if menu_crud.buscar_menu(id_menu) is None:
        print("\nMenú no encontrado.")
        return
    print("\nDeje vacío un campo si no desea modificarlo.")
    nombre = input("Nuevo nombre: ").strip()
    descripcion = input("Nueva descripción: ").strip()
    menu = menu_crud.actualizar_menu(
        id_menu,
        usuario_actual.id_usuario,
        nombre=nombre if nombre else None,
        descripcion=descripcion if descripcion else None,
    )
    print("\nMenú actualizado.")
    print(menu)


def eliminar_menu():
    id_menu = obtener_uuid("ID del menú a eliminar: ")
    if menu_crud.eliminar_menu(id_menu):
        print("\nMenú eliminado correctamente.")
    else:
        print("\nMenú no encontrado.")


# INVENTARIO
def crear_inventario():
    print("\n--- CREAR INSUMO DE INVENTARIO ---")
    nombre_insumo = input("Nombre del insumo: ").strip()
    cantidad = float(input("Cantidad: "))
    unidad_medida = input("Unidad de medida: ").strip()
    insumo = inventario_crud.crear_inventario(
        nombre_insumo, cantidad, unidad_medida, usuario_actual.id_usuario
    )
    print("\nInsumo creado correctamente.")
    print(insumo)


def listar_inventarios():
    insumos = inventario_crud.listar_inventarios()
    print("\n--- INVENTARIO ---")
    if not insumos:
        print("No hay insumos registrados.")
        return
    for insumo in insumos:
        print(insumo)


def buscar_inventario():
    id_insumo = obtener_uuid("ID del insumo: ")
    insumo = inventario_crud.buscar_inventario(id_insumo)
    if insumo:
        print("\n--- INSUMO ENCONTRADO ---")
        print(insumo)
    else:
        print("\nInsumo no encontrado.")


def actualizar_inventario():
    id_insumo = obtener_uuid("ID del insumo a actualizar: ")
    if inventario_crud.buscar_inventario(id_insumo) is None:
        print("\nInsumo no encontrado.")
        return
    print("\nDeje vacío un campo si no desea modificarlo.")
    nombre_insumo = input("Nuevo nombre: ").strip()
    cantidad_texto = input("Nueva cantidad: ").strip()
    cantidad = float(cantidad_texto) if cantidad_texto else None
    unidad_medida = input("Nueva unidad de medida: ").strip()
    insumo = inventario_crud.actualizar_inventario(
        id_insumo,
        usuario_actual.id_usuario,
        nombre_insumo=nombre_insumo if nombre_insumo else None,
        cantidad=cantidad,
        unidad_medida=unidad_medida if unidad_medida else None,
    )
    print("\nInsumo actualizado.")
    print(insumo)


def eliminar_inventario():
    id_insumo = obtener_uuid("ID del insumo a eliminar: ")
    if inventario_crud.eliminar_inventario(id_insumo):
        print("\nInsumo eliminado correctamente.")
    else:
        print("\nInsumo no encontrado.")


# DOMICILIOS
def crear_domicilio():
    print("\n--- CREAR DOMICILIO ---")
    id_cliente = obtener_uuid("ID del cliente: ")
    if cliente_crud.buscar_cliente(id_cliente) is None:
        print("\nEl cliente no existe.")
        return
    direccion_entrega = input("Dirección de entrega: ").strip()
    ids_texto = input("IDs de platos pedidos (separados por coma): ").strip()
    ids_platos = [uuid.UUID(x.strip()) for x in ids_texto.split(",") if x.strip()]
    domicilio = domicilio_crud.crear_domicilio(
        id_cliente, direccion_entrega, ids_platos, usuario_actual.id_usuario
    )
    print("\nDomicilio creado correctamente.")
    print(domicilio)


def listar_domicilios():
    domicilios = domicilio_crud.listar_domicilios()
    print("\n--- DOMICILIOS ---")
    if not domicilios:
        print("No hay domicilios registrados.")
        return
    for domicilio in domicilios:
        print(domicilio)


def buscar_domicilio():
    id_domicilio = obtener_uuid("ID del domicilio: ")
    domicilio = domicilio_crud.buscar_domicilio(id_domicilio)
    if domicilio:
        print("\n--- DOMICILIO ENCONTRADO ---")
        print(domicilio)
    else:
        print("\nDomicilio no encontrado.")


def actualizar_domicilio():
    id_domicilio = obtener_uuid("ID del domicilio a actualizar: ")
    if domicilio_crud.buscar_domicilio(id_domicilio) is None:
        print("\nDomicilio no encontrado.")
        return
    print("\nDeje vacío un campo si no desea modificarlo.")
    direccion_entrega = input("Nueva dirección: ").strip()
    estado = input("Nuevo estado (pendiente/en_camino/entregado): ").strip()
    domicilio = domicilio_crud.actualizar_domicilio(
        id_domicilio,
        usuario_actual.id_usuario,
        direccion_entrega=direccion_entrega if direccion_entrega else None,
        estado=estado if estado else None,
    )
    print("\nDomicilio actualizado.")
    print(domicilio)


def eliminar_domicilio():
    id_domicilio = obtener_uuid("ID del domicilio a eliminar: ")
    if domicilio_crud.eliminar_domicilio(id_domicilio):
        print("\nDomicilio eliminado correctamente.")
    else:
        print("\nDomicilio no encontrado.")


# MENÚ PRINCIPAL
def menu_principal():
    """
    Muestra el menú principal y permite acceder
    a todas las operaciones del sistema.
    """
    while True:
        print("RESTAURANTE - MENÚ PRINCIPAL")
        print("\n              EMPLEADOS")
        print("1. Crear empleado")
        print("2. Listar empleados")
        print("3. Buscar empleado")
        print("4. Actualizar empleado")
        print("5. Eliminar empleado")
        print("\n              PEDIDOS")
        print("6. Crear pedido")
        print("7. Listar pedidos")
        print("8. Buscar pedido")
        print("9. Actualizar pedido")
        print("10. Eliminar pedido")
        print("\n         DETALLES DE PEDIDO")
        print("11. Crear detalle")
        print("12. Listar detalles")
        print("13. Buscar detalle")
        print("14. Listar detalles por pedido")
        print("15. Actualizar detalle")
        print("16. Eliminar detalle")
        print("\n              FACTURAS")
        print("17. Crear factura")
        print("18. Listar facturas")
        print("19. Buscar factura")
        print("20. Buscar factura por pedido")
        print("21. Actualizar factura")
        print("22. Eliminar factura")
        print("\n              USUARIOS")
        print("23. Crear usuario")
        print("24. Listar usuarios")
        print("25. Buscar usuario")
        print("26. Actualizar usuario")
        print("27. Eliminar usuario")
        print("\n              CLIENTES")
        print("28. Crear cliente")
        print("29. Listar clientes")
        print("30. Buscar cliente")
        print("31. Actualizar cliente")
        print("32. Eliminar cliente")
        print("\n              MESAS")
        print("33. Crear mesa")
        print("34. Listar mesas")
        print("35. Buscar mesa")
        print("36. Actualizar mesa")
        print("37. Eliminar mesa")
        print("\n              RESERVAS")
        print("38. Crear reserva")
        print("39. Listar reservas")
        print("40. Buscar reserva")
        print("41. Actualizar reserva")
        print("42. Eliminar reserva")
        print("\n              PLATOS")
        print("43. Crear plato")
        print("44. Listar platos")
        print("45. Buscar plato")
        print("46. Actualizar plato")
        print("47. Eliminar plato")
        print("\n              MENÚS")
        print("48. Crear menú")
        print("49. Listar menús")
        print("50. Buscar menú")
        print("51. Actualizar menú")
        print("52. Eliminar menú")
        print("\n              INVENTARIO")
        print("53. Crear insumo")
        print("54. Listar inventario")
        print("55. Buscar insumo")
        print("56. Actualizar insumo")
        print("57. Eliminar insumo")
        print("\n              DOMICILIOS")
        print("58. Crear domicilio")
        print("59. Listar domicilios")
        print("60. Buscar domicilio")
        print("61. Actualizar domicilio")
        print("62. Eliminar domicilio")
        print("\n0. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        acciones = {
            "1": crear_empleado,
            "2": listar_empleados,
            "3": buscar_empleado,
            "4": actualizar_empleado,
            "5": eliminar_empleado,
            "6": crear_pedido,
            "7": listar_pedidos,
            "8": buscar_pedido,
            "9": actualizar_pedido,
            "10": eliminar_pedido,
            "11": crear_detalle,
            "12": listar_detalles,
            "13": buscar_detalle,
            "14": listar_detalles_por_pedido,
            "15": actualizar_detalle,
            "16": eliminar_detalle,
            "17": crear_factura,
            "18": listar_facturas,
            "19": buscar_factura,
            "20": buscar_factura_por_pedido,
            "21": actualizar_factura,
            "22": eliminar_factura,
            "23": crear_usuario,
            "24": listar_usuarios,
            "25": buscar_usuario,
            "26": actualizar_usuario,
            "27": eliminar_usuario,
            "28": crear_cliente,
            "29": listar_clientes,
            "30": buscar_cliente,
            "31": actualizar_cliente,
            "32": eliminar_cliente,
            "33": crear_mesa,
            "34": listar_mesas,
            "35": buscar_mesa,
            "36": actualizar_mesa,
            "37": eliminar_mesa,
            "38": crear_reserva,
            "39": listar_reservas,
            "40": buscar_reserva,
            "41": actualizar_reserva,
            "42": eliminar_reserva,
            "43": crear_plato,
            "44": listar_platos,
            "45": buscar_plato,
            "46": actualizar_plato,
            "47": eliminar_plato,
            "48": crear_menu,
            "49": listar_menus,
            "50": buscar_menu,
            "51": actualizar_menu,
            "52": eliminar_menu,
            "53": crear_inventario,
            "54": listar_inventarios,
            "55": buscar_inventario,
            "56": actualizar_inventario,
            "57": eliminar_inventario,
            "58": crear_domicilio,
            "59": listar_domicilios,
            "60": buscar_domicilio,
            "61": actualizar_domicilio,
            "62": eliminar_domicilio,
        }

        if opcion == "0":
            print("\nPrograma finalizado.")
            break
        elif opcion in acciones:
            acciones[opcion]()
        else:
            print("\nOpción no válida.")


if __name__ == "__main__":
    cargar_datos_semilla()
    pantalla_login()
    menu_principal()