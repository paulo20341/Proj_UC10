import mercadopago

def gerar_link_pagamento():
    
    # Inicializando o SDK com o Access Token
    sdk = mercadopago.SDK("TEST-4803588640992888-120518-035456cee4f530c7b4bb47607619f83c-1346656170")


    # Dados do pagamento
    payment_data = {
        "items": [
            {
                "id": "1",
                "title": "Camisa",
                "quantity": 1,
                "currency_id": "BRL",
                "unit_price": 259.99
            }
        ],"back_urls": {
            "success": "http://127.0.0.1:5000/compracerta",
            "failure": "http://127.0.0.1:5000/compraerrada",
            "pending": "http://127.0.0.1:5000/compraerrada",
        },
        "auto_return":"all"
    }

    # Criando o pagamento
    result = sdk.preference().create(payment_data)
    payment = result["response"]
    link_iniciar_pagamento = payment["init_point"]
    return link_iniciar_pagamento

    