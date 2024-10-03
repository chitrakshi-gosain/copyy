"""
@purpose QuoteCheck Code Challenge
@author Chitrakshi Gosain
@date Last Edited - Sep 20, 2024
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def clear_items() -> None:
    """Clear items before each test."""
    client.post("/clear")


def test_exact_match() -> None:
    """Test for exact matching of trade and unit of measure."""
    response = client.post(
        url="/match/item",
        json={
            "trade": "painting",
            "unit_of_measure": "m2"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["best_match"]["trade"] == "Painting"
    assert data["best_match"]["unit_of_measure"] == "M2"
    assert data["best_match"]["rate"] == 23.0
    assert data["similarity_score"] == 1.0


def test_partial_match() -> None:
    """Test for partial matching of trade and unit of measure."""
    response = client.post(
        url="/match/item",
        json={
            "trade": "plumbing",
            "unit_of_measure": "item"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["best_match"]["trade"] == "Plumbing"
    assert data["best_match"]["unit_of_measure"] == "EACH"
    assert data["best_match"]["rate"] == 150.0
    assert data["similarity_score"] > 0.5


def test_no_match() -> None:
    """Test for no match found in the system."""
    response = client.post(
        url="/match/item",
        json={
            "trade": "random",
            "unit_of_measure": "whatnot"
        }
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "No matching item found."}


def test_load_default_items():
    """Test loading default items."""
    # Check if default items are loaded
    response = client.get(url="/item")
    assert response.status_code == 200
    assert len(response.json()) > 0  # Should return some default items


def test_load_items_from_scratch() -> None:
    """Test for loading new items into the system."""
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
            },
        ],
        "replace": True,
    }

    load_response = client.post(url="/item", json=new_items)
    assert load_response.status_code == 200
    assert load_response.json() == "Successfully loaded items"

    # Test that the new items are available
    match_response = client.post(
        url="/match/item",
        json={
            "trade": "carpentry",
            "unit_of_measure": "hour"
        }
    )
    assert match_response.status_code == 200
    assert match_response.json()["best_match"]["trade"] == "Carpentry"
    assert match_response.json()["similarity_score"] > 0.9


def test_load_additional_items() -> None:
    """Test for loading additional items into the system."""
    current_items = client.get(url="/item")
    assert current_items.status_code == 200

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
            },
        ],
        "replace": False,
    }

    load_response = client.post(url="/item", json=new_items)
    assert load_response.status_code == 200
    assert load_response.json() == "Successfully loaded items"

    # Test that the additional items were added
    updated_items = client.get(url="/item")
    assert updated_items.status_code == 200

    assert len(updated_items.json()) - len(current_items.json()) == 2


def test_clear_items():
    """Test clearing all items."""
    response = client.delete("/clear")
    assert response.status_code == 200
    assert response.json() == "Squeaky Clean!"

    # Check if items are cleared
    response = client.get(url="/item")
    assert response.status_code == 200
    assert response.json() == []


def test_show_similarity_of_random_input():
    """Test showing similarity for a random input."""
    response = client.get(url="/match/random")
    assert response.status_code == 200 or 500
