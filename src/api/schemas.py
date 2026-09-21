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
