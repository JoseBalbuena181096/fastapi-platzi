from fastapi import status
from fastapi.testclient import TestClient
from models import Customer, Transaction

def test_create_invoice(client: TestClient):
    # Primero crear un customer
    customer_response = client.post("/customers/", json={
        "name": "Juan Perez",
        "email": "juan@example.com",
        "age": 30,
    })
    assert customer_response.status_code == status.HTTP_201_CREATED
    customer_data = customer_response.json()
    customer_id = customer_data['id']
    
    # Crear algunas transacciones para el customer
    transaction1_response = client.post("/transaction", json={
        "ammount": 100,
        "description": "Primera transacción",
        "customer_id": customer_id
    })
    assert transaction1_response.status_code == status.HTTP_201_CREATED
    
    transaction2_response = client.post("/transaction", json={
        "ammount": 200,
        "description": "Segunda transacción",
        "customer_id": customer_id
    })
    assert transaction2_response.status_code == status.HTTP_201_CREATED
    
    # Obtener las transacciones creadas
    transactions_response = client.get("/transaction")
    assert transactions_response.status_code == status.HTTP_200_OK
    transactions = transactions_response.json()
    
    # Crear invoice con los datos
    invoice_data = {
        "id": 1,
        "customer": customer_data,
        "transactions": transactions,
        "total": 300
    }
    
    response = client.post("/invoice", json=invoice_data)
    assert response.status_code == status.HTTP_200_OK
    
    invoice_response = response.json()
    assert invoice_response["id"] == 1
    assert invoice_response["customer"]["name"] == "Juan Perez"
    assert invoice_response["total"] == 300
    assert len(invoice_response["transactions"]) >= 2