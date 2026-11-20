import re
import random
from collections import Counter, defaultdict

# Three original sample stories used as the training corpus.
CORPUS = [
    """
    Once upon a time, there lived a young princess.
    She lived in a beautiful castle near a forest.
    The princess loved reading books and exploring the forest.
    One day, she discovered a magical golden key.
    The key opened a mysterious door in the forest.
    Behind the door, she found a wonderful kingdom.
    """,

    """
    A little boy lived in a small village.
    He loved playing with his friends.
    Every morning, he walked through the green forest.
    One day, he found a little bird.
    The bird was sitting under a large tree.
    The boy helped the bird return to its nest.
    """,

    """
    There was once a brave knight.
    The knight travelled across the kingdom.
    He wanted to find a hidden treasure.
    After many days, he reached a dark cave.
    Inside the cave, he discovered a golden crown.
    The crown belonged to the king.
    """
]


def tokenize(text):
    """Convert text into lowercase word tokens."""
    return re.findall(r"[a-zA-Z']+", text.lower())


# Milestone 1: Tokenization
def milestone_1(corpus=None, preserve_stories=False):
    if corpus is None:
        corpus = CORPUS

    if isinstance(corpus, str):
        corpus = [corpus]

    stories = [
        tokenize(story)
        for story in corpus
    ]

    stories = [story for story in stories if story]

    if not stories:
        raise ValueError("The corpus cannot be empty.")

    if preserve_stories:
        return stories

    return [
        word
        for story in stories
        for word in story
    ]


# Milestone 2: N-gram counting
def milestone_2(tokens, n=3):
    if n < 2:
        raise ValueError("n must be at least 2.")

    if not tokens:
        raise ValueError("Tokens cannot be empty.")

    # Accept either one token sequence or multiple separate stories.
    if isinstance(tokens[0], (list, tuple)):
        sequences = tokens
    else:
        sequences = [tokens]

    context_counts = defaultdict(Counter)

    for sequence in sequences:
        if len(sequence) < n:
            continue

        for i in range(len(sequence) - n + 1):
            context = tuple(sequence[i:i + n - 1])
            next_word = sequence[i + n - 1]

            context_counts[context][next_word] += 1

    if not context_counts:
        raise ValueError("Not enough tokens to build the model.")

    return dict(context_counts)


# Milestone 3: Add-k smoothing
def milestone_3(context, model, vocabulary, k=1.0):
    if k <= 0:
        raise ValueError("k must be greater than zero.")

    if not vocabulary:
        raise ValueError("Vocabulary cannot be empty.")

    context = tuple(context)
    observed = model.get(context, {})

    total = sum(observed.values())
    denominator = total + k * len(vocabulary)

    return {
        word: (observed.get(word, 0) + k) / denominator
        for word in sorted(vocabulary)
    }


# Milestone 4: Reproducible text generation
def milestone_4(
    tokens,
    model,
    vocabulary,
    seed_text,
    length=20,
    k=1.0,
    seed=None
):
    if length < 0:
        raise ValueError("Length cannot be negative.")

    if not vocabulary:
        raise ValueError("Vocabulary cannot be empty.")

    if k <= 0:
        raise ValueError("k must be greater than zero.")

    rng = random.Random(seed)

    generated = tokenize(seed_text)

    if not generated:
        generated = ["once", "upon"]

    for _ in range(length):
        context = tuple(generated[-2:])

        distribution = milestone_3(
            context,
            model,
            vocabulary,
            k
        )

        words = list(distribution.keys())
        weights = list(distribution.values())

        next_word = rng.choices(
            words,
            weights=weights,
            k=1
        )[0]

        generated.append(next_word)

    return " ".join(generated)


# Evaluation: Compare trigram prediction with a unigram baseline.
def evaluate_model(stories, n=3):
    if len(stories) < 2:
        raise ValueError(
            "At least two stories are required for evaluation."
        )

    if n != 3:
        raise ValueError("This evaluation currently supports trigrams.")

    training_stories = stories[:-1]
    test_story = stories[-1]

    training_tokens = [
        word
        for story in training_stories
        for word in story
    ]

    vocabulary = set(training_tokens)

    model = milestone_2(training_stories, n=n)

    unigram_counts = Counter(training_tokens)

    trigram_correct = 0
    baseline_correct = 0
    evaluated = 0

    for i in range(2, len(test_story)):
        context = tuple(test_story[i - 2:i])
        actual = test_story[i]

        if actual not in vocabulary:
            continue

        probabilities = milestone_3(
            context,
            model,
            vocabulary
        )

        prediction = max(
            probabilities,
            key=probabilities.get
        )

        baseline_prediction = unigram_counts.most_common(1)[0][0]

        trigram_correct += prediction == actual
        baseline_correct += baseline_prediction == actual
        evaluated += 1

    if evaluated == 0:
        raise ValueError(
            "No test words were in the training vocabulary."
        )

    return {
        "evaluated_tokens": evaluated,
        "trigram_accuracy": trigram_correct / evaluated,
        "unigram_accuracy": baseline_correct / evaluated
    }


# Milestone 5: Interactive next-word suggestions
def milestone_5():
    print("\n====================================")
    print("     CREATIVE WRITING PROMPTER")
    print("====================================")

    stories = milestone_1(preserve_stories=True)

    tokens = [
        word
        for story in stories
        for word in story
    ]

    vocabulary = set(tokens)
    model = milestone_2(stories)

    while True:
        text = input(
            "\nEnter your sentence (or 'exit'): "
        ).strip()

        if text.lower() == "exit":
            print(
                "Thank you for using Creative Writing Prompter!"
            )
            break

        words = tokenize(text)

        if not words:
            print("Please enter some words.")
            continue

        context = tuple(words[-2:])

        suggestions = milestone_3(
            context,
            model,
            vocabulary
        )

        print("\nNext-word suggestions:")

        top_words = sorted(
            suggestions.items(),
            key=lambda item: item[1],
            reverse=True
        )[:5]

        for word, probability in top_words:
            print(f"{word}: {probability:.4f}")

        generate = input(
            "\nGenerate a continuation? (yes/no): "
        ).strip().lower()

        if generate == "yes":
            generated = milestone_4(
                tokens,
                model,
                vocabulary,
                text,
                length=10,
                seed=42
            )

            print("\nGenerated story:")
            print(generated)