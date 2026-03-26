from api.repositories.vehicle_repository import create_vehicle, get_all
from api.repositories.queue_repository import enqueue_vehicle
from api.repositories.pump_repository import get_free_pump, assign_vehicle_to_pump
from api.repositories.transaction_repository import create_transaction

TIEMPO_POR_LITRO = 1


def calcular_tiempo_servicio(capacidad, nivel_actual):
    litros = capacidad - nivel_actual
    return litros * TIEMPO_POR_LITRO, litros


def register_vehicle(data: dict, t_global: int):
    tiempo_servicio, litros = calcular_tiempo_servicio(
        data["capacidad_tanque"],
        data["nivel_actual"]
    )

    vehicle_data = {
        "placa": data["placa"],
        "capacidad_tanque": data["capacidad_tanque"],
        "nivel_actual": data["nivel_actual"],
        "tiempo_servicio": tiempo_servicio
    }

    vehicle = create_vehicle(vehicle_data)

    # 🔥 NUEVA LÓGICA
    pump = get_free_pump()

    if pump:
        # asignar directamente
        assign_vehicle_to_pump(
            pump["id_bomba"],
            vehicle["id_vehiculo"],
            tiempo_servicio
        )

        create_transaction(
            vehicle["id_vehiculo"],
            pump["id_bomba"],
            litros,
            t_global,
            tiempo_servicio
        )

        return {
            "status": "assigned",
            "vehicle": vehicle,
            "pump": pump["id_bomba"]
        }

    else:
        # enviar a cola
        enqueue_vehicle(vehicle["id_vehiculo"], t_global)

        return {
            "status": "queued",
            "vehicle": vehicle
        }


async def get_all_vehicles() :
    return await get_all()