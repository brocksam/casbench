"""Tests for the ``casbench.lexer`` module."""

from __future__ import annotations

import pytest

from casbench.exception import InvalidLexemeError
from casbench.lexer import (
    Lexer,
    Token,
    TokenType,
)


class TestTokenType:
    """Tests for the ``TokenType`` enumeration."""

    @staticmethod
    def test_fields() -> None:
        """Enumeration has expected fields."""
        expected_fields = (
            "identifier",
            "integer_literal",
            "float_literal",
            "left_parenthesis",
            "right_parenthesis",
            "comma",
            "equal_equal",
            "end_of_file",
        )
        for expected_field in expected_fields:
            assert hasattr(TokenType, expected_field)
        assert len(TokenType) == len(expected_fields)


class TestToken:
    """Tests for the ``Token`` class."""

    @staticmethod
    @pytest.mark.parametrize(
        "token_type, lexeme",
        [
            (TokenType.identifier, "f"),
            (TokenType.left_parenthesis, "("),
            (TokenType.right_parenthesis, ")"),
            (TokenType.comma, ","),
            (TokenType.equal_equal, "=="),
            (TokenType.end_of_file, None),
        ]
    )
    def test_instantiate_token(token_type: TokenType, lexeme: str) -> None:
        """``Token`` instances of different types are tokenized correctly."""
        token = Token(
            token_type=token_type,
            lexeme=lexeme,
            literal=None,
            line=0,
            column=0,
        )

        assert hasattr(token, "token_type")
        assert token.token_type == token_type

        assert hasattr(token, "lexeme")
        assert token.lexeme == lexeme

        assert hasattr(token, "literal")
        assert token.literal is None

        assert hasattr(token, "line")
        assert token.line == 0

        assert hasattr(token, "column")
        assert token.column == 0

    @staticmethod
    @pytest.mark.parametrize(
        "token_type, lexeme, literal",
        [
            (TokenType.integer_literal, "10", 10),
            (TokenType.float_literal, "0.0", 0.0),
        ]
    )
    def test_instantiate_literal_token(
        token_type: TokenType,
        lexeme: str,
        literal: int | float | None,
    ) -> None:
        """``Token`` instances of literal types are tokenized correctly."""
        token = Token(
            token_type=token_type,
            lexeme=lexeme,
            literal=literal,
            line=0,
            column=0,
        )

        assert hasattr(token, "token_type")
        assert token.token_type == token_type

        assert hasattr(token, "lexeme")
        assert token.lexeme == lexeme

        assert hasattr(token, "literal")
        assert token.literal == literal

        assert hasattr(token, "line")
        assert token.line == 0

        assert hasattr(token, "column")
        assert token.column == 0


