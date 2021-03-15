from ortools.linear_solver import pywraplp
from typing import List, Dict
from data.calendar import Calendar
from data.event import Event

days = 7


def create_model(
    calendars: List[Calendar],
    events: List[Event],
    fixed_events: Dict[Calendar, List[Event]],
):

    calendar_timeslots = [range(c.day_start_time, c.day_end_time + 1) for c in calendars]
    solver = pywraplp.Solver.CreateSolver("SCIP")

    z = {
        (i, c, d, t): solver.IntVar(0, 1, f"z_{i}_{c}_{d}_{t}")
        if (d in event.possible_days) and (t <= event.max_time) and (t >= event.min_time)
        else 0
        for i, event in enumerate(events)
        for c, _ in enumerate(calendars)
        for d in range(days)
        for t in calendar_timeslots[c]
    }

    add_one_event_per_timeslot_constraint(solver, z, calendars, events, fixed_events)
    add_daily_load_constraint(solver, z, calendars, events, fixed_events)

    add_event_repetition_constraint(solver, z, calendars, events)

    solver.Maximize(
        sum(
            z[i, c, d, t] * event.importance
            for i, event in enumerate(events)
            for c, _ in enumerate(calendars)
            for d in range(days)
            for t in calendar_timeslots[c]
        )
    )

    return solver, z


def add_event_repetition_constraint(solver, z, calendars: List[Calendar], events: List[Event]):
    # Event is assigned only # repetition times
    calendar_timeslots = [range(c.day_start_time, c.day_end_time + 1) for c in calendars]

    for i, event in enumerate(events):
        solver.Add(
            sum(
                z[i, c, d, t]
                for i, event in enumerate(events)
                for c, _ in enumerate(calendars)
                for d in range(days)
                for t in calendar_timeslots[c]
            )
            <= event.repetition
        )


def add_one_event_per_timeslot_constraint(
    solver, z, calendars: List[Calendar], events: List[Event], fixed_events: Dict[Calendar, List[Event]]
):
    # one event per time slot constraint
    calendar_timeslots = [range(c.day_start_time, c.day_end_time + 1) for c in calendars]

    for c, calendar in enumerate(calendars):
        for d in range(days):
            for t in calendar_timeslots[c]:
                number_fixed = len(
                    [
                        e
                        for e in fixed_events[calendar]
                        if ((d in e.possible_days) and (t >= e.min_time) and (t <= e.max_time))
                    ]
                )

                if number_fixed > 1:
                    print("we have more than 1 event assigned for the same time slot, relaxing the constraint")

                assigned_now = sum(z[i, c, d, t] for i, _ in enumerate(events))
                assigned_before = sum(
                    z[i, c, d, t2]
                    for i, event in enumerate(events)
                    for t2 in calendar_timeslots[c]
                    if (t2 < t) and (event.duration > t2 - t)
                )
                solver.Add(assigned_now + assigned_before <= max(1, number_fixed))


def add_daily_load_constraint(
    solver, z, calendars: List[Calendar], events: List[Event], fixed_events: Dict[Calendar, List[Event]]
):
    # daily load is respected
    calendar_timeslots = [range(c.day_start_time, c.day_end_time + 1) for c in calendars]

    for c, calendar in enumerate(calendars):
        for d in range(days):

            fixed_load = len(
                [
                    t
                    for e in fixed_events[calendar]
                    for t in calendar_timeslots[c]
                    if ((d in e.possible_days) and (t >= e.min_time) and (t <= e.max_time))
                ]
            )
            max_load = calendar.daily_load
            if fixed_load > calendar.daily_load:
                print(f"Fixed load for {calendar.name} and {d} is above the daily load limit. Relaxing it")
                max_load = fixed_load
            assigned_load = sum(
                z[i, c, d, t] * event.duration for i, event in enumerate(events) for t in calendar_timeslots[c]
            )

            solver.Add(assigned_load + fixed_load <= max_load)
