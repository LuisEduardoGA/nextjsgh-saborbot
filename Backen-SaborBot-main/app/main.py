# app/main.py
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from app import crud, schemas
from app.database import get_db
from app.bedrock_client import invoke_bedrock, generate_image_with_titan
from starlette.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse # Para devolver errores personalizados
from sqlalchemy.orm import Session
from typing import List
from dotenv import load_dotenv
from app.crud import verify_token
from starlette.middleware.cors import CORSMiddleware

load_dotenv()  # carga las variables de .env
app = FastAPI(title="AWS Nova & Titan Chef Bot API")

# --- Configuración CORS ---
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,             # Permite cookies de origen cruzado
    allow_methods=["*"],                # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],                # Permite todos los headers, incluyendo Content-Type y Authorization
)


### --- Endpoints de Chat e Imagenes con Bedrock y Titan ---
@app.post("/chat", response_model=schemas.ChatResponse)
async def chat(req: schemas.ChatRequest, db: Session = Depends(get_db), token: schemas.TokenData = Depends(verify_token)):
    user_message = req.message
    user_id = int(token.sub) # type: ignore
    print(f"Usuario autenticado ID: {user_id}")
    nova_response_text = await run_in_threadpool(
        invoke_bedrock,
        prompt=user_message
    )
    create_receta = await crud.create_receta(
            db=db,
            receta_data={
                "titulo": f"Receta generada para: {user_message[:30]}...",
                "promt_usuario": user_message,
                "instrucciones": nova_response_text,
                "imagen_receta_base64": None
            },
            usuario_id=user_id
        )
    return schemas.ChatResponse(
        query=user_message,
        response=nova_response_text,
        id_receta=create_receta.id # type: ignore
    )

@app.post("/generate-image/{receta_id}", response_model=schemas.ImageResponse, )
async def generate_image(receta_id: int,  db: Session = Depends(get_db), token: schemas.TokenData = Depends(verify_token)):
    """
    Genera una imagen basada en el prompt del usuario utilizando Amazon Titan Image Generator.
    Devuelve la imagen en formato Base64.
    """
    receta = await crud.get_receta(db, receta_id)
    image_prompt = str(receta.promt_usuario) if (receta is not None and getattr(receta, "promt_usuario", None) is not None) else "Delicious food"
    # Llama a la función de generación de imágenes en un threadpool
    image_base64_data = await run_in_threadpool(
        generate_image_with_titan,
        prompt=image_prompt,
        width=1024,
        height=1024,
        quality='premium',
        output_image_path=None # Queremos los datos Base64 directamente # type: ignore
    )

    if "Error" in image_base64_data: # Si la función devuelve un mensaje de error
        return JSONResponse(status_code=500, content={"message": image_base64_data})
    
    await crud.update_receta(
            db=db,
            receta_id=receta_id,
            update_data={"imagen_receta_base64": image_base64_data}
        )
    return schemas.ImageResponse(
        image_base64=image_base64_data
    )

# app/main.py

@app.post("/auth", response_model=schemas.Authresponse)
async def login(form_data: schemas.Authrequest, db: Session = Depends(get_db)):
    # Los datos vienen en form_data.email y form_data.password
    user = crud.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Crear token JWT
    access_token = crud.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


### --- Endpoints de Usuarios (CRUD) ---
@app.post("/users/", response_model=schemas.UserOut, status_code=201)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario."""
    db_user = await crud.get_usuario_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    # Aquí deberías hashear la contraseña (usando bcrypt, por ejemplo)
    hashed_password = crud.hash_password(user.password)
    user_data = user.model_dump(exclude={"password"})
    user_data["hashed_password"] = hashed_password
    return await crud.create_usuario(db=db, user_data=user_data)

@app.get("/users/{user_id}", response_model=schemas.UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """Obtiene un usuario por ID."""
    db_user = await crud.get_usuario(db, usuario_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@app.get("/usersbymail/{email}", response_model=schemas.UserOut)
async def read_user_by_mail(email: str, db: Session = Depends(get_db)):
    """Obtiene un usuario por Email."""
    db_user = await crud.get_usuario_by_email(db, email=email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.UserUpdateResponse)
async def update_user( user_id: int,usuario_data: schemas.UsuarioUpdate,db: Session = Depends(get_db)):
    """Obtiene un usuario por Email."""
    updated_user = await crud.update_usuario(db, user_id, usuario_data.model_dump(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"msg": "Usuario actualizado correctamente", "usuario": {
        "id": updated_user.id,
        "nombre": updated_user.nombre,
        "apellido": updated_user.apellido,
        "email": updated_user.email
    }}

# --- Endpoints de Recetas (CRUD) ---


@app.get("/recetasbyuser", response_model=List[schemas.RecetaOut])
async def read_recipes_for_user(db: Session = Depends(get_db), token: schemas.TokenData = Depends(verify_token)):
    """Obtiene todas las recetas de un usuario."""
    user_id = int(token.sub) # type: ignore
    recetas = await crud.get_recetas_by_usuario(db, usuario_id=user_id)
    return recetas

@app.delete("/recipes/{receta_id}", status_code=204)
async def delete_recipe(receta_id: int, db: Session = Depends(get_db)):
    """Elimina una receta por ID."""
    success = await crud.delete_receta(db, receta_id=receta_id)
    if not success:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return {"message": "Receta eliminada correctamente"}




@app.get("/")
async def read_root():
    return {"message": "Welcome to the AWS Nova & Titan Chef Bot API. Use POST /chat or /generate-image."}