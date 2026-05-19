"""
text_preprocessor.py — Text cleaning and normalization utilities.

All text fed into the AI model must be preprocessed consistently.
These functions are pure (no side effects) and can be reused in
training pipelines, API handlers, and batch jobs.

Planned functions:
  - clean(text)       : remove HTML tags, special characters, excess whitespace
  - normalize(text)   : lowercase, unicode normalization, URL/email masking
  - tokenize(text)    : split into tokens (word-level or subword)
  - remove_stopwords  : filter common words that carry no scam signal
"""


def clean(text: str) -> str:
    """Remove noise from raw input text (HTML, extra whitespace, etc.)."""
    # TODO: implement cleaning logic
    raise NotImplementedError


def normalize(text: str) -> str:
    """Lowercase and normalize unicode characters."""
    # TODO: implement normalization
    raise NotImplementedError


def preprocess(text: str) -> str:
    """Full pipeline: clean → normalize. Main entry point for preprocessing."""
    # TODO: chain clean() and normalize()
    raise NotImplementedError
