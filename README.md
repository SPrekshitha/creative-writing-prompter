# Creative Writing Prompter

A simple next-word prediction and story-generation application built from scratch using Python and a trigram language model.

The application learns word sequences from a small collection of sample stories and uses probability-based sampling to generate story continuations.

## Features

- Text tokenization and preprocessing.
- Trigram model construction.
- Maximum Likelihood Estimation (MLE).
- Add-k smoothing for unseen words and contexts.
- Next-word probability suggestions.
- Randomized story generation.
- Reproducible generation using a random seed.
- Command-line interface.
- Automated tests using pytest.

## Technologies Used

- Python 3.12
- Regular Expressions
- Python Collections
- Random module
- Argparse
- Pytest

## Project Structure

```text
creative-writing-prompter/
│
├── app/
│   ├── __init__.py
│   ├── core.py
│   └── cli.py
│
├── tests/
│   └── test_core.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env.example
├── .gitignore
├── README.md
├── pytest.ini
└── requirements.txt
```

## Dataset

The project currently uses three short sample stories defined directly in `app/core.py`.

The corpus is a small, handcrafted demonstration dataset. It is not an external benchmark dataset.

The text is converted to lowercase tokens using regular expressions.

## Installation

Python 3.12 is recommended.

Clone the repository:

```bash
git clone https://github.com/SPrekshitha/creative-writing-prompter.git
cd creative-writing-prompter
```

Create a virtual environment:

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the Application

Check that the application works:

```powershell
python -m app.cli hello
```

Expected output:

```text
Creative Writing Prompter is ready!
```

Generate a story:

```powershell
python -m app.cli generate --prompt "once upon" --length 20 --seed 42
```

The `--prompt` argument specifies the starting text.

The `--length` argument specifies the number of words to generate after the prompt.

The `--seed` argument makes generation reproducible. Running the same command with the same seed produces the same output.

## Sample Result

Command:

```powershell
python -m app.cli generate --prompt "once upon" --length 20 --seed 42
```

Observed output:

```text
Generated story:
once upon once across exploring days return playing under belonged inside after days large after day one loved days morning through a
```

## Model Methodology

### 1. Tokenization

The sample stories are converted into lowercase word tokens.

### 2. Trigram Model

The model uses the previous two words as context to estimate the probability of the next word.

### 3. Maximum Likelihood Estimation

For an observed context, next-word probabilities are calculated using:

P(word | context) = count(context, word) / count(context)

### 4. Add-k Smoothing

Add-k smoothing assigns a positive probability to every word in the vocabulary:

P(word | context) = (count(context, word) + k) / (count(context) + k × vocabulary_size)

The default smoothing parameter is k = 1.

### 5. Text Generation

The application samples the next word from the probability distribution and repeats this process to generate a continuation.

A local random-number generator accepts an optional seed for reproducible results.

## Evaluation and Baseline

The current implementation has been verified using automated unit tests.

The tests cover:

- Tokenization.
- N-gram counting.
- Probability normalization.
- Unseen-context smoothing.
- Text generation.
- Reproducibility with a fixed random seed.
- CLI execution.

A simple baseline for comparison would be selecting the most frequent next word for a given context instead of sampling from a probability distribution.

No formal held-out accuracy or perplexity benchmark has been established yet. The current test results demonstrate functional correctness, not predictive quality on unseen real-world text.

## Limitations

- The training corpus contains only three short sample stories.
- The model has a limited vocabulary.
- It predicts using only the previous two words.
- It does not understand meaning, context, or grammar like a modern language model.
- Generated stories can be repetitive or grammatically incorrect.
- Predictions are limited to words present in the training vocabulary.

## Running Tests

Run:

```powershell
pytest -v
```

The project includes seven automated tests covering its core functionality.

## Continuous Integration

GitHub Actions automatically runs the test suite on pushes and pull requests using Python 3.12.

Workflow configuration:

`.github/workflows/ci.yml`

## Future Improvements

- Train on a larger story dataset.
- Compare trigram predictions against a unigram baseline.
- Measure prediction accuracy and perplexity on held-out data.
- Add support for configurable n-gram sizes.
- Improve sentence generation and punctuation handling.

## Author

Prekshitha

GitHub Repository:

https://github.com/SPrekshitha/creative-writing-prompter