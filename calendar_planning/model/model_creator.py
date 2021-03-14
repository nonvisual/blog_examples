from ortools.linear_solver import pywraplp

days = 7
def create_model(calendars:List[Calendar], events:List[Event],  fixed_events: Dict[Calendar, List[Event]]):

    calendar_timeslots = [range(c.day_start_time,c.day_end_time+1) for c in calendars]
    z = { (i,c,d,t): solver.IntVar(0, 1, f'z_{i}_{c}_{d}_{t}') 
                 if (d in event.possible_days) and (t<=event.max_time) and (t>=event.min_time)
                 else 0
     
                 for i,event in enumerate(events) 
                 for c,_ in enumerate(calendars) for d in range(days)  for t in calendar_timeslots[c]}

