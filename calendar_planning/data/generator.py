import random
from data.calendar import Calendar
from data.event import Event
from typing import List, Dict, Tuple

FIXED_EVENT_NAMES = ["Lunch", "Training", "Language Course", "Weekly call with Ann", "Call with Fred", "Coffee Break"]
EVENT_NAMES = [
    "Clean the room",
    "Go for a walk",
    "Meditation",
    "Workout",
    "Make Homework",
    "Buy groceries",
    "Practice guitar",
    "Read Python book",
    "Read OR article",
]
CALENDAR_NAMES = ["Bob's Calendar", "V's Calendar", "Random name Calendar", "Bart"]


def generate_data(
    num_calendars: int, fixed_events_num: int, events_num: int, seed: int = 1125
) -> Tuple[List[Calendar], Dict[Calendar, List[Event]], List[Event]]:
    random.seed(seed)
    c_names = random.sample(CALENDAR_NAMES, num_calendars)
    calendars = []
    fixed_events = {}
    events = []
    for i in range(num_calendars):
        c = Calendar(
            name=c_names[i],
            day_start_time=random.randint(6, 9),
            day_end_time=random.randint(15, 20),
            daily_load=random.randint(6, 10),
        )
        calendars.append(c)
        fixed_events[c] = []

    for i in range(fixed_events_num):
        start_time = random.randint(8, 15)
        duration = random.randint(1, 2)
        fixed_event = Event(
            name=random.choice(FIXED_EVENT_NAMES),
            min_time=start_time,
            max_time=start_time + duration,
            possible_days=random.sample(range(5), 3),
            importance=1,
            duration=duration,
            repetition=random.randint(1, 5),
        )
        fixed_events[random.choice(calendars)].append(fixed_event)

    for i in range(events_num):
        start_time = random.randint(8, 15)
        end_time = min(24, start_time + random.randint(1, 8))
        duration = random.randint(1, 3)
        event = Event(
            name=random.choice(EVENT_NAMES),
            min_time=start_time,
            max_time=end_time,
            possible_days=random.sample(range(5), 3),
            importance=random.randint(1, 10),
            duration=duration,
            repetition=random.randint(1, 5),
        )
        events.append(event)

    return calendars, fixed_events, events
