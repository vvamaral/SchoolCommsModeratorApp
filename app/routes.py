from flask import Blueprint, request, jsonify
from app.services.grammar_checker import check_grammar
from app.config import LANGUAGETOOL_API_URL, PALAVRAS_PROIBIDAS
from unidecode import unidecode
import time

routes = Blueprint("routes", __name__)

def medir_tempo(f):
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = f(*args, **kwargs)
        fim = time.time()
        print(f"Tempo de execução: {fim - inicio:.2f} segundos")
        return resultado
    return wrapper

@routes.route('/')
def index():
    return "O Moderador Inteligente de Comunicações Escolares está funcionando!"

@routes.route('/moderar', methods=['POST'])
def moderar_texto():
    if not request.is_json:
        return jsonify({"status": "REJEITADO", "motivo": "Requisição deve ser JSON"}), 400

    data = request.get_json()
    texto = data.get('texto', '')

    if not texto:
        return jsonify({"status": "REJEITADO", "motivo": "Campo 'texto' ausente ou vazio."}), 400

    texto_normalizado = unidecode(texto.lower())
    palavras_encontradas = [palavra for palavra in PALAVRAS_PROIBIDAS if palavra in texto_normalizado]

    if palavras_encontradas:
        return jsonify({
            "status": "REJEITADO",
            "motivo": f"Palavra(s) proibida(s) detectada(s): {', '.join(palavras_encontradas)}."
        }), 200

    return jsonify({"status": "APROVADO", "motivo": "Nenhuma palavra proibida encontrada."}), 200

@routes.route('/analyze-text', methods=['POST'])
@medir_tempo
def analyze_text():
    if not request.is_json:
        return jsonify({"erro": "Requisição deve ser JSON"}), 400

    data = request.get_json()
    texto = data.get("texto", "")

    if not texto:
        return jsonify({"erro": "Campo 'texto' ausente ou vazio"}), 400

    resultado = check_grammar(texto)
    return jsonify(resultado)