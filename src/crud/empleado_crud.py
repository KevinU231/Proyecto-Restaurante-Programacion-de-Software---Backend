import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.empleado import Empleado


class EmpleadoCRUD:
    """
    CRUD para gestionar los empleados.

    CRUD significa:
    - Create: crear
    - Read: consultar
    - Update: actualizar
    - Delete: eliminar
    """

    def __init__(self, db: Session) -> None:
        """
        Recibe una sesión de SQLAlchemy.

        Esta sesión permite realizar operaciones
        directamente sobre la base de datos.
        """
        self.db = db

    def crear(
        self,
        nombre: str,
        telefono: str,
        correo: str,
        cargo: str,
        id_usuario_creacion: uuid.UUID | None,
    ) -> Empleado:
        """
        Crea un nuevo empleado y lo guarda en la base de datos.
        """

        empleado = Empleado(
            nombre=nombre,
            telefono=telefono,
            correo=correo,
            cargo=cargo,
            id_usuario_creacion=id_usuario_creacion,
        )

        # Agrega el empleado a la sesión.
        self.db.add(empleado)

        # Guarda los cambios en la base de datos.
        self.db.commit()

        # Actualiza el objeto con los datos generados por la BD.
        self.db.refresh(empleado)

        return empleado

    def obtener(
        self,
        id_empleado: uuid.UUID,
    ) -> Empleado | None:
        """
        Busca un empleado por su ID.

        Retorna el empleado si existe.
        Si no existe, retorna None.
        """

        consulta = select(Empleado).where(Empleado.id_empleado == id_empleado)

        return self.db.scalar(consulta)

    def listar(self) -> list[Empleado]:
        """
        Obtiene todos los empleados registrados
        en la base de datos.
        """

        consulta = select(Empleado)

        return list(self.db.scalars(consulta).all())

    def actualizar(
        self,
        id_empleado: uuid.UUID,
        id_usuario_edicion: uuid.UUID,
        nombre: str | None = None,
        telefono: str | None = None,
        correo: str | None = None,
        cargo: str | None = None,
    ) -> Empleado | None:
        """
        Busca un empleado y actualiza únicamente
        los datos que fueron enviados.
        """

        empleado = self.obtener(id_empleado)

        if empleado is None:
            return None

        if nombre is not None:
            empleado.nombre = nombre.strip()

        if telefono is not None:
            empleado.telefono = telefono.strip()

        if correo is not None:
            empleado.correo = correo.strip()

        if cargo is not None:
            empleado.cargo = cargo.strip()

        # Registra quién realizó la modificación.
        empleado.marcar_editado(id_usuario_edicion)

        # Guarda los cambios.
        self.db.commit()

        # Actualiza el objeto.
        self.db.refresh(empleado)

        return empleado

    def eliminar(
        self,
        id_empleado: uuid.UUID,
    ) -> bool:
        """
        Elimina un empleado por su ID.

        Retorna True si fue eliminado.
        Retorna False si no fue encontrado.
        """

        empleado = self.obtener(id_empleado)

        if empleado is None:
            return False

        self.db.delete(empleado)
        self.db.commit()

        return True
