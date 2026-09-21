from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    UsuarioCreate,
    UsuarioList,
    UsuarioLogin,
    UsuarioPost,
    UsuarioPut,
    UsuarioRead,
    UsuarioUpdate,
)
from src.crud import usuario_crud

usuarios_router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@usuarios_router.get("/", response_model=UsuarioList)
def listar_usuarios():
    usuarios = usuario_crud.listar_usuarios()
    if not usuarios:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="No se encontraron usuarios",
        )
    return {
        "data": usuarios,
        "status": HTTPStatus.OK.value,
        "message": "Usuarios encontrados",
    }


@usuarios_router.post("/login", response_model=UsuarioRead)
def iniciar_sesion(datos: UsuarioLogin):
    usuario = usuario_crud.iniciar_sesion(datos.nombre_usuario, datos.clave)
    if usuario is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED.value,
            detail="Nombre de usuario o clave incorrectos",
        )
    return usuario


@usuarios_router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(id_usuario: UUID):
    usuario = usuario_crud.buscar_usuario(id_usuario)
    if usuario is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Usuario no encontrado"
        )
    return usuario


@usuarios_router.post("/", response_model=UsuarioPost, status_code=201)
def crear_usuario(datos: UsuarioCreate):
    usuario = usuario_crud.crear_usuario(**datos.model_dump())
    return {
        "data": usuario,
        "status": HTTPStatus.CREATED.value,
        "message": f"Usuario {usuario.nombre_usuario} creado",
    }


@usuarios_router.put("/{id_usuario}", response_model=UsuarioPut)
def actualizar_usuario(id_usuario: UUID, datos: UsuarioUpdate):
    if usuario_crud.buscar_usuario(id_usuario) is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Usuario no encontrado"
        )
    usuario = usuario_crud.actualizar_usuario(
        id_usuario,
        datos.id_usuario_edicion,
        **datos.model_dump(exclude_unset=True, exclude={"id_usuario_edicion"}),
    )
    return {
        "data": usuario,
        "status": HTTPStatus.OK.value,
        "message": f"Usuario {usuario.nombre_usuario} actualizado",
    }


@usuarios_router.delete("/{id_usuario}", status_code=HTTPStatus.NO_CONTENT.value)
def eliminar_usuario(id_usuario: UUID):
    if not usuario_crud.eliminar_usuario(id_usuario):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND.value, detail="Usuario no encontrado"
        )
