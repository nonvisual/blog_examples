from hypothesis import settings, given, reproduce_failure
from datetime import timedelta
from pulp import LpStatus
from test.hypothesis_testing.model.data_generator import generate_data
from hypothesis_testing.model.knapsack_model import create_knapsack_problem


@settings(max_examples=8, print_blob=True, deadline=timedelta(seconds=20))
@given(generate_data(num_classes=1))
def test_knapsack_model_optimal(data):
    profits, weights, _ = data
    model, _ = create_knapsack_problem(profits, weights, 10)
    status = model.solve()

    assert LpStatus[status] == "Optimal", "Al  small problem instances should be optimal"


@settings(max_examples=8, print_blob=True, deadline=timedelta(seconds=20))
@given(generate_data(length=10, num_classes=1))
def test_knapsack_model_respects_capacity(data):
    profits, weights, _ = data
    index = range(len(profits))
    capacity = 10
    model, decision_vars = create_knapsack_problem(profits, weights, capacity)
    status = model.solve()
    solution = [
        decision_vars[t].varValue if decision_vars[t].varValue is not None else 0
        for t in index
    ]

    total_weight = sum([solution[t] * weights[t] for t in index])
    assert total_weight <= 0, "We should not overweight our knapsack!"
