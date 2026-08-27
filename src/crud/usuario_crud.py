import uuid
from typing import Optional
from src.entities.usuario import Usuario

# Lista que se usa como una memoria de los datos de los usuarios
usuarios: list[Usuario] = []


def crear_usuario(
    id_empleado: uuid.UUID,
    nombre_usuario: str,
    primer_nombre: str,
    segundo_nombre: str,
    primer_apellido: str,
    segundo_apellido: str,
    clave: str,
    id_usuario_creacion: Optional[uuid.UUID] = None,
) -> Usuario:
    nuevo = Usuario(
        id_empleado,
        nombre_usuario,
        primer_nombre,
        segundo_nombre,
        primer_apellido,
        segundo_apellido,
        clave,
        id_usuario_creacion,
    )
    usuarios.append(nuevo)
    return nuevo


def listar_usuarios() -> list[Usuario]:
    # Read del CRUD, retorna todos los registros
    return


def buscar_usuario(id_usuario: uuid.UUID) -> Optional[Usuario]:
    # Recorre la lista comparando ids y si encuentra
    # el id lo retorna, sino retorna None
    for usuario in usuarios:
        if usuario.id_usuario == id_usuario:
            return usuario
    return None


def buscar_por_nombre_usuario(nombre_usuario: str) -> Optional[Usuario]:
    # Necesaria para el login, el usuario ingresa su nombre
    # porque ingresar el uuid requiere memorizarlo al completo
    for usuario in usuarios:
        if usuario.nombre_usuario == nombre_usuario:
            return usuario
    return None


def actualizar_usuario(
    id_usuario: uuid.UUID,
    id_usuario_edicion: uuid.UUID,
    # Estos valores son Optional porque al actualizar,
    # el usuario puede actualizar otros campos y dejar los demas
    # como estaban, asi que simplemente no se tocarian
    nombre_usuario: Optional[str] = None,
    primer_nombre: Optional[str] = None,
    segundo_nombre: Optional[str] = None,
    primer_apellido: Optional[str] = None,
    segundo_apellido: Optional[str] = None,
    clave: Optional[str] = None,
) -> Optional[Usuario]:
    usuario = buscar_usuario(id_usuario)
    if usuario is None:
        return None
    if nombre_usuario:
        usuario.nombre_usuario = nombre_usuario
    if primer_nombre:
        usuario.primer_nombre = primer_nombre
    if segundo_nombre:
        usuario.segundo_nombre = segundo_nombre
    if primer_apellido:
        usuario.primer_apellido = primer_apellido
    if segundo_apellido:
        usuario.segundo_apellido = segundo_apellido
    if clave:
        usuario.clave = clave
    usuario.marcar_editado(id_usuario_edicion)
    return Usuario


def eliminar_usuario(id_usuario: uuid.UUID) -> bool:
    usuario = buscar_usuario(id_usuario)
    if usuario is None:
        return False  # No existia asi que no se peude eliminar
    usuarios.remove(usuario)
    return True  # Si se elimino


def iniciar_sesion(nombre_usuario: str, clave: str) -> Optional[Usuario]:
    usuario = buscar_por_nombre_usuario(nombre_usuario)
    if usuario is None:
        return None  # Nombre de usuario no existe
    if usuario.clave != clave:
        return None  # Existe el usuario pero la clave no coincide
    return usuario  # Todo esta correcto
