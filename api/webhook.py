import json
from flask import jsonify, request


PAYMENTS = {}



def handler(request):


    data = request.json or {}



    transaction_id = data.get("id")



    status = data.get("status")



    if not transaction_id:

        return jsonify({
            "success": False
        })



    if status in [
        "paid",
        "approved",
        "completed"
    ]:


        PAYMENTS[transaction_id] = {

            "status":"paid"

        }



    return jsonify({

        "success":True

    })
