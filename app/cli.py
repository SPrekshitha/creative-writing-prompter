import argparse

from app.core import milestone_1, milestone_2, milestone_4


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
        help="Generate story continuation."
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

    args = parser.parse_args(argv)

    if args.command == "hello":
        print("Creative Writing Prompter is ready!")

    elif args.command == "generate":

        tokens = milestone_1()
        model = milestone_2(tokens)
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


if __name__ == "__main__":
    main()