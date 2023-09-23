from pydantic import BaseModel
from typing import List
from model.tarefa import Tarefa


class TarefaSchema(BaseModel):
    """ Define como uma nova tarefa deve ser representada
    """
    id: int = 1
    descricao: str = "Descricao da tarefa"
    data_inicio: str = "15/11/1889 01:01:01"
    data_conclusao: str = "15/11/1889 01:01:01"

class NovaTarefaSchema(BaseModel):
    """ Define como uma nova tarefa deve ser representada
    """
    descricao: str = "Descricao da tarefa"

class AtualizarTarefaSchema(BaseModel):
    """ Define como uma tarefa iniciada deve ser representada
    """
    id: int = 1

class TarefaBuscaDescricaoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por descricao.
    """
    descricao: str = "Tarefa teste"

class TarefaBuscaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca por id.
    """
    id: int = 1

class ListagemTarefasSchema(BaseModel):
    """ Define como uma listagem de tarefas será retornada.
    """
    tarefas:List[TarefaSchema]

def apresenta_tarefas(tarefas: List[Tarefa]):
    """ Retorna uma representação da tarefa seguindo o schema definido em
        TarefaViewSchema.
    """
    result = []
    for tarefa in tarefas:
        result.append({
            "id": tarefa.id,
            "descricao": tarefa.descricao,
            "data_inicio": tarefa.data_inicio,
            "data_conclusao": tarefa.data_conclusao
        })

    return {"tarefas": result}


class TarefaViewSchema(BaseModel):
    """ Define como uma tarefa será retornada.
    """
    id: int = 1
    descricao: str = "Tarefa exemplo"
    data_inicio: str = '15/11/1889 01:01:01'
    data_conclusao: str = '15/11/1889 07:30:15'
    

class TarefaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int

def apresenta_tarefa(tarefa: Tarefa):
    """ Retorna uma representação da tarefa seguindo o schema definido em
        TarefaViewSchema.
    """
    return {
        "id": tarefa.id,
        "descricao": tarefa.descricao,
        "data_inicio": tarefa.data_inicio.strftime("%d/%m/%Y %H:%M:%S") if tarefa.data_inicio is not None else "",
        "data_conclusao": tarefa.data_conclusao.strftime("%d/%m/%Y %H:%M:%S") if tarefa.data_conclusao is not None else ""
    }