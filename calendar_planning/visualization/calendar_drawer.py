import plotly.graph_objects as go

from data.calendar import Calendar
from data.event import Event
from typing import Dict
from visualization.event_drawer import draw_daily_events
def draw_calendar(calendar: Calendar, assignment: Dict[int,Dict[int, Event]], fig = None, y_offset=0):
    
    # Create figure
    fig = go.Figure() if fig is None else fig

    fig.update_xaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
    )

    fig.update_yaxes(
        showticklabels=False,
        showgrid=False,
        zeroline=False,
    )

    draw_daily_events(fig,0.1,y_offset,calendar,assignment[0], "Monday", "blue")

    draw_daily_events(fig,1.2,y_offset,calendar,assignment[1], "Tuesday", "red")

    draw_daily_events(fig,2.3,y_offset,calendar,assignment[2], "Wednesday", "green")

    draw_daily_events(fig,3.4,y_offset,calendar,assignment[3], "Thursday", "blue")

    draw_daily_events(fig,4.5,y_offset,calendar,assignment[4], "Friday", "red")


    fig.update_shapes(opacity=0.3, xref="x", yref="y")
    fig.update_layout(showlegend=False)

    fig.update_layout(
        margin=dict(l=20, r=20, b=100),
        height=600, width=800,
        plot_bgcolor="white",
        font=dict(
            size=9    )
    )

    return fig
