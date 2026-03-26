from api.db.supabase_client import supabase

class SimulationEngine:
    def __init__(self):
        self.t_global = 0

    def tick(self):
        self.t_global += 1
        self._update_pumps()
        self._assign_from_queue()

    def _update_pumps(self):
        # restar 1 al tiempo_restante de bombas ocupadas
        bombas = supabase.table("bombas").select("*").eq("estado", "ocupada").execute().data
        for bomba in bombas:
            nuevo_tiempo = bomba["tiempo_restante"] - 1
            if nuevo_tiempo <= 0:
                # liberar bomba
                supabase.table("bombas").update({
                    "estado": "libre",
                    "tiempo_restante": 0,
                    "id_vehiculo_actual": None
                }).eq("id_bomba", bomba["id_bomba"]).execute()

                # actualizar transaccion con hora_fin y tiempo_espera
                trans = supabase.table("transacciones").select("*") .eq("id_bomba", bomba["id_bomba"]) .is_("hora_fin", None).execute().data

                if trans:
                    t = trans[0]
                    tiempo_espera = t["hora_inicio"] - bomba["hora_llegada"] if "hora_llegada" in bomba else 0
                    supabase.table("transacciones").update({
                        "hora_fin": self.t_global,
                        "tiempo_espera": tiempo_espera
                    }).eq("id_transaccion", t["id_transaccion"]).execute()
            else:
                supabase.table("bombas").update({
                    "tiempo_restante": nuevo_tiempo
                }).eq("id_bomba", bomba["id_bomba"]).execute()

    def _assign_from_queue(self):
        # si hay bombas libres y vehículos en cola
        bombas_libres = supabase.table("bombas").select("*").eq("estado", "libre").execute().data
        for bomba in bombas_libres:
            cola = supabase.table("cola").select("*").order("hora_llegada", desc=False).limit(1).execute().data
            if not cola:
                break
            vehiculo = supabase.table("vehiculos").select("*").eq("id_vehiculo", cola[0]["id_vehiculo"]).execute().data[0]

            # asignar vehículo a bomba
            supabase.table("bombas").update({
                "estado": "ocupada",
                "id_vehiculo_actual": vehiculo["id_vehiculo"],
                "tiempo_restante": vehiculo["tiempo_servicio"]
            }).eq("id_bomba", bomba["id_bomba"]).execute()

            # crear transaccion
            supabase.table("transacciones").insert({
                "id_vehiculo": vehiculo["id_vehiculo"],
                "id_bomba": bomba["id_bomba"],
                "litros_suministrados": vehiculo["capacidad_tanque"] - vehiculo["nivel_actual"],
                "hora_inicio": self.t_global,
                "tiempo_servicio": vehiculo["tiempo_servicio"]
            }).execute()

            # eliminar de cola
            supabase.table("cola").delete().eq("id_cola", cola[0]["id_cola"]).execute()

engine = SimulationEngine()