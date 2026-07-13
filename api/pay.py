import os
import uuid
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ===========================================================================
# 🚀 TABELA DE PREÇOS CENTRALIZADA (Altere aqui para fazer promoções relâmpago!)
# ===========================================================================
PACKS = {
    "combo": {"price": 99.90, "name": "Combo Gabi Total 👑"},
    "ousado": {"price": 79.90, "name": "Sessão Ousada VIP 🛥️"},
    "erotico": {"price": 29.90, "name": "Sessão Erótica VIP 🔞"}
}
# ===========================================================================

NEXUSPAG_API_KEY = os.getenv("NEXUSPAG_API_KEY")

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
        "webhook_url": "https://seu-site.vercel.app/api/webhook", # Mude para o seu link da Vercel
        "expiration": 900
    }

    headers = {
        "x-api-key": NEXUSPAG_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://nexuspag.com/api/pix/create", json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            res_data = response.json()
            if res_data.get("success"):
                return jsonify({
                    "success": True,
                    "pix_copia_cola": res_data["transaction"]["pix_copia_cola"],
                    "qr_code_base64": res_data["transaction"]["qr_code_base64"]
                })
        return jsonify({"success": False, "message": "Erro no gateway"}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 502
