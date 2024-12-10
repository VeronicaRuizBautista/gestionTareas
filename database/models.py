from sqlalchemy import Column, Integer, String
from database import Base

class Task(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(String, nullable=False, default='pendiente')

