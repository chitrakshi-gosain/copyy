"""
@author Chitrakshi Gosain
"""

from typing import List
from pydantic import BaseModel

# Request model for matching items
class MatchRequest(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    trade: str
    unit_of_measure: str

# Model for individual items
class Item(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    trade: str
    unit_of_measure: str
    rate: float

# Request model for loading new items
class LoadRequest(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    items: List[Item]
    replace: bool = True  # If true, replace the current items; otherwise append
