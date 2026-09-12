"""
Seeder para las entidades: Plato, Menu, Inventario, Domicilio.

Este script llena las tablas con datos de ejemplo para poder probar
el CRUD y main.py sin necesidad de escribir todo manualmente.

IMPORTANTE:
- Los UUID de "usuario_admin_id" y "cliente_ejemplo_id" son FICTICIOS,
  ya que aun no existen usuarios ni clientes reales en la base de datos.
  Cuando el equipo tenga usuarios/clientes reales, se pueden reemplazar
  estos valores por los UUID reales.
- Ubica este archivo en la raiz del proyecto (o ajusta los imports segun
  donde lo coloques) y correlo con: python seed_restaurante.py
"""

import uuid
from src.database.connection import get_session, engine, Base

# Importamos los modelos para que SQLAlchemy los conozca
from src.entities.plato import Plato
from src.entities.menu import Menu
from src.entities.inventario import Inventario
from src.entities.domicilio import Domicilio


# --- UUIDs de ejemplo (ficticios, mientras no existan usuarios/clientes reales) ---
usuario_admin_id = uuid.uuid4()
cliente_ejemplo_id = uuid.uuid4()


def seed():
    session = get_session()

    try:
        # --- 1. Inventario (insumos) ---
        insumo_tomate = Inventario(
            nombre_insumo="Tomate",
            cantidad=50.0,
            unidad_medida="kg",
            id_usuario_creacion=usuario_admin_id,
        )
        insumo_queso = Inventario(
            nombre_insumo="Queso mozzarella",
            cantidad=20.0,
            unidad_medida="kg",
            id_usuario_creacion=usuario_admin_id,
        )
        insumo_pollo = Inventario(
            nombre_insumo="Pechuga de pollo",
            cantidad=30.0,
            unidad_medida="kg",
            id_usuario_creacion=usuario_admin_id,
        )

        session.add_all([insumo_tomate, insumo_queso, insumo_pollo])
        session.flush()  # para que ya tengan id antes de relacionarlos

        # --- 2. Platos (usando insumos) ---
        plato_pizza = Plato(
            nombre="Pizza margarita",
            precio=28000.0,
            descripcion="Pizza clasica con tomate y queso mozzarella",
            id_usuario_creacion=usuario_admin_id,
        )
        plato_pizza.insumos.extend([insumo_tomate, insumo_queso])

        plato_pollo = Plato(
            nombre="Pollo a la plancha",
            precio=32000.0,
            descripcion="Pechuga de pollo a la plancha con vegetales",
            id_usuario_creacion=usuario_admin_id,
        )
        plato_pollo.insumos.append(insumo_pollo)

        session.add_all([plato_pizza, plato_pollo])
        session.flush()

        # --- 3. Menu (usando platos) ---
        menu_almuerzo = Menu(
            nombre="Menu del dia",
            descripcion="Menu ejecutivo de almuerzo",
            id_usuario_creacion=usuario_admin_id,
        )
        menu_almuerzo.platos.extend([plato_pizza, plato_pollo])

        session.add(menu_almuerzo)
        session.flush()

        # --- 4. Domicilio (usando platos) ---
        domicilio_ejemplo = Domicilio(
            id_cliente=cliente_ejemplo_id,
            direccion_entrega="Calle 10 # 20-30, Medellin",
            estado="pendiente",
            id_usuario_creacion=usuario_admin_id,
        )
        domicilio_ejemplo.platos.append(plato_pizza)

        session.add(domicilio_ejemplo)

        # --- Confirmar todo ---
        session.commit()

        print("Seeder ejecutado con exito:")
        print(f"  - {insumo_tomate}")
        print(f"  - {insumo_queso}")
        print(f"  - {insumo_pollo}")
        print(f"  - {plato_pizza}")
        print(f"  - {plato_pollo}")
        print(f"  - {menu_almuerzo}")
        print(f"  - {domicilio_ejemplo}")

    except Exception as e:
        session.rollback()
        print(f"Error al ejecutar el seeder: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
