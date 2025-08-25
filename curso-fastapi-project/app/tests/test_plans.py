from fastapi import status
from fastapi.testclient import TestClient

def test_create_plan(client: TestClient):
    plan_data = {
        "name": "Plan Básico",
        "price": 1000,
        "description": "Plan básico con funcionalidades esenciales"
    }
    
    response = client.post("/plan", json=plan_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    plan_response = response.json()
    assert plan_response["name"] == "Plan Básico"
    assert plan_response["price"] == 1000
    assert plan_response["description"] == "Plan básico con funcionalidades esenciales"
    assert "id" in plan_response

def test_create_plan_premium(client: TestClient):
    plan_data = {
        "name": "Plan Premium",
        "price": 2500,
        "description": "Plan premium con todas las funcionalidades"
    }
    
    response = client.post("/plan", json=plan_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    plan_response = response.json()
    assert plan_response["name"] == "Plan Premium"
    assert plan_response["price"] == 2500
    assert plan_response["description"] == "Plan premium con todas las funcionalidades"
    assert "id" in plan_response

def test_create_plan_without_description(client: TestClient):
    plan_data = {
        "name": "Plan Sin Descripción",
        "price": 500
    }
    
    response = client.post("/plan", json=plan_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    plan_response = response.json()
    assert plan_response["name"] == "Plan Sin Descripción"
    assert plan_response["price"] == 500
    assert "id" in plan_response

def test_get_plans_empty(client: TestClient):
    # Obtener planes cuando no hay ninguno creado
    response = client.get("/plans")
    assert response.status_code == status.HTTP_200_OK
    
    plans = response.json()
    assert isinstance(plans, list)

def test_get_plans_with_data(client: TestClient):
    # Crear varios planes
    plans_data = [
        {
            "name": "Plan Starter",
            "price": 800,
            "description": "Plan para principiantes"
        },
        {
            "name": "Plan Business",
            "price": 1500,
            "description": "Plan para empresas"
        },
        {
            "name": "Plan Enterprise",
            "price": 3000,
            "description": "Plan para grandes empresas"
        }
    ]
    
    created_plans = []
    for plan_data in plans_data:
        response = client.post("/plan", json=plan_data)
        assert response.status_code == status.HTTP_201_CREATED
        created_plans.append(response.json())
    
    # Obtener todos los planes
    response = client.get("/plans")
    assert response.status_code == status.HTTP_200_OK
    
    plans = response.json()
    assert isinstance(plans, list)
    assert len(plans) >= 3
    
    # Verificar que los planes creados están en la respuesta
    plan_names = [plan["name"] for plan in plans]
    assert "Plan Starter" in plan_names
    assert "Plan Business" in plan_names
    assert "Plan Enterprise" in plan_names

def test_create_plan_with_zero_price(client: TestClient):
    plan_data = {
        "name": "Plan Gratuito",
        "price": 0,
        "description": "Plan gratuito para pruebas"
    }
    
    response = client.post("/plan", json=plan_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    plan_response = response.json()
    assert plan_response["name"] == "Plan Gratuito"
    assert plan_response["price"] == 0
    assert plan_response["description"] == "Plan gratuito para pruebas"

def test_create_multiple_plans_and_verify_list(client: TestClient):
    # Crear múltiples planes con diferentes precios
    plan_names = ["Plan A", "Plan B", "Plan C", "Plan D"]
    plan_prices = [100, 200, 300, 400]
    
    for name, price in zip(plan_names, plan_prices):
        plan_data = {
            "name": name,
            "price": price,
            "description": f"Descripción para {name}"
        }
        response = client.post("/plan", json=plan_data)
        assert response.status_code == status.HTTP_201_CREATED
    
    # Verificar que todos los planes están en la lista
    response = client.get("/plans")
    assert response.status_code == status.HTTP_200_OK
    
    plans = response.json()
    retrieved_names = [plan["name"] for plan in plans]
    
    for name in plan_names:
        assert name in retrieved_names