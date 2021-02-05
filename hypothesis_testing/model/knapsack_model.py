import pulp
from typing import List


def create_knapsack_problem(
    profits: List[float], weights: List[float], capacity: float
):
    index = range(len(profits))

    model = pulp.LpProblem("knapsack_problem", pulp.constants.LpMaximize)
    decision_vars = pulp.LpVariable.dicts("decisions", index, 0, 1, pulp.LpInteger)

    objective = pulp.lpSum([decision_vars[t] * profits[t] for t in index])
    model += objective

    capacity_constraint = (
        pulp.lpSum([decision_vars[t] * weights[t] for t in index]) <= capacity
    )
    model += capacity_constraint

    return model, decision_vars
