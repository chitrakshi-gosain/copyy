"""
@author Chitrakshi Gosain
"""

import json
from typing import List
from difflib import SequenceMatcher
from .models import Item, MatchRequest

class Matcher:
    """_summary_
    """
    def __init__(self) -> None:
        """_summary_
        """
        # Load default items from static data
        self.items = self.load_default_items()

    def load_default_items(self) -> List[dict]:
        """_summary_

        Returns:
            List[dict]: _description_
        """
        with open(file='app/data/items.json', mode='r', encoding='utf-8') as f:
            return json.load(f)

    def load_new_items(self, new_items: List[Item], replace: bool = True) -> None:
        """_summary_

        Args:
            new_items (List[Item]): _description_
            replace (bool, optional): _description_. Defaults to True.
        """
        if replace:
            self.items = [item.dict() for item in new_items]
        else:
            self.items.extend([item.dict() for item in new_items])

    def calculate_similarity(self, input_str: str, target_str: str) -> float:
        """_summary_

        Args:
            input_str (str): _description_
            target_str (str): _description_

        Returns:
            float: _description_
        """
        return SequenceMatcher(None, input_str.lower(), target_str.lower()).ratio()

    def find_best_match(self, data: MatchRequest) -> dict:
        """_summary_

        Args:
            data (MatchRequest): _description_

        Returns:
            dict: _description_
        """
        best_match = None
        highest_score = 0

        for item in self.items:
            trade_similarity = self.calculate_similarity(data.trade, item["trade"])
            uom_similarity = self.calculate_similarity(data.unit_of_measure, item["unit_of_measure"])

            # Weighted score
            similarity_score = (trade_similarity * 0.7) + (uom_similarity * 0.3)

            if similarity_score > highest_score:
                highest_score = similarity_score
                best_match = item

        return {
            "best_match": best_match,
            "highest_score": highest_score
        }
