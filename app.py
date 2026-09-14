from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db, Producto, Venta
from schema import ProductoCreate, ProductoResponse, VentaCreate, VentaResponse

app = FastAPI(title="API Gestión de Ventas - UNLa")

# ==========================================
# ENDPOINTS PRODUCTOS
# ==========================================

@app.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@app.get("/productos", response_model=List[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@app.get("/productos/{id}", response_model=ProductoResponse)
def obtener_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@app.put("/productos/{id}", response_model=ProductoResponse)
def actualizar_producto(id: int, producto_data: ProductoCreate, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    producto.nombre = producto_data.nombre
    producto.precio = producto_data.precio
    
    db.commit()
    db.refresh(producto)
    return producto

@app.delete("/productos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(producto)
    db.commit()
    return None

# ==========================================
# ENDPOINTS VENTAS
# ==========================================

@app.post("/ventas", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(venta: VentaCreate, db: Session = Depends(get_db)):
    prod = db.query(Producto).filter(Producto.id == venta.id_producto).first()
    if not prod:
        raise HTTPException(status_code=400, detail="El producto especificado no existe")
    
    # El precio_total se calcula multiplicando el precio del producto por la cantidad
    total = prod.precio * venta.cantidad

    db_venta = Venta(
        fecha=venta.fecha,
        hora=venta.hora,
        id_producto=venta.id_producto,
        cantidad=venta.cantidad,
        precio_total=total
    )
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)
    return db_venta

@app.get("/ventas", response_model=List[VentaResponse])
def listar_ventas(db: Session = Depends(get_db)):
    return db.query(Venta).all()

@app.get("/ventas/{id}", response_model=VentaResponse)
def obtener_venta(id: int, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(Venta.id == id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@app.put("/ventas/{id}", response_model=VentaResponse)
def actualizar_venta(id: int, venta_data: VentaCreate, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(Venta.id == id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    prod = db.query(Producto).filter(Producto.id == venta_data.id_producto).first()
    if not prod:
        raise HTTPException(status_code=400, detail="El producto especificado no existe")

    venta.fecha = venta_data.fecha
    venta.hora = venta_data.hora
    venta.id_producto = venta_data.id_producto
    venta.cantidad = venta_data.cantidad
    venta.precio_total = prod.precio * venta_data.cantidad
    
    db.commit()
    db.refresh(venta)
    return venta

@app.delete("/ventas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_venta(id: int, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(Venta.id == id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    db.delete(venta)
    db.commit()
    return None