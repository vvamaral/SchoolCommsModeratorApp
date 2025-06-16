# Use a imagem base oficial do Python
FROM python:3.9-slim-buster

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Copia o resto do código da sua aplicação
COPY . .

# Define a variável de ambiente PORT que o Cloud Run espera
ENV PORT 8080

# Expõe a porta que a aplicação vai escutar
EXPOSE $PORT

# Comando para rodar a aplicação quando o contêiner iniciar
CMD ["python3", "main.py"]