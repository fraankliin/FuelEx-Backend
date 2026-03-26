from sqlalchemy import Column, String, Integer, ForeignKey
from api.db.base import Base
import uuid

class Queue(Base):
    __tablename__ = "cola"

    id_cola = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    id_vehiculo = Column(String, ForeignKey("vehiculos.id_vehiculo"))
    hora_llegada = Column(Integer, nullable=False)
