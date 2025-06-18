import requests
from app.config import LANGUAGETOOL_API_URL

def check_grammar(text, lang="pt-BR"):
    payload = {
        "text": text,
        "language": lang
    }

    try:
        response = requests.post(LANGUAGETOOL_API_URL, data=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"LanguageTool error: {str(e)}"}