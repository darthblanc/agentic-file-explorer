from difflib import SequenceMatcher
from typing import Dict, List
from string_functions import strip_base_directory

def isEqual(target: str, candidate: str) -> bool:
    return target == candidate

def isApproximatelyEqual(target: str, candidate: str) -> bool:
    return SequenceMatcher(None, target, candidate).ratio() > 0.8

def compare(directory: str, target: str, candidate: str, approximate_search: bool, results: Dict[str, List[str]]) -> None:
    if isEqual(target, candidate):
            results["match"].append(strip_base_directory(f"{directory}/{candidate}"))
    else:
        if approximate_search:
            if isApproximatelyEqual(target, candidate):
                results["fuzzy"].append(strip_base_directory(f"{directory}/{candidate}"))

