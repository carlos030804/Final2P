from pydantic import BaseModel, Field, EmailStr

class modelPelicula(BaseModel):
    id: int
    titulo: str = Field(..., min_length=2, max_length=255, description="Título de la película")
    genero: str = Field(..., min_length=4, description="Género de la película")
    ano: int = Field(..., gt=1900, lt=2100, description="Año de lanzamiento")
    clasificacion: str = Field(
        ..., 
        min_length=1, 
        max_length=1, 
        pattern="^[A-C]$",  
        description="Clasificación (A, B, C)"
    )

class modelAuth(BaseModel):
    mail: EmailStr
    passw: str = Field(..., min_length=8, description="Contraseña (mínimo 8 caracteres)")