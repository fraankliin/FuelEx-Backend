from fastapi import APIRouter
from api.repositories.pump_repository import get_pumps
from api.repositories.transaction_repository import get_active_transactions

router = APIRouter()

@router.get("/pumps")
def pumps():

    bombas = get_pumps()
    transacciones = get_active_transactions()

    tx_by_bomba = {
        tx["id_bomba"]: tx for tx in transacciones
    }

    result = []

    for b in bombas:

        placa = None
        if b.get("vehiculos"):
            placa = b["vehiculos"]["placa"]

        bomba_data = {
            "id_bomba": b["id_bomba"],
            "estado": b["estado"],
            "velocidad_litro_seg": b["velocidad_litro_seg"],
            "tiempo_restante": b["tiempo_restante"],
            "id_vehiculo_actual": b["id_vehiculo_actual"],
            "placa": placa
        }

        result.append(bomba_data)

    return {
        "pumps": result
    }
