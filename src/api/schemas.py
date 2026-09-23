from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


# USUARIO
class UsuarioCreate(BaseModel):
    nombre_usuario: str
    primer_nombre: str
    segundo_nombre: str = ""
    primer_apellido: str
    segundo_apellido: str = ""
    clave: str
    id_empleado: UUID
    id_usuario_creacion: Optional[UUID] = None


class UsuarioUpdate(BaseModel):
    id_usuario_edicion: UUID
    nombre_usuario: Optional[str] = None
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    clave: Optional[str] = None


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: UUID
    id_empleado: UUID
    nombre_usuario: str
    primer_nombre: str
    segundo_nombre: str
    primer_apellido: str
    segundo_apellido: str


class UsuarioLogin(BaseModel):
    nombre_usuario: str
    clave: str


class UsuarioPost(BaseModel):
    data: UsuarioRead
    status: int
    message: str


class UsuarioPut(BaseModel):
    data: UsuarioRead
    status: int
    message: str


class UsuarioList(BaseModel):
    data: List[UsuarioRead]
    status: int
    message: str


# CLIENTE
class ClienteCreate(BaseModel):
    nombre: str
    telefono: str
    correo: str = ""
    direccion: str = ""
    id_usuario_creacion: UUID


class ClienteUpdate(BaseModel):
    id_usuario_edicion: UUID
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None


class ClienteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_cliente: UUID
    nombre: str
    telefono: str
    correo: str
    direccion: str


class ClientePost(BaseModel):
    data: ClienteRead
    status: int
    message: str


class ClientePut(BaseModel):
    data: ClienteRead
    status: int
    message: str


class ClienteList(BaseModel):
    data: List[ClienteRead]
    status: int
    message: str


# MESA
class MesaCreate(BaseModel):
    numero: int
    capacidad: int
    estado: str = "libre"
    id_usuario_creacion: UUID


class MesaUpdate(BaseModel):
    id_usuario_edicion: UUID
    numero: Optional[int] = None
    capacidad: Optional[int] = None
    estado: Optional[str] = None


class MesaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_mesa: UUID
    numero: int
    capacidad: int
    estado: str


class MesaPost(BaseModel):
    data: MesaRead
    status: int
    message: str


class MesaPut(BaseModel):
    data: MesaRead
    status: int
    message: str


class MesaList(BaseModel):
    data: List[MesaRead]
    status: int
    message: str


# RESERVA
class ReservaCreate(BaseModel):
    id_cliente: UUID
    id_mesa: UUID
    fecha: str
    hora: str
    num_personas: int
    estado: str = "confirmada"
    id_usuario_creacion: UUID


class ReservaUpdate(BaseModel):
    id_usuario_edicion: UUID
    fecha: Optional[str] = None
    hora: Optional[str] = None
    num_personas: Optional[int] = None
    estado: Optional[str] = None


class ReservaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_reserva: UUID
    id_cliente: UUID
    id_mesa: UUID
    fecha: str
    hora: str
    num_personas: int
    estado: str


class ReservaPost(BaseModel):
    data: ReservaRead
    status: int
    message: str


class ReservaPut(BaseModel):
    data: ReservaRead
    status: int
    message: str


class ReservaList(BaseModel):
    data: List[ReservaRead]
    status: int
    message: str


# empleado
class EmpleadoCreate(BaseModel):
    nombre: str
    telefono: str
    correo: str
    cargo: str
    id_usuario_creacion: Optional[UUID] = None


class EmpleadoUpdate(BaseModel):
    id_usuario_edicion: UUID
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    cargo: Optional[str] = None


class EmpleadoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_empleado: UUID
    nombre: str
    telefono: str
    correo: str
    cargo: str


class EmpleadoPost(BaseModel):
    data: EmpleadoRead
    status: int
    message: str


class EmpleadoPut(BaseModel):
    data: EmpleadoRead
    status: int
    message: str


class EmpleadoList(BaseModel):
    data: List[EmpleadoRead]
    status: int
    message: str


# pedido
class PedidoCreate(BaseModel):
    id_empleado: UUID
    id_cliente: UUID
    id_mesa: Optional[UUID] = None
    estado: str
    total: float
    id_usuario_creacion: Optional[UUID] = None


class PedidoUpdate(BaseModel):
    id_usuario_edicion: UUID
    id_empleado: Optional[UUID] = None
    id_cliente: Optional[UUID] = None
    id_mesa: Optional[UUID] = None
    estado: Optional[str] = None
    total: Optional[float] = None


class PedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_pedido: UUID
    id_empleado: UUID
    id_cliente: UUID
    id_mesa: Optional[UUID]
    estado: str
    total: float


class PedidoPost(BaseModel):
    data: PedidoRead
    status: int
    message: str


class PedidoPut(BaseModel):
    data: PedidoRead
    status: int
    message: str


class PedidoList(BaseModel):
    data: List[PedidoRead]
    status: int
    message: str


# Detalle Pedido


class DetallePedidoCreate(BaseModel):
    id_pedido: UUID
    id_plato: UUID
    cantidad: int
    precio_unitario: float
    id_usuario_creacion: Optional[UUID] = None


class DetallePedidoUpdate(BaseModel):
    id_usuario_edicion: UUID
    id_pedido: Optional[UUID] = None
    id_plato: Optional[UUID] = None
    cantidad: Optional[int] = None
    precio_unitario: Optional[float] = None


class DetallePedidoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_detalle_pedido: UUID
    id_pedido: UUID
    id_plato: UUID
    cantidad: int
    precio_unitario: float
    subtotal: float


class DetallePedidoPost(BaseModel):
    data: DetallePedidoRead
    status: int
    message: str


class DetallePedidoPut(BaseModel):
    data: DetallePedidoRead
    status: int
    message: str


class DetallePedidoList(BaseModel):
    data: List[DetallePedidoRead]
    status: int
    message: str


# Factura


class FacturaCreate(BaseModel):
    id_pedido: UUID
    metodo_pago: str
    total: float
    id_usuario_creacion: Optional[UUID] = None


class FacturaUpdate(BaseModel):
    id_usuario_edicion: UUID
    id_pedido: Optional[UUID] = None
    metodo_pago: Optional[str] = None
    total: Optional[float] = None


class FacturaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_factura: UUID
    id_pedido: UUID
    metodo_pago: str
    total: float


class FacturaPost(BaseModel):
    data: FacturaRead
    status: int
    message: str


class FacturaPut(BaseModel):
    data: FacturaRead
    status: int
    message: str


class FacturaList(BaseModel):
    data: List[FacturaRead]
    status: int
    message: str
