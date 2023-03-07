"""Module for all CASBench exceptions."""


class CASBenchError(Exception):
    """Superclass for all CASBench exceptions."""

    pass


class InvalidLexemeError(CASBenchError):
    """Raised when a :class:`Lexer` encounters a lexeme that can't be tokenized."""

    pass
