from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, Time
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

    ventas = relationship("Venta", back_populates="producto")

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    id_producto = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_total = Column(Float, nullable=False)

    producto = relationship("Producto", back_populates="ventas")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()