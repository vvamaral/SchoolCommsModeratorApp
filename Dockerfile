# ====================================================================
# IMAGEM BASE
# Usamos eclipse-temurin:17-jre que já vem com Java 17 (para LanguageTool)
# e é baseada em Debian, o que facilita a instalação de pacotes APT.
# ====================================================================
FROM eclipse-temurin:17-jre

# ====================================================================
# INSTALAÇÃO DE DEPENDÊNCIAS DO SISTEMA
# Inclui Python, pip, venv, dev tools (para compilação), curl, unzip,
# build-essential (compilador C/C++ para pacotes Python como pyhunspell)
# e libhunspell-dev (bibliotecas do Hunspell para pyhunspell).
# O ca-certificates já deve vir com a imagem base JRE, mas se necessário
# pode ser adicionado aqui.
# ====================================================================
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    curl \
    unzip \
    build-essential \
    libhunspell-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ====================================================================
# DIRETÓRIO DE TRABALHO
# Onde a aplicação será executada dentro do contêiner.
# ====================================================================
WORKDIR /app

# ====================================================================
# AMBIENTE VIRTUAL PYTHON
# Cria um ambiente virtual para isolar as dependências Python.
# A pasta 'venv/' deve estar no .dockerignore para não ser copiada do host.
# ====================================================================
RUN python3 -m venv /app/venv

# ====================================================================
# DEPENDÊNCIAS PYTHON
# Copia o arquivo requirements.txt e instala as dependências.
# A flag --trusted-host é usada para contornar problemas de certificado SSL
# que podem ocorrer em alguns ambientes de rede ao acessar pypi.org.
# ====================================================================
COPY requirements.txt .
RUN /app/venv/bin/pip install --no-cache-dir -r requirements.txt --trusted-host files.pythonhosted.org --trusted-host pypi.org

# ====================================================================
# DOWNLOAD E CONFIGURAÇÃO DO LANGUAGETOOL
# Cria um diretório para o LanguageTool, baixa o ZIP, descompacta e remove o ZIP.
# A flag --insecure é usada no curl para contornar problemas de certificado SSL
# com o servidor de download do LanguageTool.
# ====================================================================
RUN mkdir -p /app/languagetool && \
    curl -L --insecure "https://www.languagetool.org/download/LanguageTool-6.6.zip" -o languagetool.zip && \
    unzip languagetool.zip -d languagetool && \
    rm languagetool.zip

# ====================================================================
# COPIA ARQUIVOS DO PROJETO
# Copia todo o código-fonte da sua aplicação para o diretório de trabalho.
# O .dockerignore garante que arquivos/pastas indesejados (como venv/ local)
# não sejam copiados.
# ====================================================================
COPY . .

# ====================================================================
# PERMISSÕES
# Garante que o script de inicialização tenha permissões de execução.
# ====================================================================
RUN chmod +x /app/run_services.sh

# ====================================================================
# COMANDO DE INICIALIZAÇÃO
# Define o comando que será executado quando o contêiner for iniciado.
# ====================================================================
CMD ["/bin/bash", "-c", "/app/run_services.sh"]