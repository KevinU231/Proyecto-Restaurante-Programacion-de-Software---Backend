import uuid
from typing import Optional
from src.entities.cliente import Cliente

clientes: list[Cliente] = []


def crear_cliente(
    nombre: str,
    telefono: str,
    correo: str,
    id_usuario_creacion: uuid.UUID,
    direccion: str = "",
) -> Cliente:
    nuevo = Cliente(nombre, telefono, correo, id_usuario_creacion, direccion)
    clientes.append(nuevo)
    return nuevo


def listar_clientes() -> list[Cliente]:
    return clientes


def buscar_cliente(id_cliente: uuid.UUID) -> Optional[Cliente]:
    for cliente in clientes:
        if cliente.id_cliente == id_cliente:
            return cliente
    return None


def actualizar_cliente(
    id_cliente: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    nombre: Optional[str] = None,
    telefono: Optional[str] = None,
    correo: Optional[str] = None,
    direccion: Optional[str] = None,
) -> Optional[Cliente]:
    cliente = buscar_cliente(id_cliente)
    if cliente is None:
        return None
    if nombre:
        cliente.nombre = nombre
    if telefono:
        cliente.telefono = telefono
    if correo:
        cliente.correo = correo
    if direccion:
        cliente.direccion = direccion
    cliente.marcar_editado(id_usuario_edicion)
    return cliente


def eliminar_cliente(id_cliente: uuid.UUID) -> bool:
    cliente = buscar_cliente(id_cliente)
    if cliente is None:
        return False
    clientes.remove(cliente)
    return True
