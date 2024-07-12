# Use a imagem base do Python
FROM python:3.11.2

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo requirements.txt para o container
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do projeto para o container
COPY . .

# Expõe a porta que o Flask usará
EXPOSE 5000

# Defina o comando para iniciar o aplicativo (ajuste conforme necessário)
CMD ["python", "app.py"]