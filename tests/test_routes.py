"""
@purpose QuoteCheck Code Challenge
@author Chitrakshi Gosain
@date Last Edited - Sep 20, 2024
"""

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

def test_exact_match() -> None:
    """
    Test for exact matching of trade and unit of measure.

    This test checks if the API returns the correct item when both the trade and 
    unit of measure match exactly with an existing item.

    Asserts:
        - Status code is 200 (OK).
        - The best match's trade, unit_of_measure, and rate are correct.
        - The similarity score is 1.0 (exact match).
    """
    response = client.post("/match", json={"trade": "painting", "unit_of_measure": "m2"})
    assert response.status_code == 200
    data = response.json()
    assert data["best_match"]["trade"] == "Painting"
    assert data["best_match"]["unit_of_measure"] == "M2"
    assert data["best_match"]["rate"] == 23.0
    assert data["similarity_score"] == 1.0

def test_partial_match() -> None:
    """
    Test for partial matching of trade and unit of measure.

    This test verifies that the API returns a match when there is only a partial 
    similarity between the input and an existing item (similarity score > 0.5).

    Asserts:
        - Status code is 200 (OK).
        - The best match's trade, unit_of_measure, and rate are correct.
        - The similarity score is greater than 0.5.
    """
    response = client.post("/match", json={"trade": "plumbing", "unit_of_measure": "item"})
    assert response.status_code == 200
    data = response.json()
    assert data["best_match"]["trade"] == "Plumbing"
    assert data["best_match"]["unit_of_measure"] == "EACH"
    assert data["best_match"]["rate"] == 150.0
    assert data["similarity_score"] > 0.5

def test_no_match() -> None:
    """
    Test for no match found in the system.

    This test checks if the API returns a 404 status code and appropriate error
    message when no matching trade or unit of measure is found.

    Asserts:
        - Status code is 404 (Not Found).
        - The error detail message is "No matching item found."
    """
    response = client.post("/match", json={"trade": "random", "unit_of_measure": "whatnot"})
    assert response.status_code == 404
    assert response.json() == {"detail": "No matching item found."}

def test_load_items() -> None:
    """
    Test for loading new items into the system.

    This test verifies that new items can be loaded into the system and can be
    matched later. It first loads new items and then tries to match one of them.

    Asserts:
        - Status code is 200 (OK) when loading items.
        - The load response contains no content (None).
        - The new item "Carpentry" is successfully matched after being loaded.
        - The similarity score for the matched item is greater than 0.9.
    """
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
    assert load_response.json() is None

    # Test that the new items are available
    match_response = client.post("/match", json={"trade": "carpentry", "unit_of_measure": "hour"})
    assert match_response.status_code == 200
    assert match_response.json()["best_match"]["trade"] == "Carpentry"
    assert match_response.json()["similarity_score"] > 0.9
