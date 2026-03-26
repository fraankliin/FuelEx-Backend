from api.db.supabase_client import supabase


def get_free_pump():
    response = supabase.table("bombas") \
        .select("*") \
        .eq("estado", "libre") \
        .limit(1) \
        .execute()

    if response.data:
        return response.data[0]
    return None


def assign_vehicle_to_pump(pump_id: str, vehicle_id: str, tiempo_servicio: int):
    data = {
        "estado": "ocupada",
        "id_vehiculo_actual": vehicle_id,
        "tiempo_restante": tiempo_servicio
    }

    supabase.table("bombas") \
        .update(data) \
        .eq("id_bomba", pump_id) \
        .execute()


def get_pumps():
    return (
        supabase.table("bombas")
        .select("""
            id_bomba,
            estado,
            velocidad_litro_seg,
            tiempo_restante,
            id_vehiculo_actual,
            vehiculos (placa)
        """)
        .execute()
        .data
    )


def get_pumps_active_transaction():
    # bombas ocupadas
    return (
        supabase.table("bombas")
        .select("*")
        .eq("estado", "ocupada")
        .execute()
        .data
    )
