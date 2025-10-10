from datetime import datetime, timedelta, timezone
import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated, Optional
from jose import  JWTError, jwt

from app.schemas import TokenData
from . import models
from dotenv import load_dotenv
from passlib.context import CryptContext
load_dotenv()  # carga las variables de .env

SECRET_KEY = os.getenv("SECRET_KEY", "")
ALGORITHM = os.getenv("ALGORITHM", "")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
PEPPER = os.getenv("PEPPER", "")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth") # La URL debe coincidir con tu endpoint de login

# Configuración personalizada de Argon2
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__memory_cost=65536,    # 64 MB de RAM
    argon2__time_cost=3,          # 3 iteraciones
    argon2__parallelism=4         # 4 hilos (ajústalo al nº de cores)
)

def _apply_pepper(password: str, pepper: str | None) -> str:
    return password + pepper if pepper else password

def hash_password(password: str) -> str:
    peppered = _apply_pepper(password, PEPPER)
    return pwd_context.hash(peppered)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    peppered = _apply_pepper(plain_password, PEPPER)
    return pwd_context.verify(peppered, hashed_password)


# --- CRUD para Usuario (Usuario) ---

async def get_usuario(db: Session, usuario_id: int) -> Optional[models.Usuario]:
    """Obtiene un usuario por su ID."""
    return db.get(models.Usuario, usuario_id)

async def get_usuario_by_email(db: Session, email: str) -> Optional[models.Usuario]:
    """Obtiene un usuario por su correo electrónico."""
    stmt = select(models.Usuario).where(models.Usuario.email == email)
    return db.execute(stmt).scalars().first()

async def create_usuario(db: Session, user_data: dict) -> models.Usuario:
    """Crea un nuevo usuario."""
    # En FastAPI real, user_data sería un objeto Pydantic
    db_user = models.Usuario(**user_data) 
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def update_usuario(db: Session, usuario_id: int, update_data: dict) -> Optional[models.Usuario]:
    """Actualiza la información de un usuario."""
    db_user = db.get(models.Usuario, usuario_id)
    if db_user:
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

async def delete_usuario(db: Session, usuario_id: int) -> bool:
    """Elimina un usuario por su ID."""
    db_user = db.get(models.Usuario, usuario_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

#------------------------------------------------------------------
#-----Autenticación y manejo de contraseñas (hashing)-----
#------------------------------------------------------------------

def authenticate_user(db: Session, email: str, password: str):
    # Buscar usuario
    user = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if not user:
        return None
    # Verificar contraseña
    if not verify_password(password, user.hashed_password): # type: ignore
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    """
    Decodifica el token JWT y verifica su validez.
    Lanza HTTPException si el token es inválido o si faltan datos esenciales.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales no válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodificación del token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extracción del 'sub' (ID del usuario)
        user_id: str = payload.get("sub") # type: ignore
        if user_id is None:
            raise credentials_exception
        # Retorna el objeto TokenData con el ID extraído
        token_data = TokenData(sub=user_id)
    except JWTError:
        # Esto atrapa errores de firma (token inválido) o de expiración ('exp' vencido)
        raise credentials_exception
        
    return token_data

# ------------------------------------------------------------------
# --- CRUD para Receta (Receta) ---
# ------------------------------------------------------------------

async def get_receta(db: Session, receta_id: int) -> Optional[models.Receta]:
    """Obtiene una receta por su ID."""
    return db.get(models.Receta, receta_id)

from typing import Sequence
# Importa Receta si no lo has hecho
from . import models 

# ...

async def get_recetas_by_usuario(db: Session, usuario_id: int) -> Sequence[models.Receta]:
    """Obtiene todas las recetas creadas por un usuario."""
    stmt = select(models.Receta).where(models.Receta.usuario_id == usuario_id)
    # El resultado de .all() se anotará como Sequence[Receta]
    return db.execute(stmt).scalars().all()

async def create_receta(db: Session, receta_data: dict, usuario_id: int) -> models.Receta:
    """Crea una nueva receta asociada a un usuario."""
    db_receta = models.Receta(usuario_id=usuario_id, **receta_data)
    db.add(db_receta)
    db.commit()
    db.refresh(db_receta)
    return db_receta

async def update_receta(db: Session, receta_id: int, update_data: dict) -> Optional[models.Receta]:
    """Actualiza una receta por su ID."""
    db_receta = db.get(models.Receta, receta_id)
    if db_receta:
        # Nota: La clave foránea 'usuario_id' no debería cambiarse a menos que se reasigne la receta.
        for key, value in update_data.items():
            setattr(db_receta, key, value)
        db.commit()
        db.refresh(db_receta)
        return db_receta
    return None

async def delete_receta(db: Session, receta_id: int) -> bool:
    """Elimina una receta por su ID."""
    db_receta = db.get(models.Receta, receta_id)
    if db_receta:
        db.delete(db_receta)
        db.commit()
        return True
    return False

# ------------------------------------------------------------------
# --- CRUD para Menu Semanal (MenuSemanal) ---
# ------------------------------------------------------------------

async def get_menu_semanal(db: Session, menu_id: int) -> Optional[models.MenuSemanal]:
    """Obtiene un menú semanal por su ID."""
    # Esta función no carga las recetas asociadas, solo el objeto MenuSemanal principal.
    return db.get(models.MenuSemanal, menu_id)

async def create_menu_semanal(db: Session, menu_data: dict, usuario_id: int) -> models.MenuSemanal:
    """Crea un nuevo menú semanal."""
    db_menu = models.MenuSemanal(usuario_id=usuario_id, **menu_data)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

# (Funciones update_menu_semanal y delete_menu_semanal seguirían un patrón similar)