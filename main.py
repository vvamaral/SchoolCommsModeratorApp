from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Habilita CORS para todas as rotas

# Não precisamos de PROJECT_ID, LOCATION ou ENDPOINT_ID se não estivermos usando Vertex AI AGORA.
# As variáveis de ambiente PORT já são tratadas pelo os.environ.get diretamente no app.run.

PALAVRAS_PROIBIDAS = ["idiota", "chata", "palavrão", "ofensa", "gostoso"]

@app.route('/')
def index():
    return "O Moderador Inteligente de Comunicações Escolares está funcionando!"

@app.route('/moderar', methods=['POST'])
def moderar_texto():
    if not request.is_json:
        return jsonify({"status": "REJEITADO", "motivo": "Requisição deve ser JSON"}), 400

    data = request.get_json()
    texto = data.get('texto', '')

    if not texto:
        return jsonify({"status": "REJEITADO", "motivo": "Campo 'texto' ausente ou vazio."}), 400

    palavras_encontradas = [palavra for palavra in PALAVRAS_PROIBIDAS if palavra in texto.lower()]
    if palavras_encontradas:
        return jsonify({
            "status": "REJEITADO",
            "motivo": f"Palavra(s) proibida(s) detectada(s): {', '.join(palavras_encontradas)}."
        }), 200

    return jsonify({"status": "APROVADO", "motivo": "Nenhuma palavra proibida encontrada."}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)