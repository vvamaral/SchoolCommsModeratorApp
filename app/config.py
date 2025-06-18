import os

# Porta padrão que o Flask usará
FLASK_PORT = int(os.getenv("PORT", 8080))

# URL da API do LanguageTool
LANGUAGETOOL_API_URL = os.getenv("LT_API_URL", "http://localhost:8081/v2/check")

# Timeout para requisições ao LanguageTool
LANGUAGETOOL_TIMEOUT = int(os.getenv("LT_TIMEOUT", 5))

# Lista de palavras proibidas (usado em moderation_service.py)
PALAVRAS_PROIBIDAS = [
    "idiota", 
    "burra", 
    "burro", 
    "besta", 
    "desgraca", 
    "porcaria", 
    "lixo", 
    "nojento", 
    "nojenta",
    "vagabundo", 
    "vagabunda", 
    "merda", 
    "droga", 
    "ridiculo",
    "escroto",
    "babaca",
    "cretino",
    "corno",
    "corna",
    "cornao",
    "safado",
    "safada",
    "ignorante", 
    "tapado", 
    "imbecil", 
    "otario", 
    "idiotice",
    "puta",
    "puto",
    "escroto",
    "toba",
    "cu"
]
