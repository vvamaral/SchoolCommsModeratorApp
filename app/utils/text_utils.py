import unicodedata

def normalizar_texto(texto: str) -> str:
    """
    Remove acentos e coloca tudo em minúsculas.
    """
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto.lower()
