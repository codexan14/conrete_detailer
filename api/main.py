from fastapi import FastAPI
from pydantic import BaseModel
from core.flexural import *

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción: pon solo tu frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

class TrialInput(BaseModel):
    base: float
    height: float

@app.get("/")
async def root(number: int) -> dict[str, float]:
     return{"number": number**2}


@app.post("/producto")
async def func(input: TrialInput) -> dict[str, float]:
     print(2)
     return {"resultado": input.base * input.height}


class FlexuralInput(BaseModel):
    base: float
    steel_area: float
    rebar_centroid: float
    concrete_compression_strength: float
    steel_yield_stress:float 

@app.post("/get_reduced_nominal_moment_beam_no_compression_reinforcement")
async def get_reduced_nominal_moment_beam_no_compression_reinforcement_endpoint(input: FlexuralInput):
     result = get_reduced_nominal_moment_beam_no_compression_reinforcement(
          base=input.base, 
          steel_area=input.steel_area, 
          rebar_centroid=input.rebar_centroid,
          concrete_compression_strength=input.concrete_compression_strength,
          steel_yield_stress=input.steel_yield_stress
     )

     return {"result": result}