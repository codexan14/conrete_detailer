from fastapi import FastAPI
import math 
app = FastAPI()

@app.get("/")
async def root(number: int) -> dict[str, float]:
     return{"number": number**2}