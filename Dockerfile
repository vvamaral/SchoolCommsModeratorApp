# Use uma imagem base Python slim (menor e mais segura)
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código da sua aplicação
COPY . .

# A porta que a aplicação Flask vai escutar
EXPOSE 8080

# Comando para iniciar a aplicação quando o contêiner for executado
CMD ["python", "main.py"]