from app.config import PALAVRAS_PROIBIDAS
from app.utils.text_utils import normalizar_texto

def verificar_palavras_proibidas(texto: str):
    texto_normalizado = normalizar_texto(texto)
    return [palavra for palavra in PALAVRAS_PROIBIDAS if palavra in texto_normalizado]
