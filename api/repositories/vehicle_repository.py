from api.db.supabase_client import supabase

def create_vehicle(vehicle_data: dict):
    response = supabase.table("vehiculos").insert(vehicle_data).execute()
    return response.data[0]

async def get_all() -> list:
    resultado = (
        supabase.table("vehiculos")
        .select("id_vehiculo, placa, capacidad_tanque, nivel_actual", "tiempo_servicio", "created_at")
        .order("id_vehiculo", desc=False)
        .execute()
    )
    return resultado.data or []