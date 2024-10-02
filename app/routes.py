"""
@author Chitrakshi Gosain
"""

import random
import json
from fastapi import APIRouter, HTTPException
from .models import MatchRequest, LoadRequest
from .services import Matcher

# Initialize FastAPI router
router = APIRouter()

# Instantiate the Matcher service (could be dependency injected)
matcher = Matcher()

@router.post("/load")
def load_items(data: LoadRequest) -> None:
    """
    Endpoint to load new items into the system.

    Args:
        data (LoadRequest): The request data containing items to be loaded and a flag to either replace or append.
    """
    matcher.load_new_items(data.items, replace=data.replace)

@router.post("/match")
def match_item(data: MatchRequest) -> dict[str, dict[str, str | float] | float]:
    """
    Endpoint to find the best match for a given trade and unit of measure.

    Args:
        data (MatchRequest): The request data containing the trade and unit of measure to be matched.

    Raises:
        HTTPException: If the trade or unit_of_measure is not provided.
        HTTPException: If no matching item is found with a similarity score greater than 0.5.

    Returns:
        dict: A dictionary containing the best matching item and its similarity score.
    """
    if not data.trade or not data.unit_of_measure:
        raise HTTPException(status_code=400, detail="Invalid input, trade and unit_of_measure must be provided.")

    best_match, score = matcher.find_best_match(data).values()

    if best_match is None or score < 0.5:
        raise HTTPException(status_code=404, detail="No matching item found.")

    return {
        "best_match": best_match,
        "similarity_score": round(score, 2)
    }

@router.post("/clear")
def clear_items() -> None:
    """
    Clear all items from the system.
    """
    try:
        matcher.clear_items()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear items: {str(e)}")


@router.get("/get_items")
def get_items() -> list:
    """
    Retrieve all items currently stored in the system.
    
    Returns:
        list: List of all stored items.
    """
    try:
        items = matcher.get_all_items()
        if not items:
            raise HTTPException(status_code=404, detail="No items found.")
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve items: {str(e)}")


@router.get("/show_similarity_of_random_input")
def show_similarity_of_random_input() -> dict:
    """
    Pick a random input from 'app/data/inputs.json' and return its similarity score.

    Returns:
        dict: A dictionary containing the random input and its similarity score.
    """
    try:
        # Assuming inputs.json exists and has a proper structure
        with open("app/data/inputs.json", "r") as file:
            inputs = json.load(file)
        
        if not inputs:
            raise HTTPException(status_code=404, detail="No inputs found in inputs.json.")

        # Randomly select an input
        random_input = random.choice(inputs)

        # Assuming the random input contains a 'trade' and 'unit_of_measure'
        match_request = MatchRequest(trade=random_input['trade'], unit_of_measure=random_input['unit_of_measure'])

        # Match the random input and get the similarity score
        result = match_item(match_request)
        
        return {
            "random_input": random_input,
            "best_match": result["best_match"],
            "similarity_score": result["similarity_score"]
        }

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="inputs.json not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to show similarity for random input: {str(e)}")

# /clear
# /get_items
# /show_similarity_of_random_input (pick an input from app/data/inputs.json)
