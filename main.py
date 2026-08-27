import uuid
from src.crud.empleado_crud import EmpleadoCRUD
from src.crud.Pedido_crud import PedidoCRUD
from src.crud.Detalle_Pedido_crud import DetallePedidoCRUD
from src.crud.Factura_crud import FacturaCRUD

# INSTANCIAS DE LOS CRUD
empleado_crud = EmpleadoCRUD()
pedido_crud = PedidoCRUD()
detalle_crud = DetallePedidoCRUD()
factura_crud = FacturaCRUD()


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

    id_usuario = obtener_uuid("ID del usuario que crea el empleado: ")

    empleado = empleado_crud.crear(
        nombre=nombre,
        telefono=telefono,
        correo=correo,
        cargo=cargo,
        id_usuario_creacion=id_usuario,
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

    id_usuario = obtener_uuid("ID del usuario que realiza la edición: ")

    print("\nDeje vacío un campo si no desea modificarlo.")

    nombre = input("Nuevo nombre: ").strip()
    telefono = input("Nuevo teléfono: ").strip()
    correo = input("Nuevo correo: ").strip()
    cargo = input("Nuevo cargo: ").strip()

    empleado = empleado_crud.actualizar(
        id_empleado=id_empleado,
        id_usuario_edicion=id_usuario,
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

    estado = input("Estado del pedido: ")
    total = float(input("Total del pedido: "))

    id_usuario = obtener_uuid("ID del usuario que crea el pedido: ")

    pedido = pedido_crud.crear(
        id_empleado=id_empleado,
        estado=estado,
        total=total,
        id_usuario_creacion=id_usuario,
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

    id_usuario = obtener_uuid("ID del usuario que realiza la edición: ")

    print("\nDeje vacío un campo si no desea modificarlo.")

    estado = input("Nuevo estado: ").strip()
    total_texto = input("Nuevo total: ").strip()

    total = float(total_texto) if total_texto else None

    pedido = pedido_crud.actualizar(
        id_pedido=id_pedido,
        id_usuario_edicion=id_usuario,
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

    id_usuario = obtener_uuid("ID del usuario que crea el detalle: ")

    detalle = detalle_crud.crear(
        id_pedido=id_pedido,
        id_producto=id_producto,
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        id_usuario_creacion=id_usuario,
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

    id_usuario = obtener_uuid("ID del usuario que realiza la edición: ")

    print("\nDeje vacío un campo si no desea modificarlo.")

    cantidad_texto = input("Nueva cantidad: ").strip()
    precio_texto = input("Nuevo precio unitario: ").strip()

    cantidad = int(cantidad_texto) if cantidad_texto else None

    precio_unitario = float(precio_texto) if precio_texto else None

    detalle = detalle_crud.actualizar(
        id_detalle_pedido=id_detalle,
        id_usuario_edicion=id_usuario,
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

    id_usuario = obtener_uuid("ID del usuario que crea la factura: ")

    factura = factura_crud.crear(
        id_pedido=id_pedido,
        metodo_pago=metodo_pago,
        total=total,
        id_usuario_creacion=id_usuario,
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
    id_usuario = obtener_uuid("ID del usuario que realiza la edición: ")

    print("\nDeje vacío un campo si no desea modificarlo.")

    metodo_pago = input("Nuevo método de pago: ").strip()

    total_texto = input("Nuevo total: ").strip()

    total = float(total_texto) if total_texto else None

    factura = factura_crud.actualizar(
        id_factura=id_factura,
        id_usuario_edicion=id_usuario,
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

        print("\n0. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            crear_empleado()

        elif opcion == "2":
            listar_empleados()

        elif opcion == "3":
            buscar_empleado()

        elif opcion == "4":
            actualizar_empleado()

        elif opcion == "5":
            eliminar_empleado()

        elif opcion == "6":
            crear_pedido()

        elif opcion == "7":
            listar_pedidos()

        elif opcion == "8":
            buscar_pedido()

        elif opcion == "9":
            actualizar_pedido()

        elif opcion == "10":
            eliminar_pedido()

        elif opcion == "11":
            crear_detalle()

        elif opcion == "12":
            listar_detalles()

        elif opcion == "13":
            buscar_detalle()

        elif opcion == "14":
            listar_detalles_por_pedido()

        elif opcion == "15":
            actualizar_detalle()

        elif opcion == "16":
            eliminar_detalle()

        elif opcion == "17":
            crear_factura()

        elif opcion == "18":
            listar_facturas()

        elif opcion == "19":
            buscar_factura()

        elif opcion == "20":
            buscar_factura_por_pedido()

        elif opcion == "21":
            actualizar_factura()

        elif opcion == "22":
            eliminar_factura()

        elif opcion == "0":
            print("\nPrograma finalizado.")
            break

        else:
            print("\nOpción no válida.")


# EJECUCIÓN DEL PROGRAMA
if __name__ == "__main__":
    menu_principal()
