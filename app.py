from datetime import datetime
from flask import redirect
from flask_openapi3 import OpenAPI, Info, Tag

from logger import logger
from schemas import *
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

from model import Session, Tarefa

import requests

info = Info(title="API - Minhas Tarefas", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tarefa_tag = Tag(name="Tarefa", description="Adição, visualização e remoção de tarefas à base")


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect("/openapi")

@app.get('/tarefas', tags=[tarefa_tag],
         responses={"200": ListagemTarefasSchema, "404": ErrorSchema})
def get_tarefas():
    """Faz a busca por todas as Tarefas cadastradas

    Retorna uma representação da listagem de tarefas.
    """
    logger.debug(f"Coletando tarefas ")
    session = Session()
    
    tarefas = session.query(Tarefa).all()

    if not tarefas:
        return {"tarefas": []}, 200
    else:
        logger.debug(f"%d tarefas encontradas" % len(tarefas))
        return apresenta_tarefas(tarefas), 200
    


@app.get('/tarefas/pendentes', tags=[tarefa_tag],
         responses={"200": ListagemTarefasSchema, "404": ErrorSchema})
def get_tarefas_pendentes():
    """Faz a busca por todas as Tarefas pendentes cadastradas

    Retorna uma representação da listagem de tarefas.
    """
        
    session = Session()

    tarefas = session.query(Tarefa).filter(
        Tarefa.data_inicio.is_(None),
        Tarefa.data_conclusao.is_(None)
        ).all()

    if not tarefas:
        return {"tarefas": []}, 200
    else:
        logger.debug(f"%d tarefas encontradas" % len(tarefas))
        return apresenta_tarefas(tarefas), 200


@app.get('/tarefas/iniciadas', tags=[tarefa_tag],
         responses={"200": ListagemTarefasSchema, "404": ErrorSchema})
def get_tarefas_iniciadas():
    """Faz a busca por todas as tarefas iniciadas

    Retorna uma representação da listagem de tarefas.
    """
    
    session = Session()
    
    tarefas = session.query(Tarefa).filter(
        and_(Tarefa.data_inicio.is_not(None),
        Tarefa.data_conclusao.is_(None))
        ).all()

    if not tarefas:
        return {"tarefas": []}, 200
    else:
        logger.debug(f"%d tarefas encontradas" % len(tarefas))
        return apresenta_tarefas(tarefas), 200


@app.get('/tarefas/concluidas', tags=[tarefa_tag],
         responses={"200": ListagemTarefasSchema, "404": ErrorSchema})
def get_tarefas_concluidas():
    """Faz a busca por todas as tarefas concluidas

    Retorna uma representação da listagem de tarefas.
    """
    
    session = Session()
    
    tarefas = session.query(Tarefa).filter(Tarefa.data_conclusao.is_not(None)).all()

    if not tarefas:
        return {"tarefas": []}, 200
    else:
        logger.debug(f"%d tarefas encontradas" % len(tarefas))
        return apresenta_tarefas(tarefas), 200
    

@app.get('/tarefa', tags=[tarefa_tag],
         responses={"200": TarefaViewSchema, "404": ErrorSchema})
def get_tarefa(query: TarefaBuscaIdSchema):
    """Faz a busca por uma Tarefa a partir do id da tarefa

    Retorna uma representação da tarefa.
    """
    tarefa_id = query.id
    logger.debug(f"Coletando dados sobre a tarefa #{tarefa_id}")
    
    session = Session()
    
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

    if not tarefa:
        error_msg = "tarefa não encontrada."
        logger.warning(f"Erro ao consultar tarefa #{tarefa_id}, {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"tarefa encontrada: '{tarefa.descricao}'")
        return apresenta_tarefa(tarefa), 200
    
@app.post("/tarefa/add", tags=[tarefa_tag],
          responses={"200": TarefaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tarefa(form: NovaTarefaSchema):
    """Adiciona uma nova Tarefa à base de dados

    Retorna uma representação da tarefa.
    """
    tarefa = Tarefa(descricao=form.descricao)
        
    try:
        
        session = Session()
        session.add(tarefa)
        session.commit()
                
        return apresenta_tarefa(tarefa), 200

    except IntegrityError as e:
        error_msg = "tarefa já salva na base :/"
        logger.warning(f"Erro ao adicionar tarefa '{tarefa.descricao}', {error_msg}")
        return {"message": error_msg}, 409
    
    except Exception as e:
        error_msg = "não foi possível salvar tarefa."
        logger.warning(f"Erro ao adicionar tarefa '{tarefa.descricao}', {error_msg}")
        return {"message": error_msg}, 400
    

@app.post("/tarefa/iniciar", tags=[tarefa_tag],
          responses={"200": TarefaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def iniciar_tarefa(form: AtualizarTarefaSchema):
    """Preenche a data de inicio de uma tarefa e atualiza o registro na base de dados

    Retorna uma representação da tarefa.
    """
    today = datetime.today().date()
    holiday_name = is_holiday(today)
    if holiday_name:
        return {"message": f"Não é possível iniciar a tarefa no feriado: {holiday_name}"}, 400

    session = Session()
    tarefa = session.query(Tarefa).filter_by(id=form.id).first()
    
    if tarefa is None:
        error_msg = "tarefa não encontrada."
        logger.warning(f"Erro ao iniciar tarefa #{form.id}, {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        tarefa.data_inicio = datetime.now()
        session.commit()
        return apresenta_tarefa(tarefa), 200

    
@app.post("/tarefa/concluir", tags=[tarefa_tag],
          responses={"200": TarefaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def concluir_tarefa(form: AtualizarTarefaSchema):
    """Preenche a data de conclusao de uma tarefa e atualiza o registro na base de dados

    Retorna uma representação da tarefa.
    """
        
    session = Session()
    tarefa = session.query(Tarefa).filter_by(id=form.id).first()
    
    if tarefa is None:
        error_msg = "tarefa não encontrada."
        logger.warning(f"Erro ao concluir tarefa #{form.id}, {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        tarefa.data_conclusao = datetime.now()
        session.commit()
        return apresenta_tarefa(tarefa), 200
    

@app.delete('/tarefa', tags=[tarefa_tag],
            responses={"200": TarefaDelSchema, "404": ErrorSchema})
def del_tarefa(query: TarefaBuscaIdSchema):
    """Deleta uma Tarefa a partir do ID informado

    Retorna uma mensagem de confirmação da remoção.
    """
    tarefa_id = query.id
    
    session = Session()
    count = session.query(Tarefa).filter(Tarefa.id == tarefa_id).delete()
    session.commit()

    if count:
        return {"mesage": "tarefa removida", "id": tarefa_id}
    else:
        error_msg = "tarefa não encontrada."
        logger.warning(f"Erro ao deletar tarefa #{tarefa_id}, {error_msg}")
        return {"mesage": error_msg}, 404
    
# Verificar se uma data é feriado
def is_holiday(date):
    response = requests.get('https://brasilapi.com.br/api/feriados/v1/2024')
    holidays = response.json()
    for holiday in holidays:
        if holiday['date'] == date.strftime('%Y-%m-%d'):
            return holiday['name']
    return None
    