from fastapi import APIRouter
from api.services.vehicle_service import register_vehicle, get_all_vehicles

router = APIRouter()

t_global = 0


@router.post("/vehicles")
def create_vehicle_endpoint(data: dict):
    global t_global

    result = register_vehicle(data, t_global)

    return result



@router.get("/vehicles")
async def list_vehicles() -> list:
    return await get_all_vehicles()

