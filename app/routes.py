from fastapi import APIRouter, HTTPException
from models import MatchRequest, LoadRequest
from services import Matcher

# Initialize FastAPI router
router = APIRouter()

# Instantiate the Matcher service (could be dependency injected)
matcher = Matcher()

@router.post("/load") # should be put? it should append
def load_items(data: LoadRequest):
    matcher.load_new_items(data.items, replace=data.replace)

@router.post("/match")
def match_item(data: MatchRequest):
    if not data.trade or not data.unit_of_measure:
        raise HTTPException(status_code=400, detail="Invalid input, trade and unit_of_measure must be provided.")
    
    best_match, score = matcher.find_best_match(data)

    if best_match is None or score < 0.5:
        raise HTTPException(status_code=404, detail="No matching item found.")
    
    return {
        "best_match": best_match,
        "similarity_score": round(score, 2)
    }

# /load_default_items
# /clear
# /get_items
# /show_similarity_of_random_input
