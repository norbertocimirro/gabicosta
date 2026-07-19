import os
import uuid
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

PACKS = {
    "promo": {"price": 19.90, "name": "Sessão Promo Exclusiva 🎁"},
    "promo_metade": {"price": 9.90, "name": "Sessão Promo Metade 🌓"}
}

NEXUSPAG_API_KEY = os.getenv("NEXUSPAG_API_KEY")

# 🔄 Blindagem de rotas: responde tanto na raiz da função quanto no caminho completo
@app.route('/', methods=['POST'])
@app.route('/api/pay', methods=['POST'])
def generate_pix():
    data = request.json or {}
    pack_id = data.get("pack_id")

    if pack_id not in PACKS:
        return jsonify({"success": False, "message": "Pacote inválido"}), 400

    selected = PACKS[pack_id]
    external_id = f"gabi_{pack_id}_{uuid.uuid4().hex[:10]}"

    payload = {
        "amount": selected["price"],
        "description": f"Acesso {selected['name']}",
        "external_id": external_id,
        "webhook_url": "https://gabicosta.vercel.app/api/webhook",
        "expiration": 900
    }

    headers = {
        "x-api-key": NEXUSPAG_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://nexuspag.com/api/pix/create", json=payload, headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            res_data = response.json()
            if res_data.get("success"):
                return jsonify({
                    "success": True,
                    "id": res_data["transaction"]["id"],  # Fornece o ID essencial para o rastreio da liberação
                    "pix_copia_cola": res_data["transaction"]["pix_copia_cola"],
                    "qr_code_base64": res_data["transaction"]["qr_code_base64"]
                })
        
        return jsonify({"success": False, "message": f"Erro na plataforma HTTP {response.status_code}"}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
