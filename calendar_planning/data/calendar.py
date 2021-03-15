from typing import List, Dict
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Calendar:
    name: str
    day_start_time: int
    day_end_time: int
    daily_load: int
