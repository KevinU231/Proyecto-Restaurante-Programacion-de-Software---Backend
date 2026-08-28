import uuid
from datetime import datetime

# Agregamos Optional ya que algunos atributos pueden
# ser del tipo indicado o pueden ser None
from typing import Optional


class Usuario:
    def __init__(
        self,
        nombre_usuario: str,
        primer_nombre: str,
        segundo_nombre: str,
        primer_apellido: str,
        segundo_apellido: str,
        clave: str,
        id_empleado: uuid.UUID,
        id_usuario_creacion: Optional[uuid.UUID] = None,
    ) -> None:
        self.id_usuario: uuid.UUID = uuid.uuid4()
        self.nombre_usuario = nombre_usuario.strip()
        self.primer_nombre = primer_nombre.strip()
        self.segundo_nombre = segundo_nombre.strip()
        self.primer_apellido = primer_apellido.strip()
        self.segundo_apellido = segundo_apellido.strip()
        self.clave = clave
        self.id_empleado = id_empleado

        # id usuario creacion puede ser None solo para el usuario que
        # arranca el sistema ya que nadie existia todavia para haberlo creado
        self.id_usuario_creacion: Optional[uuid.UUID] = id_usuario_creacion
        self.fecha_creacion: datetime = datetime.now()
        # Al crear el objeto todavia nadie lo ha editado, por eso estos
        # dos valores arrancan en None y el Optional permite que arranque
        # vacio y se llene despues de editarse
        self.fecha_edicion: Optional[datetime] = None
        self.id_usuario_edicion: Optional[uuid.UUID] = None

    # Metodo que recoge los nombres y apellidos del
    # usuario en una lista y los une
    def nombre_completo(self) -> str:
        partes = [
            self.primer_nombre,
            self.segundo_nombre,
            self.primer_apellido,
            self.segundo_apellido,
        ]
        return " ".join(parte for parte in partes if parte)

    # Metodo que se llama cada vez que alguien edita el registro, y actualiza
    # edito y cuando para dejar un rastro de lo editado
    def marcar_editado(self, id_usuario_edicion: uuid.UUID) -> None:
        self.id_usuario_edicion = id_usuario_edicion
        self.fecha_edicion = datetime.now()

    def __str__(self) -> str:
        return (
            f"Usuario({self.id_usuario}) - {self.nombre_completo()}"
            f" - {self.nombre_usuario}"
        )
