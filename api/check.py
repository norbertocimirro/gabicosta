import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

NEXUSPAG_API_KEY = os.getenv("NEXUSPAG_API_KEY")

# ===========================================================================
# 📦 LINKS DE ENTREGA (Substitua pelos seus links reais do Google Drive/Mega!)
# ===========================================================================
DELIVERY_LINKS = {
    "promo": "https://mega.nz/folder/LINK_DA_PROMO_COMPLETA",
    "promo_metade": "https://mega.nz/folder/LINK_DA_METADE_DAS_FOTOS"
}
# ===========================================================================

@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def check_status(path):
    transaction_id = request.args.get("id")
    pack_id = request.args.get("pack")

    if not transaction_id or not pack_id:
        return jsonify({"success": False, "message": "Parâmetros ausentes"}), 400

    headers = {
        "x-api-key": NEXUSPAG_API_KEY
    }

    try:
        # Consulta o status atual da transação diretamente na API da NexusPag
        response = requests.get(f"https://nexuspag.com/api/pix/{transaction_id}", headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")

            # Se o status for "paid", o cliente pagou! Liberamos o link do produto.
            if status == "paid":
                secret_link = DELIVERY_LINKS.get(pack_id, "https://mega.nz")
                return jsonify({
                    "paid": True,
                    "download_url": secret_link
                })
            
            return jsonify({"paid": False, "status": status})

        return jsonify({"success": False, "message": "Erro ao consultar gateway"}), response.status_code

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
