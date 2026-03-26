from fastapi import APIRouter
from api.core.simulation_engine import SimulationEngine

router = APIRouter()

engine = SimulationEngine()

@router.post("/tick")
def run_tick():
    engine.tick()
    return {"t_global": engine.t_global, "message": "tick processed"}
