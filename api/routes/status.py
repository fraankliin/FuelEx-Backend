from fastapi import APIRouter
from api.db.supabase_client import supabase
from api.core.simulation_engine import engine
import time

cache = None
last_call = 0
router = APIRouter()

@router.get("/status")
def get_status():
    global cache, last_call

    if time.time() - last_call < 2:
        return cache

    bombas = supabase.table("bombas").select("*").execute().data
    cola = supabase.table("cola").select("*").order("hora_llegada").execute().data
    transacciones = supabase.table("transacciones").select("*").execute().data

    cache = {
        "t_global": engine.t_global,
        "bombas": bombas,
        "cola": cola,
        "transacciones": transacciones
    }

    last_call = time.time()

    return cache