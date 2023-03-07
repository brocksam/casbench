"""Functionality for lexing expressions in CASBench benchmark definitions."""

from __future__ import annotations

import dataclasses
import enum
import functools

from casbench.exception import InvalidLexemeError


@enum.unique
class TokenType(enum.Enum):
    """Enumeration for token types to be encountered by the ``Lexer``."""

    identifier = enum.auto()
    integer_literal = enum.auto()
    float_literal = enum.auto()
    left_parenthesis = enum.auto()
    right_parenthesis = enum.auto()
    comma = enum.auto()
    equal_equal = enum.auto()
    end_of_file = enum.auto()


@dataclasses.dataclass
class Token:
    """Tokens and their associated data to be encountered by the ``Lexer``."""

    token_type: TokenType
    lexeme: str | None
    line: int
    column: int
    literal: int | float | None = None


class Lexer:
    """Lexer that tokenizes source code into ``Token`` objects."""

    def __init__(self, source: str) -> None:
        """Initialize the ``Lexer`` with its ``source`` attribute."""
        self._source = source

    @property
    def source(self) -> str:
        """The source code to be tokenized by the lexer."""
        return self._source

    @functools.cached_property
    def tokens(self) -> list[Token]:
        """The tokens encountered by the lexer during tokenization."""
        return self._tokenize()

    def _tokenize(self) -> list[Token]:
        """Tokenize the source code into a series of ``Token`` objects."""

        def invalid_lexeme(current: str, line: int, column: int, index: int) -> None:
            """Raise ``InvalidLexemeError`` for an unrecognized/invalid lexeme."""
            msg = (
                f"Invalid lexeme {current} encountered on line {line} at "
                f"column {column} (index {index}) during lexing"
            )
            raise InvalidLexemeError(msg)

        line = 0
        column = 0
        index = 0
        literal = None

        tokens = []

        while index < len(self.source):
            current = self.source[index]

            # Encountered whitespace that can be ignored (` `)
            if current == " ":
                column += 1
                index += 1
                continue

            # Encountered a candidate identifier
            elif current.isalpha():
                identifier = current
                length = 1
                while True:
                    if (index + length) >= len(self.source):
                        break
                    peek = self.source[index + length]
                    if not peek.isidentifier():
                        break
                    identifier += self.source[index + length]
                    length += 1
                token_type = TokenType.identifier
                lexeme = identifier

            # Encountered a candidate number (integer_literal or float_literal)
            elif current.isdigit():
                number = current
                length = 1
                has_decimal_point = False
                while True:
                    if (index + length) >= len(self.source):
                        break
                    peek = self.source[index + length]
                    if peek == ".":
                        if has_decimal_point:
                            invalid_lexeme(current, line, column, index)
                        has_decimal_point = True
                    elif peek.isalpha() or peek == "_":
                        invalid_lexeme(current, line, column, index)
                    elif peek.isnumeric():
                        pass
                    else:
                        break
                    number += peek
                    length += 1
                if has_decimal_point:
                    token_type = TokenType.float_literal
                    literal = float(number)
                else:
                    token_type = TokenType.integer_literal
                    literal = int(number)
                lexeme = number

            # Encountered a left parenthesis
            elif current == "(":
                token_type = TokenType.left_parenthesis
                lexeme = "("
                length = 1

            # Encountered a right parenthesis
            elif current == ")":
                token_type = TokenType.right_parenthesis
                lexeme = ")"
                length = 1

            # Encountered a comma
            elif current == ",":
                token_type=TokenType.comma
                lexeme = ","
                length = 1

            # Encountered a candidate comparison operator (only == supported)
            elif current == "=":
                if self.source[index + 1] == "=":
                    token_type = TokenType.equal_equal
                    lexeme = "=="
                    length = 2
                else:
                    invalid_lexeme(current, line, column, index)

            # No more possible valid token types
            else:
                invalid_lexeme(current, line, column, index)

            token = Token(
                token_type=token_type,
                lexeme=lexeme,
                line=line,
                column=column,
                literal=literal,
            )
            tokens.append(token)
            column += length
            index += length
            literal = None

        end_of_file_token = Token(
            token_type=TokenType.end_of_file,
            lexeme=None,
            line=line,
            column=column,
        )
        tokens.append(end_of_file_token)

        return tokens
