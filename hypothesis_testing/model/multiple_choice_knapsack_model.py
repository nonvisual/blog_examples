import pulp
from typing import List
from hypothesis_testing.model.knapsack_model import create_knapsack_problem


def create_multiple_choice_knapsack_problem(
    profits: List[float], weights: List[float], classes: List[int], capacity: float
):
    index = range(len(profits))

    classes_dict = dict()
    for i in index:
        if classes[i] in classes_dict:
            classes_dict[classes[i]].append(index)
        else:
            classes_dict[classes[i]] = [i]

    model, decision_vars = create_knapsack_problem(profits, weights, capacity)

    for c in classes_dict:
        class_constraint = (
            pulp.lpSum(
                [decision_vars[t] for t in index if t in classes_dict[classes[i]]]
            )
            <= 1
        )
        model += class_constraint
    return model, decision_vars
