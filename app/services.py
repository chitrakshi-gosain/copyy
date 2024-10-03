"""
@purpose QuoteCheck Code Challenge
@author Chitrakshi Gosain
@date Last Edited - Sep 20, 2024
"""

import json
from typing import List, Any
from difflib import SequenceMatcher
from .models import Item, MatchRequest
from uuid import uuid4

class Matcher:
    """
    Service class responsible for matching items and loading new items.

    Attributes:
        items (List[dict]): A list of items loaded into the system, either from default data or newly provided data.
    """
    def __init__(self) -> None:
        """
        Initialize the Matcher class and load default items into the system.
        """
        # Load default items from static data
        self.items = self.load_default_items()

    def load_default_items(self) -> List[dict]:
        """
        Load default items from a JSON file.

        Returns:
            List[dict]: A list of default items.
        """
        with open(file='app/data/items.json', mode='r', encoding='utf-8') as f:
            return json.load(f)

    def add_item_id(self, item: Item) -> dict:
        """
        Ensure that each item has a unique ID. If an ID is not provided, it will be generated.

        Args:
            item (Item): The item to process.

        Returns:
            dict: The item with an assigned ID.
        """
        # If the item does not already have an ID, generate one
        if not item.id:
            item.id = str(uuid4())
        return item.model_dump()

    def load_new_items(self, new_items: List[Item], replace: bool = True) -> None:
        """
        Load new items into the system, replacing or appending based on the flag.

        Args:
            new_items (List[Item]): A list of new items to be loaded.
            replace (bool, optional): If True, replaces the current items; if False, appends the new items. Defaults to True.
        """
        if replace:
            self.items = [self.add_item_id(item) for item in new_items]
        else:
            self.items.extend([self.add_item_id(item) for item in new_items])

    def clear_items(self) -> None:
        """
        Clear all items from the matcher.
        """
        self.items.clear()

    def get_all_items(self) -> List[dict[str, Any]]:
        """
        Get all items currently stored in the matcher.

        Returns:
            List[dict[str, Any]]: List of all items.
        """
        return self.items

    def calculate_similarity(self, input_str: str, target_str: str) -> float:
        """
        Calculate the similarity score between two strings using a sequence matching algorithm.

        Args:
            input_str (str): The first input string.
            target_str (str): The second target string to compare against.

        Returns:
            float: A similarity score between 0 and 1, where 1 is an exact match.
        """
        return SequenceMatcher(None, input_str.lower(), target_str.lower()).ratio()

    def find_best_match(self, data: MatchRequest) -> dict:
        """
        Find the best match for a given trade and unit of measure from the loaded items.

        Args:
            data (MatchRequest): The match request containing the trade and unit of measure.

        Returns:
            dict: A dictionary containing the best matching item and its highest similarity score.
        """
        best_match = None
        highest_score = 0

        for item in self.items:
            trade_similarity = self.calculate_similarity(data.trade, item["trade"])
            uom_similarity = self.calculate_similarity(data.unit_of_measure, item["unit_of_measure"])

            # Weighted score
            similarity_score = (trade_similarity * 0.7) + (uom_similarity * 0.3)

            if item and similarity_score > highest_score:
                highest_score = similarity_score
                best_match =  item

        return {
            "best_match": best_match,
            "highest_score": highest_score
        }
