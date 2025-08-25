from fastapi import status
from fastapi.testclient import TestClient

def test_create_transaction(client: TestClient):
    # Primero crear un customer
    customer_response = client.post("/customers/", json={
        "name": "Ana Garcia",
        "email": "ana@example.com",
        "age": 25,
    })
    assert customer_response.status_code == status.HTTP_201_CREATED
    customer_id = customer_response.json()['id']
    
    # Crear una transacción
    transaction_data = {
        "ammount": 150,
        "description": "Compra de producto",
        "customer_id": customer_id
    }
    
    response = client.post("/transaction", json=transaction_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    transaction_response = response.json()
    assert transaction_response["ammount"] == 150
    assert transaction_response["description"] == "Compra de producto"
    assert transaction_response["customer_id"] == customer_id
    assert "id" in transaction_response

def test_create_transaction_invalid_customer(client: TestClient):
    # Intentar crear transacción con customer inexistente
    transaction_data = {
        "ammount": 100,
        "description": "Transacción inválida",
        "customer_id": 99999  # ID que no existe
    }
    
    response = client.post("/transaction", json=transaction_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Customer not found" in response.json()["detail"]

def test_get_transactions(client: TestClient):
    # Crear un customer
    customer_response = client.post("/customers/", json={
        "name": "Carlos Lopez",
        "email": "carlos@example.com",
        "age": 35,
    })
    assert customer_response.status_code == status.HTTP_201_CREATED
    customer_id = customer_response.json()['id']
    
    # Crear varias transacciones
    for i in range(3):
        transaction_data = {
            "ammount": 100 + (i * 50),
            "description": f"Transacción {i+1}",
            "customer_id": customer_id
        }
        response = client.post("/transaction", json=transaction_data)
        assert response.status_code == status.HTTP_201_CREATED
    
    # Obtener todas las transacciones
    response = client.get("/transaction")
    assert response.status_code == status.HTTP_200_OK
    
    transactions = response.json()
    assert isinstance(transactions, list)
    assert len(transactions) >= 3

def test_get_transactions_with_pagination(client: TestClient):
    # Crear un customer
    customer_response = client.post("/customers/", json={
        "name": "Maria Rodriguez",
        "email": "maria@example.com",
        "age": 28,
    })
    assert customer_response.status_code == status.HTTP_201_CREATED
    customer_id = customer_response.json()['id']
    
    # Crear varias transacciones
    for i in range(10):
        transaction_data = {
            "ammount": 50 + (i * 10),
            "description": f"Transacción paginada {i+1}",
            "customer_id": customer_id
        }
        response = client.post("/transaction", json=transaction_data)
        assert response.status_code == status.HTTP_201_CREATED
    
    # Probar paginación
    response = client.get("/transaction?limit=3&skip=0")
    assert response.status_code == status.HTTP_200_OK
    transactions = response.json()
    assert len(transactions) <= 3
    
    # Probar con página específica
    response = client.get("/transaction?page=2&limit=5")
    assert response.status_code == status.HTTP_200_OK
    transactions = response.json()
    assert len(transactions) <= 5