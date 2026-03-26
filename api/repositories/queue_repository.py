from api.db.supabase_client import supabase

def enqueue_vehicle(vehicle_id: str, t_global: int):
    data = {
        "id_vehiculo": vehicle_id,
        "hora_llegada": t_global
    }

    response = supabase.table("cola").insert(data).execute()
    return response.data[0]


def get_queue():
    return (
        supabase.table("cola")
        .select("id_cola, hora_llegada, id_vehiculo, vehiculos(placa)")
        .order("hora_llegada", desc=False)
        .execute()
        .data
    )