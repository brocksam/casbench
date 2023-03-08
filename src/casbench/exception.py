"""Module for all CASBench exceptions."""


class CASBenchError(Exception):
    """Superclass for all CASBench exceptions."""

    pass


class InvalidLexemeError(CASBenchError):
    """Raised when a :class:`Lexer` encounters a lexeme that can't be tokenized."""

    pass


class UnexpectedTokenError(CASBenchError):
    """Raised when a :class:`Parser` encounters a :class:`Token` that's invalid grammar."""

    pass


class ExhaustedTokensError(CASBenchError):
    """Raised when a :class:`Parser` unexpectedly runs out of :class:`Token` instances."""

    pass
