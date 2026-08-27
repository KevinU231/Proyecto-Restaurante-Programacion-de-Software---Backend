import uuid
from src.entities.empleado import Empleado


class EmpleadoCRUD:
    def __init__(self) -> None:
        # Lista donde se almacenan los empleados creados
        self.empleados: list[Empleado] = []

    def crear(
        self,
        nombre: str,
        telefono: str,
        correo: str,
        cargo: str,
        id_usuario_creacion: uuid.UUID,
    ) -> Empleado:
        """
        Crea un nuevo empleado y lo agrega a la lista.
        """
        empleado = Empleado(
            nombre=nombre,
            telefono=telefono,
            correo=correo,
            cargo=cargo,
            id_usuario_creacion=id_usuario_creacion,
        )

        self.empleados.append(empleado)
        return empleado

    def obtener(self, id_empleado: uuid.UUID) -> Empleado | None:
        """
        Busca un empleado por su ID.
        Retorna el empleado si existe; de lo contrario, retorna None.
        """
        for empleado in self.empleados:
            if empleado.id_empleado == id_empleado:
                return empleado

        return None

    def listar(self) -> list[Empleado]:
        """
        Retorna todos los empleados registrados.
        """
        return self.empleados

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
        Busca un empleado y actualiza únicamente los datos recibidos.
        También registra quién realizó la modificación.
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

        empleado.marcar_editado(id_usuario_edicion)

        return empleado

    def eliminar(self, id_empleado: uuid.UUID) -> bool:
        """
        Elimina un empleado por su ID.
        Retorna True si fue eliminado y False si no fue encontrado.
        """
        empleado = self.obtener(id_empleado)

        if empleado is None:
            return False

        self.empleados.remove(empleado)
        return True
