import pytest
from app.core import milestone_1, milestone_2, milestone_3, milestone_4


def test_milestone_1():
    tokens = milestone_1()

    assert isinstance(tokens, list)
    assert len(tokens) > 0
    assert all(isinstance(word, str) for word in tokens)
    assert all(word == word.lower() for word in tokens)


def test_milestone_2():
    tokens = milestone_1()
    model = milestone_2(tokens)

    assert isinstance(model, dict)
    assert len(model) > 0

    for context, predictions in model.items():
        assert isinstance(context, tuple)
        assert isinstance(predictions, dict)
        assert abs(sum(predictions.values()) - 1.0) < 0.000001


def test_milestone_3():
    tokens = milestone_1()
    model = milestone_2(tokens)
    vocabulary = set(tokens)

    probabilities = milestone_3(("in", "a"), model, vocabulary)

    assert isinstance(probabilities, dict)
    assert set(probabilities.keys()) == vocabulary
    assert all(probability > 0 for probability in probabilities.values())
    assert abs(sum(probabilities.values()) - 1.0) < 0.000001


def test_milestone_4():
    tokens = milestone_1()
    model = milestone_2(tokens)
    vocabulary = set(tokens)

    generated = milestone_4(
        tokens,
        model,
        vocabulary,
        "once upon",
        10
    )

    assert isinstance(generated, str)
    assert len(generated.split()) >= 10
    assert generated.startswith("once upon")


def test_milestone_5():
    from app.cli import main

    main(["hello"])