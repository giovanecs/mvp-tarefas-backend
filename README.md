# POS-GRADUAÇÃO ENGENHARIA SOFTWARE PUC/RIO

# TAREFAS API

Este pequeno projeto fez parte da avalicao da Sprint: **Arquitetura Software**

O objetivo aqui é ilutsrar o conteúdo apresentado ao longo das disciplinas.

## Como executar

Você pode executar o projeto de duas formas, localmente ou utilizando docker

### Clone o repositório:

git clone https://github.com/giovanecs/mvp-tarefas-backend.git

### Acesso o diretório do projeto

cd mvp-tarefas-backend

# Executando localmente 

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

# Executando o projeto com Docker

## Construção da Imagem

### Para construir a imagem Docker, execute o seguinte comando na raiz do projeto:

docker build -t mvp-tarefas-backend .

## Executar o Contêiner

### Para executar o contêiner Docker, execute o seguinte comando:

docker run -d --name mvp-tarefas-backend -p 5000:5000 mvp-tarefas-backend