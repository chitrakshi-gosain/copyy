"""
@author Chitrakshi Gosain
"""

from typing import List
from pydantic import BaseModel, Field
from uuid import uuid4

# Request model for matching items
class MatchRequest(BaseModel):
    """
    Data model representing a request for matching items.

    Attributes:
        trade (str): The trade type of the item.
        unit_of_measure (str): The unit of measurement associated with the item.
    """
    trade: str
    unit_of_measure: str

# Model for individual items
class Item(BaseModel):
    """
    Data model representing an individual item.

    Attributes:
        id (str): The unique identifier of the item.
        trade (str): The trade type of the item.
        unit_of_measure (str): The unit of measurement associated with the item.
        rate (float): The rate associated with the item.
    """
    id: str = Field(default_factory=lambda: str(uuid4()))  # Auto-generate unique id if not provided
    trade: str
    unit_of_measure: str
    rate: float

# Request model for loading new items
class LoadRequest(BaseModel):
    """
    Data model representing a request to load new items into the system.

    Attributes:
        items (List[Item]): A list of items to be loaded.
        replace (bool): If True, replaces the existing items; otherwise appends the new items. Defaults to True.
    """
    items: List[Item]
    replace: bool = True  # If true, replace the current items; otherwise append
