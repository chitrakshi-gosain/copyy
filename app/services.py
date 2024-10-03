"""
@purpose QuoteCheck Code Challenge
@author Chitrakshi Gosain
@date Last Edited - Sep 20, 2024
"""

import json
from typing import List
from difflib import SequenceMatcher
from .models import Item, MatchRequest


class Matcher:
    """
    Service class responsible for matching items and loading new items.

    Attributes:
        items (List[Item]): A list of items loaded in the system, either from default data, newly provided data or a mix of both.
    """

    def __init__(self) -> None:
        """
        Initialize the Matcher class and load default items from "app/data/items.json" into the system.

        This method reads the JSON file containing item data and populates the items list with Item instances
        created from the JSON data.
        """
        self.items: list[Item] = []

        with open(file="app/data/items.json", mode="r", encoding="utf-8") as file:
            self.load_new_items(self.create_items_from_json(json.load(file)))

    def create_items_from_json(
        self, json_input: List[dict[str, str | float]]
    ) -> List[Item]:
        """
        Create a list of Item instances from the provided JSON input.

        Args:
            input (List[dict[str, str | float]]): A list of dictionaries, each representing an item with
                                                    'trade', 'unit_of_measure', and 'rate' keys.

        Returns:
            List[Item]: A list of Item instances created from the input data.
        """
        items = []
        for item in json_input:
            if (
                isinstance(item["trade"], str)
                and isinstance(item["unit_of_measure"], str)
                and isinstance(item["rate"], float)
            ):
                items.append(
                    Item(
                        trade=item["trade"],
                        unit_of_measure=item["unit_of_measure"],
                        rate=item["rate"],
                    )
                )

        return items

    def load_new_items(self, new_items: List[Item], replace: bool = True) -> None:
        """
        Load new items into the system, replacing or appending based on the flag.

        Args:
            new_items (List[Item]): A list of new items to be loaded.
            replace (bool, optional): If True, replaces the current items; if False, appends the new items. Defaults to True.
        """
        if replace:
            self.items = list(new_items)
        else:
            self.items.extend(list(new_items))

    def clear_items(self) -> None:
        """
        Clear all items from the matcher.
        """
        self.items.clear()

    def get_all_items(self) -> List[Item]:
        """
        Get all items currently stored in the matcher.

        Returns:
            List[Item]: List of all items.
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
        highest_score = 0.0

        for item in self.items:
            trade_similarity = self.calculate_similarity(data.trade, item.trade)
            uom_similarity = self.calculate_similarity(
                data.unit_of_measure, item.unit_of_measure
            )

            # Weighted score
            similarity_score = (trade_similarity * 0.7) + (uom_similarity * 0.3)

            if item and similarity_score > highest_score:
                highest_score = similarity_score
                best_match = item

        return {"best_match": best_match, "highest_score": highest_score}
