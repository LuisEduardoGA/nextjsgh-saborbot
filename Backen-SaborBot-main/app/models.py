from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# --- Tabla de asociación Muchos a Muchos ---
receta_menu_semanal = Table(
    "recetamenusemanal",
    Base.metadata,
    Column("menu_semanal_id", Integer, ForeignKey("menusemanal.id"), primary_key=True),
    Column("receta_id", Integer, ForeignKey("receta.id"), primary_key=True),
)

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Relación 1: Usuario → Recetas
    recetas = relationship("Receta", back_populates="usuario")

    # Relación 2: Usuario → Menús Semanales
    menus_semanales = relationship("MenuSemanal", back_populates="usuario")


class Receta(Base):
    __tablename__ = "receta"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    promt_usuario = Column(Text, nullable=True)
    instrucciones = Column(Text, nullable=False)
    imagen_receta_base64 = Column(Text(length=2**32), nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="recetas")

    # Relación 3: Receta ↔ Menú Semanal (M:M)
    menus_asociados = relationship(
        "MenuSemanal",
        secondary=receta_menu_semanal,
        back_populates="recetas_asociadas"
    )

    # Relación 4: Receta ↔ Ingredientes faltantes
    ingredientes_faltantes = relationship("IngredienteFaltanteReceta", back_populates="receta")


class MenuSemanal(Base):
    __tablename__ = "menusemanal"
    id = Column(Integer, primary_key=True, index=True)
    fecha_inicio = Column(String(10), nullable=False)  # Formato YYYY-MM-DD
    fecha_fin = Column(String(10), nullable=False)
    descripcion = Column(Text, nullable=True)

    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    usuario = relationship("Usuario", back_populates="menus_semanales")

    # Relación 3: Menú Semanal ↔ Recetas (M:M)
    recetas_asociadas = relationship(
        "Receta",
        secondary=receta_menu_semanal,
        back_populates="menus_asociados"
    )


class IngredienteFaltanteReceta(Base):
    __tablename__ = "ingredientefaltantereceta"
    id = Column(Integer, primary_key=True, index=True)
    receta_id = Column(Integer, ForeignKey("receta.id"), nullable=False)
    ingrediente = Column(String(200), nullable=False)
    cantidad = Column(String(200), nullable=True)
    unidad_medida = Column(String(50), nullable=True)

    receta = relationship("Receta", back_populates="ingredientes_faltantes")
