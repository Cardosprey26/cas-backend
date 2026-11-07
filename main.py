from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sympy as sp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalcRequest(BaseModel):
    expression: str
    variable: str = "x"
    operation: str  
    point: str = "0"

@app.get("/")
def read_root():
    return {"status": "CAS API activa"}

@app.post("/api/eval")
def evaluate(data: CalcRequest):
    try:
        x = sp.Symbol(data.variable)
        expr = sp.sympify(data.expression)
        
        if data.operation == "diff":
            res = sp.diff(expr, x)
        elif data.operation == "integrate":
            res = sp.integrate(expr, x)
        elif data.operation == "limit":
            pt = sp.sympify(data.point)
            res = sp.limit(expr, x, pt)
        else:
            res = sp.simplify(expr)
            
        return {"status": "ok", "latex_result": sp.latex(res)}
    except Exception as e:
        return {"status": "error", "message": str(e)}