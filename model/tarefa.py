import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from sqlalchemy import String, DateTime
from model import Base

class Tarefa(Base):
    __tablename__ = 'tarefas'

    id: Mapped[int] = mapped_column(primary_key=True)
    descricao: Mapped[str] = mapped_column(String(128), unique=True)
    data_inicio: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), nullable=True)
    data_conclusao: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), nullable=True)

    def __init__(self, descricao):
        self.descricao = descricao
        
        