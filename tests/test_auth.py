from fastapi.testclient import TestClient
from app.infra.models import User
from app.main import app
from app.infra.database import sessionLocal

client = TestClient(app)

def test_signup_and_login():
    #delete before it runs
    database = sessionLocal()
    database.query(User).filter(User.email == "alice@example.com").delete()
    database.commit()
    database.close()
    
    # 1. Sign up
    response = client.post("/users/signup", json={
        "username": "Alice",
        "email": "alice@example.com",
        "password": "secret123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "id" in data

    # 2. Login
    response = client.post("/users/login", json={
        "email": "alice@example.com",
        "password": "secret123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

    # 3. Access protected route
    response = client.get("/games", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
