from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Event:
    name: str
    min_time: int
    max_time: int
    possible_days: List[int]
    importance: int
    duration: int
    repetition: int


class EmptyEvent(Event):
    def __init__(self):
        self.name = ""
        self.min_time = 0
        self.max_time = 24
        self.possible_days = range(7)
        self.importance = 0
        self.duration = 0
