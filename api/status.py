import os
import json
from flask import jsonify, request


# Temporário:
# depois substituímos por banco real

PAYMENTS = {}



def handler(request):

    transaction_id = request.args.get("id")


    if not transaction_id:
        return jsonify({
            "paid": False,
            "message": "ID ausente"
        })


    payment = PAYMENTS.get(transaction_id)



    if payment and payment.get("status") == "paid":

        return jsonify({

            "paid": True

        })



    return jsonify({

        "paid": False

    })
