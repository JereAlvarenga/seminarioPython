from pydantic import BaseModel
from datetime import date, time

# --- PRODUCTOS ---
class ProductoBase(BaseModel):
    nombre: str
    precio: float

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True

# --- VENTAS ---
class VentaCreate(BaseModel):
    fecha: date
    hora: time
    id_producto: int
    cantidad: int

class VentaResponse(BaseModel):
    id: int
    fecha: date
    hora: time
    producto: ProductoResponse
    cantidad: int
    precio_total: float

    class Config:
        from_attributes = True