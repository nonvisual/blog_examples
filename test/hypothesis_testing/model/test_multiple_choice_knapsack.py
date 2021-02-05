from hypothesis import settings, given, reproduce_failure
from datetime import timedelta
from pulp import LpStatus
from test.hypothesis_testing.model.data_generator import generate_data
from hypothesis_testing.model.multiple_choice_knapsack_model import (
    create_multiple_choice_knapsack_problem,
)


@settings(max_examples=8, print_blob=True, deadline=timedelta(seconds=20))
@given(generate_data(num_classes=1))
def test_multiple_choice_knapsack_model_feasible(data):
    profits, weights, classes = data
    model, _ = create_multiple_choice_knapsack_problem(profits, weights, classes, 10)
    status = model.solve()

    assert LpStatus[status] == "Optimal", "All problem instances are feasible"


@settings(max_examples=8, print_blob=True, deadline=timedelta(seconds=20))
@given(generate_data(length=10, num_classes=2))
def test_knapsack_model_respects_classes_constraint(data):
    profits, weights, classes = data
    index = range(len(profits))
    capacity = 10
    model, decision_vars = create_multiple_choice_knapsack_problem(
        profits, weights, classes, capacity
    )
    status = model.solve()
    solution = [
        decision_vars[t].varValue if decision_vars[t].varValue is not None else 0
        for t in index
    ]

    classes_dict = dict()
    for i in index:
        if classes[i] in classes_dict:
            classes_dict[classes[i]].append(index)
        else:
            classes_dict[classes[i]] = [i]

    for c in classes_dict:
        num_chosen = sum(
            [
                decision_vars[t].varValue
                if (decision_vars[t].varValue is not None) and (t in classes_dict[c])
                else 0
                for t in index
            ]
        )
        assert (
            num_chosen <= 1
        ), "We cannot select more than one element of te same class"
