from fastapi import status
from fastapi.testclient import TestClient

def test_create_customer(client: TestClient):
    response = client.post("/customers/", json={
        "name": "Marta Luis",
        "email": "marta@gmail.com",
        "age":34,
        })
    assert response.status_code == status.HTTP_201_CREATED
   
def test_read_customer(client: TestClient):
    response = client.post("/customers/", json={
        "name": "Marta Luis",
        "email": "marta@gmail.com",
        "age":34,
        })
    assert response.status_code == status.HTTP_201_CREATED
    customer_id: int = response.json()['id']
    response_read = client.get(
        f"/customers/{customer_id}"
    )
    assert response_read.status_code == status.HTTP_200_OK
    assert response_read.json()['name'] == "Marta Luis"
    assert response_read.json()['email'] == "marta@gmail.com"
    assert response_read.json()['age'] == 34

    
