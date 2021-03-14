import plotly.graph_objects as go

from data.calendar import Calendar
from data.event import Event, EmptyEvent
from typing import List, Dict


def draw_daily_events(
    fig,
    x_offset,
    y_offset,
    calendar: Calendar,
    daily_assignment: Dict[int, Event],
    day,
    color,
):
    hours_num = calendar.day_end_time - calendar.day_start_time
    max_height = 3.0
    cell_width = 1.0
    cell_height = max_height / hours_num

    hourly_assignment = {}
    for i in range(calendar.day_start_time, calendar.day_end_time + 1):
        if i in daily_assignment:
            event = daily_assignment[i]
            for j in range(i, i + event.duration):
                hourly_assignment[j] = event

    for i in range(calendar.day_start_time, calendar.day_end_time + 1):

        hour = f"{i}:00"
        cell_color = color if i in hourly_assignment else "grey"
        position_offset = i - calendar.day_start_time
        fig.add_shape(
            type="rect",
            xref="paper",
            yref="paper",
            x0=x_offset,
            y0=y_offset + position_offset * cell_height,
            x1=x_offset + cell_width,
            y1=y_offset + (position_offset + 1) * cell_height,
            line=dict(
                color="LightSeaGreen",
                width=3,
            ),
            fillcolor=cell_color,
        )

        event = hourly_assignment.get(i, EmptyEvent())
        text = event.name
        fig.add_trace(
            go.Scatter(
                x=[x_offset + 0.1],
                y=[y_offset + (position_offset) * cell_height + cell_height / 2],
                text=f"{hour} {text}",
                mode="text",
                textposition="bottom right",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=[x_offset + 0.2],
            y=[y_offset + (hours_num) * cell_height + 0.6],
            text=day,
            mode="text",
            textposition="bottom center",
        )
    )
