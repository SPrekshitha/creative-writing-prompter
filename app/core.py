import re
import random
from collections import Counter, defaultdict


# Sample short-story corpus
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


# Milestone 1: Prepare and tokenize the text corpus.
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


# Milestone 2: N-gram counting and maximum likelihood estimation.
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

    probabilities = {}

    for context, next_words in context_counts.items():
        total = sum(next_words.values())

        probabilities[context] = {
            word: count / total
            for word, count in next_words.items()
        }

    return probabilities


# Milestone 3: Add-k smoothing.
def milestone_3(context, probabilities, vocabulary, k=1.0):
    if k <= 0:
        raise ValueError("k must be greater than zero.")

    if not vocabulary:
        raise ValueError("Vocabulary cannot be empty.")

    context = tuple(context)

    observed = probabilities.get(context, {})

    total = sum(observed.values())

    denominator = total + k * len(vocabulary)

    smoothed = {}

    for word in vocabulary:
        count = observed.get(word, 0)

        smoothed[word] = (count + k) / denominator

    return smoothed


# Milestone 4: Generate text by sampling from probabilities.
def milestone_4(tokens, probabilities, vocabulary, seed_text, length=20, k=1.0):
    if length < 0:
        raise ValueError("Length cannot be negative.")

    if not vocabulary:
        raise ValueError("Vocabulary cannot be empty.")

    n_minus_one = len(next(iter(probabilities))) if probabilities else 2

    generated = list(seed_text.lower().split())

    if not generated:
        generated = ["once", "upon"]

    while len(generated) < length + len(generated):
        context = tuple(generated[-n_minus_one:])

        distribution = milestone_3(
            context,
            probabilities,
            vocabulary,
            k
        )

        words = list(distribution.keys())
        weights = list(distribution.values())

        next_word = random.choices(words, weights=weights, k=1)[0]

        generated.append(next_word)

        if len(generated) >= length + len(seed_text.split()):
            break

    return " ".join(generated)


# Milestone 5: CLI support and next-word suggestions.
def milestone_5():
    print("\n====================================")
    print("     CREATIVE WRITING PROMPTER")
    print("====================================")

    tokens = milestone_1()

    vocabulary = sorted(set(tokens))

    probabilities = milestone_2(tokens, n=3)

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
            probabilities,
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
                probabilities,
                vocabulary,
                text,
                length=10
            )

            print("\nGenerated story:")
            print(generated)