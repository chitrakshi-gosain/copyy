"""
@purpose QuoteCheck Code Challenge
@author Chitrakshi Gosain
@date Last Edited - Sep 20, 2024
"""

from uuid import uuid4
from typing import List
from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    """
    Data model representing a request for matching items.

    Attributes:
        trade (str): The trade type of the item.
        unit_of_measure (str): The unit of measurement associated with the item.
    """
    trade: str
    unit_of_measure: str


class Item(BaseModel):
    """
    Data model representing an individual item obtained as an input.

    Attributes:
        id (str): The auto-generated unique identifier of the item.
        trade (str): The trade type of the item.
        unit_of_measure (str): The unit of measurement associated with the item.
        rate (float): The rate associated with the item.
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    trade: str
    unit_of_measure: str
    rate: float


class LoadRequest(BaseModel):
    """
    Data model representing a request to load new items into the system.

    Attributes:
        items (List[Item]): A list of items to be loaded.
        replace (bool): If True, replaces the existing items; otherwise appends the new items. Defaults to True.
    """
    items: List[dict[str, str | float]]
    replace: bool = True
