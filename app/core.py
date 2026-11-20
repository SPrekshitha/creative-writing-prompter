import re
import random
from collections import Counter, defaultdict


# Small sample corpus containing three short stories.
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


# Milestone 1: Tokenization
def milestone_1(corpus=None):
    if corpus is None:
        corpus = CORPUS

    if isinstance(corpus, str):
        corpus = [corpus]

    tokens = []

    for story in corpus:
        words = re.findall(r"[a-zA-Z']+", story.lower())
        tokens.extend(words)

    if not tokens:
        raise ValueError("The corpus cannot be empty.")

    return tokens


# Milestone 2: N-gram counting
def milestone_2(tokens, n=3):
    if n < 2:
        raise ValueError("n must be at least 2.")

    if len(tokens) < n:
        raise ValueError("Not enough tokens to build the model.")

    context_counts = defaultdict(Counter)

    for i in range(len(tokens) - n + 1):
        context = tuple(tokens[i:i + n - 1])
        next_word = tokens[i + n - 1]

        context_counts[context][next_word] += 1

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

    rng = random.Random(seed)

    generated = seed_text.lower().split()

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


# Milestone 5: Interactive next-word suggestions
def milestone_5():
    print("\n====================================")
    print("     CREATIVE WRITING PROMPTER")
    print("====================================")

    tokens = milestone_1()
    vocabulary = set(tokens)
    model = milestone_2(tokens)

    while True:
        text = input("\nEnter your sentence (or 'exit'): ").strip()

        if text.lower() == "exit":
            print("Thank you for using Creative Writing Prompter!")
            break

        words = re.findall(r"[a-zA-Z']+", text.lower())

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

        generate = input("\nGenerate a continuation? (yes/no): ")

        if generate.lower() == "yes":
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