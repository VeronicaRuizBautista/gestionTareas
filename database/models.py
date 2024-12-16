from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_FILE = "tasks.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"

db_exists = os.path.exists(DATABASE_FILE)

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tareas'
    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    estado = Column(String, nullable=False, default='pendiente')

if not db_exists:
    Base.metadata.create_all(engine)
    print(f"Base de datos creada en {DATABASE_FILE}")
else:
    print(f"Base de datos existente encontrada en {DATABASE_FILE}")