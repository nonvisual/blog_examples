import hypothesis.strategies as st


@st.composite
def profits(draw, length):
    return draw(
        st.lists(
            st.floats(min_value=0, max_value=50.0), min_size=length, max_size=length
        )
    )


@st.composite
def weights(draw, length):
    return draw(
        st.lists(
            st.floats(min_value=0, max_value=10.0), min_size=length, max_size=length
        )
    )


@st.composite
def classes(draw, length, num_classes):
    return draw(
        st.lists(
            st.integers(min_value=0, max_value=num_classes),
            min_size=length,
            max_size=length,
        )
    )


@st.composite
def generate_data(draw, length=20, num_classes=10):
    profits_data = draw(profits(length))
    weights_data = draw(weights(length))
    classes_data = draw(classes(length, num_classes))

    return profits_data, weights_data, classes_data
