from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from models import modelPelicula, modelAuth
from gentoken import createToken
from middlewares import BearerJWT

app = FastAPI(
    title="API de Películas",
    description="API para el registro y gestión de películas",
    version="1.0.1"
)

peliculas = [
    {"id": 1, "titulo": "Titanic", "genero": "Romance", "ano": 1997, "clasificacion": "B"},
    {"id": 2, "titulo": "Avatar", "genero": "Ciencia ficción", "ano": 2009, "clasificacion": "A"},
    {"id": 3, "titulo": "Avengers: Endgame", "genero": "Acción", "ano": 2019, "clasificacion": "A"},
]

@app.post('/auth', tags=['autenticacion'])
def auth(credenciales: modelAuth):
    if credenciales.mail == 'carlos@example.com' and credenciales.passw == '123456789':
        token = createToken(credenciales.dict())
        return JSONResponse(content={"token": token})
    raise HTTPException(status_code=403, detail="Usuario no autorizado")

@app.get('/peliculas', dependencies=[Depends(BearerJWT())], response_model=List[modelPelicula], tags=['CRUD'])
def get_peliculas():
    return peliculas

@app.get('/peliculas/{id}', response_model=modelPelicula, tags=['Operaciones CRUD'])
def consultar_pelicula(id: int):
    for pelicula in peliculas:
        if pelicula["id"] == id:
            return pelicula
    raise HTTPException(status_code=404, detail="Película no encontrada")

@app.post('/peliculas/', response_model=modelPelicula, tags=['Operaciones CRUD'])
def guardar_pelicula(pelicula: modelPelicula):
    nuevo_id = max([p["id"] for p in peliculas]) + 1 if peliculas else 1
    pelicula_dict = pelicula.dict()
    pelicula_dict["id"] = nuevo_id
    peliculas.append(pelicula_dict)
    return pelicula_dict

@app.put('/peliculas/{id}', response_model=modelPelicula, tags=['Operaciones CRUD'])
def editar_pelicula(id: int, pelicula_actualizada: modelPelicula):
    for index, pelicula in enumerate(peliculas):
        if pelicula["id"] == id:
            updated_data = pelicula_actualizada.model_dump(by_alias=True)
            updated_data["id"] = id  
            peliculas[index] = updated_data
            return updated_data
    raise HTTPException(status_code=404, detail="Película no encontrada")

@app.delete('/peliculas/{id}', dependencies=[Depends(BearerJWT())], tags=['Operaciones CRUD'])
def eliminar_pelicula(id: int):
    for index, pelicula in enumerate(peliculas):
        if pelicula["id"] == id:
            peliculas.pop(index)
            return {"mensaje": "Película eliminada exitosamente"}
    raise HTTPException(status_code=404, detail="Película no encontrada")

