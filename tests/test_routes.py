from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_exact_match():
    response = client.post("/match", json={"trade": "painting", "unit_of_measure": "m2"})
    assert response.status_code == 200
    data = response.json()
    assert data["best_match"]["trade"] == "Painting"
    assert data["best_match"]["unit_of_measure"] == "M2"
    assert data["best_match"]["rate"] == 23.0
    assert data["similarity_score"] == 1.0

def test_partial_match():
    response = client.post("/match", json={"trade": "plumbing", "unit_of_measure": "item"})
    assert response.status_code == 200
    data = response.json()
    assert data["best_match"]["trade"] == "Plumbing"
    assert data["best_match"]["unit_of_measure"] == "EACH"
    assert data["best_match"]["rate"] == 150.0
    assert data["similarity_score"] > 0.5

def test_no_match():
    response = client.post("/match", json={"trade": "random", "unit_of_measure": "whatnot"})
    assert response.status_code == 404
    assert response.json() == {"detail": "No matching item found."}

def test_load_items():
    new_items = {
        "items": [
            {
                "trade": "Carpentry",
                "unit_of_measure": "Hour",
                "rate": 35.0
            },
            {
                "trade": "Landscaping",
                "unit_of_measure": "SqFt",
                "rate": 10.0
            }
        ],
        "replace": True
    }
    
    load_response = client.post("/load", json=new_items)
    assert load_response.status_code == 200
    assert load_response.json() == None

    # Test that the new items are available
    match_response = client.post("/match", json={"trade": "carpentry", "unit_of_measure": "hour"})
    assert match_response.status_code == 200
    assert match_response.json()["best_match"]["trade"] == "Carpentry"
    assert match_response.json()["similarity_score"] > 0.9
