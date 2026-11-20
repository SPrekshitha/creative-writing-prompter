from app.core import (
    milestone_1,
    milestone_2,
    milestone_3,
    milestone_4
)


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

    for context, counts in model.items():
        assert isinstance(context, tuple)
        assert isinstance(counts, dict)
        assert all(count > 0 for count in counts.values())


def test_milestone_3():
    tokens = milestone_1()
    model = milestone_2(tokens)
    vocabulary = set(tokens)

    probabilities = milestone_3(
        ("in", "a"),
        model,
        vocabulary
    )

    assert isinstance(probabilities, dict)
    assert set(probabilities.keys()) == vocabulary

    assert all(p > 0 for p in probabilities.values())

    assert abs(sum(probabilities.values()) - 1.0) < 0.000001


def test_milestone_3_unseen_context():
    tokens = milestone_1()
    model = milestone_2(tokens)
    vocabulary = set(tokens)

    probabilities = milestone_3(
        ("unknown", "context"),
        model,
        vocabulary
    )

    assert abs(sum(probabilities.values()) - 1.0) < 0.000001
    assert all(p > 0 for p in probabilities.values())


def test_milestone_4():
    tokens = milestone_1()
    model = milestone_2(tokens)
    vocabulary = set(tokens)

    generated = milestone_4(
        tokens,
        model,
        vocabulary,
        "once upon",
        length=10,
        seed=42
    )

    assert isinstance(generated, str)
    assert len(generated.split()) == 12
    assert generated.startswith("once upon")


def test_milestone_4_reproducibility():
    tokens = milestone_1()
    model = milestone_2(tokens)
    vocabulary = set(tokens)

    first = milestone_4(
        tokens, model, vocabulary,
        "once upon", 20, seed=42
    )

    second = milestone_4(
        tokens, model, vocabulary,
        "once upon", 20, seed=42
    )

    assert first == second


def test_milestone_5():
    from app.cli import main

    main(["hello"])