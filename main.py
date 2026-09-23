from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.usuarios import usuarios_router
from src.api.clientes import clientes_router
from src.api.mesas import mesas_router
from src.api.reservas import reservas_router
from src.api.empleados import empleados_router
from src.api.pedidos import pedidos_router
from src.api.detalle_pedidos import detalles_pedido_router
from src.api.facturas import facturas_router

app = FastAPI(
    title="API Restaurante - Programacion de Software",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router)
app.include_router(clientes_router)
app.include_router(mesas_router)
app.include_router(reservas_router)
app.include_router(empleados_router)
app.include_router(pedidos_router)
app.include_router(detalles_pedido_router)
app.include_router(facturas_router)


@app.get("/")
def raiz():
    return {"mensaje": "API en marcha"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
