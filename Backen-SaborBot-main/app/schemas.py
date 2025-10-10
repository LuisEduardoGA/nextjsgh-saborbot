# app/schemas.py
from pydantic import BaseModel

from pydantic import BaseModel
from typing import Optional

# --- Esquemas para Usuario ---
class UserBase(BaseModel):
    nombre: str
    apellido: str
    email: str

class UserCreate(UserBase):
    # El campo de contraseña es necesario solo al crear
    password: str 

class UserOut(UserBase):
    id: int
    # No exponemos la contraseña hasheada
    class Config:
        from_attributes = True # Alias de orm_mode=True (para compatibilidad con ORM)

class UserUpdateResponse(BaseModel):
    msg: str
    usuario: UserOut
# --- Esquemas para Receta ---
class RecetaBase(BaseModel):
    titulo: str
    promt_usuario: Optional[str] = None
    instrucciones: str
    imagen_receta_base64: Optional[str] = None

class RecetaCreate(RecetaBase):
    pass # Usa el mismo esquema base para crear

class RecetaOut(RecetaBase):
    id: int
    usuario_id: int
    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None

class Authrequest(BaseModel):
    email: str
    password: str

class Authresponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    query: str
    response: str
    id_receta:int
    
class ImageResponse(BaseModel):
    image_base64: str # Devuelve la imagen como una cadena Base64

class TokenData(BaseModel):
    # El campo 'sub' (subject) se usa típicamente para el ID del usuario.
    # Debe ser el mismo tipo que usaste al crear el token: data={"sub": str(user.id)}
    sub: Optional[str] = None 