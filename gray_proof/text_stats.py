"""Tiny text helpers for the agent_memory demo."""


def word_count(text: str) -> int:
    """Return the number of whitespace-separated words in text.
    word_count("hello world") -> 2 ; word_count("") -> 0
    """
    return len(text.split())
