from sqlalchemy import Column, String, Numeric
from api.db.base import Base
import uuid

class Vehicle(Base):
    __tablename__ = "vehiculos"

    id_vehiculo = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    placa = Column(String, unique=True, nullable=False)
    capacidad_tanque = Column(Numeric, nullable=False)
    nivel_actual = Column(Numeric, nullable=False)
    tiempo_servicio = Column(Numeric, nullable=False)
