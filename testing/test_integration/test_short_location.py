from fastapi.testclient import TestClient
from main import app

def test_short_location_integration():
    client = TestClient(app)
    response = client.post("/short-location", json={"city": "Berlin"})
    
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    assert data["short_url"].startswith("http://localhost:8000/")
    
    short_code = data["short_url"].split("/")[-1]

    get_response = client.get(f"/{short_code}")
    assert get_response.status_code == 200
