import pulp


def create_multiple_choice_knapsack_problem(
    profits: List[double], weights: List[double], classes: List[int], capacity: double
):
    index = range(len(profits))

    classes_dict = dict()
    for i in index:
        if classes[i] in classes_dict:
            classes_dict[i].append(index)
        else:
            classes_dict[i] = [i]

    model = create_knapsack_problem(profits, weights, capacity)

    for c in classes_dict:
        class_constraint = (
            pulp.lpSum([decision_vars[t] for t in index if t in classes_dict[i]]) <= 1
        )
        model += class_constraint
    return model, decision_vars