class TestLexer:
    """Tests for the ``Lexer`` class."""

    @staticmethod
    @pytest.mark.parametrize(
        "source",
        [
            "_",
            "0.0.0",
            "100_000",
        ],
    )
    def test_invalid_syntax_raises_unexpected_token_error(source: str) -> None:
        """``InvalidLexemeError`` raised when invalid/unsupported tokens encountered."""
        lexer = Lexer(source)
        with pytest.raises(InvalidLexemeError):
            _ = lexer.tokens

    @staticmethod
    @pytest.mark.parametrize(
        "source, expected_tokens",
        [
            ("", [Token(TokenType.end_of_file, None, line=0, column=0)]),
            ("      ", [Token(TokenType.end_of_file, None, line=0, column=6)]),
            (
                "f",
                [
                    Token(TokenType.identifier, "f", line=0, column=0),
                    Token(TokenType.end_of_file, None, line=0, column=1),
                ],
            ),
            (
                "sin",
                [
                    Token(TokenType.identifier, "sin", line=0, column=0),
                    Token(TokenType.end_of_file, None, line=0, column=3),
                ],
            ),
            (
                "0",
                [
                    Token(TokenType.integer_literal, "0", line=0, column=0, literal=0),
                    Token(TokenType.end_of_file, None, line=0, column=1),
                ],
            ),
            (
                "99",
                [
                    Token(TokenType.integer_literal, "99", line=0, column=0, literal=99),
                    Token(TokenType.end_of_file, None, line=0, column=2),
                ],
            ),
            (
                "1.0",
                [
                    Token(TokenType.float_literal, "1.0", line=0, column=0, literal=1.0),
                    Token(TokenType.end_of_file, None, line=0, column=3),
                ],
            ),
            (
                "10.00",
                [
                    Token(TokenType.float_literal, "10.00", line=0, column=0, literal=10.0),
                    Token(TokenType.end_of_file, None, line=0, column=5),
                ],
            ),
            (
                "99.999",
                [
                    Token(TokenType.float_literal, "99.999", line=0, column=0, literal=99.999),
                    Token(TokenType.end_of_file, None, line=0, column=6),
                ],
            ),
            (
                "(",
                [
                    Token(TokenType.left_parenthesis, "(", line=0, column=0),
                    Token(TokenType.end_of_file, None, line=0, column=1),
                ],
            ),
            (
                ")",
                [
                    Token(TokenType.right_parenthesis, ")", line=0, column=0),
                    Token(TokenType.end_of_file, None, line=0, column=1),
                ],
            ),
            (
                ",",
                [
                    Token(TokenType.comma, ",", line=0, column=0),
                    Token(TokenType.end_of_file, None, line=0, column=1),
                ],
            ),
            (
                " , ",
                [
                    Token(TokenType.comma, ",", line=0, column=1),
                    Token(TokenType.end_of_file, None, line=0, column=3),
                ],
            ),
        ],
    )
    def test_single_token_statement(source: str, expected_tokens: list[Token]) -> None:
        """Single-token statements are tokenized correctly."""
        lexer = Lexer(source)
        assert lexer.tokens == expected_tokens

    @staticmethod
    @pytest.mark.parametrize(
        "source, expected_tokens",
        [
            (
                "sin(x)",
                [
                    Token(TokenType.identifier, "sin", line=0, column=0),
                    Token(TokenType.left_parenthesis, "(", line=0, column=3),
                    Token(TokenType.identifier, "x", line=0, column=4),
                    Token(TokenType.right_parenthesis, ")", line=0, column=5),
                    Token(TokenType.end_of_file, None, line=0, column=6),
                ],
            ),
            (
                "diff(expr, x)",
                [
                    Token(TokenType.identifier, "diff", line=0, column=0),
                    Token(TokenType.left_parenthesis, "(", line=0, column=4),
                    Token(TokenType.identifier, "expr", line=0, column=5),
                    Token(TokenType.comma, ",", line=0, column=9),
                    Token(TokenType.identifier, "x", line=0, column=11),
                    Token(TokenType.right_parenthesis, ")", line=0, column=12),
                    Token(TokenType.end_of_file, None, line=0, column=13),
                ],
            ),
            (
                "diff(expr, x, 10)",
                [
                    Token(TokenType.identifier, "diff", line=0, column=0),
                    Token(TokenType.left_parenthesis, "(", line=0, column=4),
                    Token(TokenType.identifier, "expr", line=0, column=5),
                    Token(TokenType.comma, ",", line=0, column=9),
                    Token(TokenType.identifier, "x", line=0, column=11),
                    Token(TokenType.comma, ",", line=0, column=12),
                    Token(TokenType.integer_literal, "10", line=0, column=14, literal=10),
                    Token(TokenType.right_parenthesis, ")", line=0, column=16),
                    Token(TokenType.end_of_file, None, line=0, column=17),
                ],
            ),
            (
                "evalf(subs(result, x, 1.0)) == 0.5678",
                [
                    Token(TokenType.identifier, "evalf", line=0, column=0),
                    Token(TokenType.left_parenthesis, "(", line=0, column=5),
                    Token(TokenType.identifier, "subs", line=0, column=6),
                    Token(TokenType.left_parenthesis, "(", line=0, column=10),
                    Token(TokenType.identifier, "result", line=0, column=11),
                    Token(TokenType.comma, ",", line=0, column=17),
                    Token(TokenType.identifier, "x", line=0, column=19),
                    Token(TokenType.comma, ",", line=0, column=20),
                    Token(TokenType.float_literal, "1.0", line=0, column=22, literal=1.0),
                    Token(TokenType.right_parenthesis, ")", line=0, column=25),
                    Token(TokenType.right_parenthesis, ")", line=0, column=26),
                    Token(TokenType.equal_equal, "==", line=0, column=28),
                    Token(TokenType.float_literal, "0.5678", line=0, column=31, literal=0.5678),
                    Token(TokenType.end_of_file, None, line=0, column=37),
                ]
            ),
        ],
    )
    def test_multiple_token_statement(source: str, expected_tokens: list[Token]) -> None:
        """Multiple-token statements are tokenized correctly."""
        lexer = Lexer(source)
        assert lexer.tokens == expected_tokens
