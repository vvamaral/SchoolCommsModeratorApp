from flask import Flask, request, jsonify
from google.cloud import aiplatform
import os

app = Flask(__name__)

# Configurações do Google Cloud
# Substitua '492434483802' pelo seu ID de projeto caso ele seja diferente
PROJECT_ID = os.environ.get('GCP_PROJECT_ID', '492434483802') 
LOCATION = os.environ.get('GCP_LOCATION', 'us-central1') # Região onde o Vertex AI está disponível

# Inicializar o cliente do Vertex AI
# Usaremos um modelo simples por enquanto. Gemini API requer configurações mais avançadas
# mas para protótipo, podemos simular ou usar um modelo básico.
# Por enquanto, vamos simular a moderação e deixar a integração real com LLM para depois,
# para você ver a aplicação rodando primeiro.

# Exemplo simples de um "modelo" de moderação em Python puro
def moderar_texto_simples(texto):
    texto_lower = texto.lower()
    erros = []
    sugestoes = []
    status = "aprovado"
    motivo = "Conteúdo OK"

    # Simulação de detecção de erros gramaticais/ortográficos (muito básico)
    if "erro" in texto_lower or "eror" in texto_lower: # Simplesmente para demonstrar
        erros.append("Possível erro ortográfico/gramatical detectado.")
        sugestoes.append("Verifique a ortografia e gramática.")

    # Simulação de detecção de tom inadequado/palavras proibidas
    palavras_proibidas = ["idiota", "bobo", "feio", "chato", "reclamação"]
    for palavra in palavras_proibidas:
        if palavra in texto_lower:
            status = "rejeitado"
            motivo = f"Contém palavra inadequada: '{palavra}'."
            sugestoes.append(f"Evite usar a palavra '{palavra}'.")
            break # Para aqui se encontrar a primeira palavra proibida

    if not erros and status == "aprovado":
        # Poderíamos adicionar aqui uma lógica mais complexa ou chamada ao LLM real
        pass
    elif erros and status == "aprovado":
        status = "revisao_humana"
        motivo = "Detectado possível erro gramatical/ortográfico, requer revisão."

    # Considerar casos ambíguos
    if "talvez" in texto_lower or "acho que" in texto_lower:
         if status == "aprovado": # Só se já não tiver sido rejeitado
            status = "revisao_humana"
            motivo = "Mensagem com tom ambíguo, sugere revisão humana."
            sugestoes.append("Tente ser mais direto ou claro.")


    return {
        "status": status, # aprovado, rejeitado, revisao_humana
        "motivo": motivo,
        "erros_detectados": erros,
        "sugestoes_melhoria": sugestoes
    }

@app.route('/moderar', methods=['POST'])
def moderar_comunicacao():
    data = request.get_json(silent=True)

    if not data or 'texto' not in data:
        return jsonify({"error": "Parâmetro 'texto' ausente na requisição."}), 400

    texto_comunicacao = data['texto']

    # Chama a função de moderação (por enquanto a simples)
    resultado_moderacao = moderar_texto_simples(texto_comunicacao)

    return jsonify(resultado_moderacao)

@app.route('/')
def hello_world():
    return 'O Moderador Inteligente de Comunicações Escolares está funcionando!'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))