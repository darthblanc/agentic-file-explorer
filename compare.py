from difflib import SequenceMatcher
from typing import List

def isEqual(target: str, candidate: str) -> bool:
    return target == candidate

def isApproximatelyEqual(target: str, candidate: str) -> bool:
    return SequenceMatcher(None, target, candidate).ratio() > 0.8

def compare(target: str, candidate: str, approximate_search: bool, results: List[str]) -> None:
    if approximate_search:
        if isApproximatelyEqual(target, candidate):
            results.append(candidate)
    else:
        if isEqual(target, candidate):
            results.append(candidate)
