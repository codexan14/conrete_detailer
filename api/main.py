from fastapi import FastAPI
from pydantic import BaseModel
import math 

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: pon solo tu frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

class Entrada(BaseModel):
    base: float
    altura: float

@app.get("/")
async def root(number: int) -> dict[str, float]:
     return{"number": number**2}


@app.post("/producto")
async def func(entrada: Entrada) -> dict[str, float]:
     print(2)
     return {"resultado": entrada.base * entrada.altura}
