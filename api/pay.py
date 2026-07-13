import os
import uuid
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Tabela de preços centralizada para suas promoções
PACKS = {
    "combo": {"price": 99.90, "name": "Combo Gabi Total 👑"},
    "ousado": {"price": 79.90, "name": "Sessão Ousada VIP 🛥️"},
    "erotico": {"price": 29.90, "name": "Sessão Erótica VIP 🔞"}
    "promo": {"price": 19.90, "name": "PROMOÇÃO EXCLUSIVA 🎁"}  # 👈 ADICIONE ESSA LINHA!
}

NEXUSPAG_API_KEY = os.getenv("NEXUSPAG_API_KEY")

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
        "webhook_url": "https://gabicosta.vercel.app/api/webhook", # Ajustado para o seu link oficial
        "expiration": 900
    }

    headers = {
        "x-api-key": NEXUSPAG_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://nexuspag.com/api/pix/create", json=payload, headers=headers, timeout=10)
        
        # 🔑 CORREÇÃO AQUI: Agora aceita tanto 200 quanto 201 (Created)
        if response.status_code in [200, 201]:
            res_data = response.json()
            if res_data.get("success"):
                return jsonify({
                    "success": True,
                    "pix_copia_cola": res_data["transaction"]["pix_copia_cola"],
                    "qr_code_base64": res_data["transaction"]["qr_code_base64"]
                })
            return jsonify({"success": False, "message": "Gateway recusou a criação"}), 400
            
        return jsonify({"success": False, "message": f"Erro NexusPag HTTP {response.status_code}"}), 500

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 502
