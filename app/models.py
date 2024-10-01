from pydantic import BaseModel
from typing import List

# Request model for matching items
class MatchRequest(BaseModel):
    trade: str
    unit_of_measure: str

# Model for individual items
class Item(BaseModel):
    trade: str
    unit_of_measure: str
    rate: float

# Request model for loading new items
class LoadRequest(BaseModel):
    items: List[Item]
    replace: bool = True  # If true, replace the current items; otherwise append
