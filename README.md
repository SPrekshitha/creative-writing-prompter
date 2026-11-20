# Creative Writing Prompter

[![Built with askThili](https://ask.thili.ai/api/v1/public/projects/a9u2865z8e/badge.svg)](https://ask.thili.ai/b/a9u2865z8e)

Creative Writing Prompter is a CLI tool for aspiring writers. It helps overcome writer's block by providing context-aware next-word suggestions, sampled from a short story corpus, to aid in story development.

## What you are building

**Goal.** You will build a command-line tool that suggests context-aware next words to help aspiring writers develop stories and overcome writer's block.

**Done when.** The tool successfully takes user input, uses the n-gram prediction engine with smoothing to suggest next words, and generates text by sampling from the model.

## Milestones

Tick these off as you go, and commit after each one.

- [ ] **1. Prepare a text corpus of short stories.**  
      Hint: Text preprocessing and tokenization.
- [ ] **2. Implement n-gram counting and maximum-likelihood probabilities.**  
      Hint: N-gram counting and maximum likelihood estimation.
- [ ] **3. Add add-k smoothing to handle unseen n-grams.**  
      Hint: Add-k smoothing.
- [ ] **4. Develop a function to generate text by sampling from the model.**  
      Hint: Sampling from a probability distribution.
- [ ] **5. Create a CLI interface for users to input text and get suggestions.**  
      Hint: CLI interaction and user input handling.

## Run it

You need Python 3.12 and git.

```bash
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then choose a model; see the comments inside
python -m app.cli hello
pytest
```

Your work goes in `app/core.py` (one stub per milestone) and `tests/test_core.py`. The first tests pass already; they
check the plumbing.

## Settings and secrets

Model settings live in `.env`, which is ignored by git. **Never commit `.env` or paste a key into code.** If a key ever
reaches GitHub, treat it as leaked and make a new one.

## Stretch ideas

- Allowing users to specify the number of next-word suggestions to display.
- Adding a feature to generate a longer sequence of words based on the current context.
- Implementing a way to save and load the trained model to avoid reprocessing the corpus.
