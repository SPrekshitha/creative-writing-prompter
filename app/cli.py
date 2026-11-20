import argparse

from app.core import (
    milestone_1,
    milestone_2,
    milestone_4,
    milestone_5,
    evaluate_model
)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="creative-writing-prompter",
        description="Generate creative writing suggestions using an n-gram model."
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True
    )

    sub.add_parser(
        "hello",
        help="Check that everything is working."
    )

    generate_parser = sub.add_parser(
        "generate",
        help="Generate a story continuation."
    )

    generate_parser.add_argument(
        "--prompt",
        default="once upon"
    )

    generate_parser.add_argument(
        "--length",
        type=int,
        default=20
    )

    generate_parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducible generation."
    )

    sub.add_parser(
        "interactive",
        help="Start interactive next-word suggestions."
    )

    sub.add_parser(
        "evaluate",
        help="Evaluate the model against a unigram baseline."
    )

    args = parser.parse_args(argv)

    if args.command == "hello":
        print("Creative Writing Prompter is ready!")

    elif args.command == "generate":
        stories = milestone_1(preserve_stories=True)

        tokens = [
            word
            for story in stories
            for word in story
        ]

        model = milestone_2(stories)
        vocabulary = set(tokens)

        result = milestone_4(
            tokens,
            model,
            vocabulary,
            args.prompt,
            args.length,
            seed=args.seed
        )

        print("\nGenerated story:")
        print(result)

    elif args.command == "interactive":
        milestone_5()

    elif args.command == "evaluate":
        stories = milestone_1(preserve_stories=True)
        results = evaluate_model(stories)

        print("\nModel Evaluation")
        print("----------------")
        print(f"Evaluated tokens: {results['evaluated_tokens']}")
        print(
            f"Trigram accuracy: "
            f"{results['trigram_accuracy']:.4f}"
        )
        print(
            f"Unigram baseline accuracy: "
            f"{results['unigram_accuracy']:.4f}"
        )


if __name__ == "__main__":
    main()