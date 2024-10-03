"""
@purpose QuoteCheck Code Challenge
@author Chitrakshi Gosain
@date Last Edited - Sep 20, 2024
"""

import random
import json
from typing import List
from fastapi import APIRouter, HTTPException
from .models import Item, MatchRequest, LoadRequest
from .services import Matcher

# Initialize FastAPI router
router = APIRouter()

# Instantiate the Matcher service
matcher = Matcher()

@router.post("/load")
def load_items(data: LoadRequest) -> None:
    """
    Endpoint to load new items into the system.

    Args:
        data (LoadRequest): The request data containing items to be loaded and a flag to either replace or append. This is for
                                any new items only. The original data provided is loaded by default when the Matcher service
                                is instantiated.

    Raises:
        ValueError: If any item in the input does not have the required data types for 'trade', 'unit_of_measure', or 'rate'.
    """
    try:
        matcher.load_new_items(matcher.create_items_from_json(data.items), replace=data.replace)
    except ValueError as v:
        raise HTTPException(
            status_code=400, detail=f"Incorrect data type for 'trade', 'unit_of_measure', or 'rate': {str(v)}"
        ) from v
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to load items due to poor structure") from e

@router.post("/match")
def match_item(data: MatchRequest) -> dict[str, Item | float]:
    """
    Endpoint to find the best match for a given trade and unit of measure.

    Args:
        data (MatchRequest): The request data containing the trade and unit of measure to be matched.

    Raises:
        HTTPException: If the trade or unit_of_measure is not provided.
        HTTPException: If no matching item is found with a similarity score greater than 0.5.

    Returns:
        dict[str, Item | float]: A dictionary containing the best matching item and its similarity score
                                    (rounded off to 2 decimal points).
    """
    if not data.trade or not data.unit_of_measure:
        raise HTTPException(status_code=400, detail="Invalid input, trade and unit_of_measure must be provided.")

    best_match, score = matcher.find_best_match(data).values()

    if best_match is None or score < 0.5:
        raise HTTPException(status_code=404, detail="No matching item found.")

    return {
        "best_match": best_match,
        "similarity_score": round(score, ndigits=2)
    }

@router.get("/get_items")
def get_items() -> List[Item]:
    """
    Retrieve all items currently stored in the system.

    Raises:
        HTTPException: If an error has occurred when retrieving items from the system.

    Returns:
        List[Item]: List of all stored items.
    """
    try:
        return matcher.get_all_items()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve items: {str(e)}") from e

@router.get("/show_similarity_of_random_input")
def show_similarity_of_random_input() -> dict:
    """
    Pick a random input from 'app/data/inputs.json' and return its similarity score.

    Returns:
        dict: A dictionary containing the random input and its similarity score.

    Assumptions:
        - "app/data/inputs.json" exists and has a proper structure
        - chosen random input contains a 'trade' and 'unit_of_measure'
    """
    try:
        with open(file="app/data/inputs.json", mode="r", encoding="utf-8") as file:
            inputs = json.load(file)["example_inputs"]

        if not inputs:
            raise HTTPException(status_code=404, detail="No inputs found in 'app/data/inputs.json'.")

        # Randomly select an input
        random_input = random.choice(inputs)
        match_request = MatchRequest(trade=random_input["trade"], unit_of_measure=random_input["unit_of_measure"])

        # Match the random input and get the similarity score
        result = match_item(match_request)

        return {
            "random_input": random_input,
            "best_match": result["best_match"],
            "similarity_score": result["similarity_score"]
        }

    except FileNotFoundError as f:
        raise HTTPException(status_code=500, detail="'app/data/inputs.json' not found.") from f
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to show similarity for random input: {str(e)}") from e

@router.delete("/clear")
def clear_items() -> str:
    """
    Clear all items from the system.

    Raises:
        HTTPException: If an error has occurred when clearing the system.

    Returns:
        str: A message to show the state of the system has been reset successfully.
    """
    try:
        matcher.clear_items()

        return "Squeaky Clean!"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear items: {str(e)}") from e
