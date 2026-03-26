from fastapi import APIRouter
from api.repositories.queue_repository import get_queue

router = APIRouter()

@router.get("/queue")
def queue():

    data = get_queue()

    queue_with_position = []

    for i, item in enumerate(data):
        queue_with_position.append({
            "id_cola": item["id_cola"],
            "id_vehiculo": item["id_vehiculo"],
            "placa": item["vehiculos"]["placa"] if item.get("vehiculos") else None,
            "hora_llegada": item["hora_llegada"],
            "posicion": i + 1
        })

    return {
        "queue": queue_with_position,
        "total": len(queue_with_position)
    }
