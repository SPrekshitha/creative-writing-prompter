[![Built with askThili](https://msrit.ask.thili.ai/api/v1/public/projects/a9u2865z8e/badge.svg)](https://msrit.ask.thili.ai/b/a9u2865z8e)
# Creative Writing Prompter

A Python-based next-word prediction and story-generation application built using an n-gram language model.

The application learns word sequences from a small collection of sample stories and uses probability-based sampling to generate creative writing continuations.

## Features

- Text tokenization and preprocessing.
- Trigram model construction.
- Support for different n-gram sizes.
- Maximum Likelihood Estimation (MLE).
- Add-k smoothing for unseen words and contexts.
- Next-word probability suggestions.
- Randomized story generation.
- Reproducible generation using a random seed.
- Interactive writing mode.
- Model evaluation against a unigram baseline.
- Automated tests using pytest.
- GitHub Actions continuous integration.

## Technologies Used

- Python 3.12
- Regular Expressions
- Python Collections
- Random module
- Argparse
- Pytest
- GitHub Actions

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
├── .gitignore
├── README.md
├── pytest.ini
└── requirements.txt
```

## Dataset

The project currently uses three short sample stories defined directly in `app/core.py`.

This is a small, handcrafted demonstration dataset rather than an external benchmark dataset.

The stories are converted into lowercase word tokens using regular expressions. Story boundaries are preserved when constructing the n-gram model so that words from separate stories are not incorrectly combined.

## Installation

Python 3.12 is recommended.

### Clone the repository

```powershell
git clone https://github.com/SPrekshitha/creative-writing-prompter.git
cd creative-writing-prompter
```

### Create a virtual environment

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

## Running the Application

### 1. Check the application

```powershell
python -m app.cli hello
```

Expected output:

```text
Creative Writing Prompter is ready!
```

### 2. Generate a story

```powershell
python -m app.cli generate --prompt "once upon" --length 10 --seed 42
```

The arguments are:

- `--prompt`: Starting text for generation.
- `--length`: Number of words to generate after the prompt.
- `--seed`: Optional random seed for reproducible generation.

Using the same prompt, length, and seed produces the same continuation.

### 3. Interactive writing mode

```powershell
python -m app.cli interactive
```

This mode allows users to:

- Enter a sentence or writing prompt.
- View the top five next-word suggestions.
- View the probability associated with each suggestion.
- Generate a continuation.
- Exit the application by entering `exit`.

### 4. Evaluate the model

```powershell
python -m app.cli evaluate
```

This command evaluates trigram prediction against a unigram baseline.

## Sample Results

### Story Generation

Command:

```powershell
python -m app.cli generate --prompt "once upon" --length 10 --seed 42
```

Observed output:

```text
Generated story:
once upon once across exploring days return playing under belonged inside after
```

### Model Evaluation

Command:

```powershell
python -m app.cli evaluate
```

Observed output:

```text
Model Evaluation
----------------
Evaluated tokens: 18
Trigram accuracy: 0.2222
Unigram baseline accuracy: 0.2222
```

The evaluation uses the final story as the test story and the preceding stories as training data. Only test words present in the training vocabulary are evaluated.

Both approaches achieved 22.22% top-1 accuracy on this small test sample. This result does not demonstrate that the trigram model outperforms the unigram baseline.

The evaluation is intended as a basic demonstration of model comparison, not as a statistically reliable benchmark.

## Model Methodology

### 1. Tokenization

The sample stories are converted into lowercase word tokens.

### 2. N-gram Counting

The model records how frequently a word follows a particular context.

For a trigram model, the previous two words are used as context.

### 3. Maximum Likelihood Estimation

For an observed context, the next-word probability is calculated using:

```text
P(word | context) =
count(context, word) / count(context)
```

### 4. Add-k Smoothing

Add-k smoothing assigns a positive probability to every word in the vocabulary, including words not previously observed after a particular context.

```text
P(word | context) =
(count(context, word) + k) /
(count(context) + k × vocabulary_size)
```

The default smoothing parameter is `k = 1`.

### 5. Text Generation

The application samples the next word from the calculated probability distribution and repeats the process to generate a continuation.

A local random-number generator supports reproducible generation through an optional seed.

### 6. Model Evaluation

The trigram model is compared against a unigram baseline that always predicts the most frequent word in the training data.

Top-1 prediction accuracy is calculated on eligible words in the held-out story.

## Running Tests

Run the test suite:

```powershell
pytest -v
```

The project currently includes 13 automated tests covering:

- Tokenization and preprocessing.
- N-gram counting.
- Probability normalization.
- Smoothing for unseen contexts.
- Story-boundary preservation.
- Different n-gram sizes.
- Story generation.
- Reproducibility with a fixed random seed.
- Input validation.
- Model evaluation.
- CLI execution.

## Continuous Integration

GitHub Actions automatically runs the test suite on pushes and pull requests using Python 3.12.

Workflow configuration:

```text
.github/workflows/ci.yml
```

## Limitations

- The training corpus contains only three short sample stories.
- The model has a limited vocabulary.
- Trigram prediction uses only the previous two words.
- The evaluation dataset is very small.
- The model does not understand meaning or context like a modern language model.
- Generated stories may be repetitive or grammatically incorrect.
- Predictions are limited to words in the training vocabulary.

## Future Improvements

- Train on a larger story dataset.
- Evaluate using multiple held-out stories.
- Add perplexity measurements.
- Improve sentence generation and punctuation handling.
- Explore higher-order n-gram models.

## Author

Sontam Prekshitha

GitHub Repository:

https://github.com/SPrekshitha/creative-writing-prompter
