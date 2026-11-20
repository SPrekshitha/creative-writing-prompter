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


def test_story_boundaries_are_preserved():
    stories = milestone_1(preserve_stories=True)

    model = milestone_2(stories)

    # A new story must not continue the previous story's context.
    assert ("kingdom", "a") not in model
    assert ("nest", "there") not in model


def test_milestone_2_supports_different_ngram_sizes():
    tokens = ["the", "small", "cat", "runs", "fast"]

    bigram_model = milestone_2(tokens, n=2)

    assert ("the",) in bigram_model
    assert bigram_model[("the",)]["small"] == 1


def test_milestone_4_rejects_negative_length():
    import pytest

    tokens = milestone_1()
    model = milestone_2(tokens)
    vocabulary = set(tokens)

    with pytest.raises(ValueError):
        milestone_4(
            tokens,
            model,
            vocabulary,
            "once upon",
            length=-1
        )


def test_model_evaluation():
    from app.core import evaluate_model

    stories = milestone_1(preserve_stories=True)

    results = evaluate_model(stories)

    assert results["evaluated_tokens"] > 0
    assert 0 <= results["trigram_accuracy"] <= 1
    assert 0 <= results["unigram_accuracy"] <= 1


def test_milestone_2_rejects_invalid_ngram_size():
    import pytest

    with pytest.raises(ValueError):
        milestone_2(["the", "cat"], n=1)


def test_milestone_3_calculates_add_k_probability():
    model = {
        ("the", "small"): {
            "cat": 2,
            "dog": 1
        }
    }

    probabilities = milestone_3(
        ("the", "small"),
        model,
        {"cat", "dog"},
        k=1
    )

    assert probabilities["cat"] == 3 / 5
    assert probabilities["dog"] == 2 / 5