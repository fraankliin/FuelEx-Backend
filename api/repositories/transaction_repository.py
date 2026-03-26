from api.db.supabase_client import supabase

def create_transaction(vehicle_id, pump_id, litros, t_global, tiempo_servicio):
    data = {
        "id_vehiculo": vehicle_id,
        "id_bomba": pump_id,
        "litros_suministrados": litros,
        "hora_inicio": t_global,
        "tiempo_servicio": tiempo_servicio
    }

    response = supabase.table("transacciones").insert(data).execute()
    return response.data[0]


def get_all_transactions():
    return (
        supabase.table("transacciones")
        .select("*")
        .order("hora_inicio", desc=True)
        .execute()
        .data
    )


def get_active_transactions():
    return (
        supabase.table("transacciones")
        .select("*")
        .is_("hora_fin", "null")
        .execute()
        .data
    )