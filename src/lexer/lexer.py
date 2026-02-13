from enum import Enum, auto

class TokenType(Enum):
    IDENTIFIER = auto()
    NUMBER     = auto()
    STRING     = auto()
    TRUE       = auto()
    FALSE      = auto()
    PLUS       = auto()
    MINUS      = auto()
    STAR       = auto()
    SLASH      = auto()
    EQUAL      = auto()
    IF         = auto()
    ELSE       = auto()
    WHILE      = auto()
    DO         = auto()
    EQEQ       = auto()
    NEQ        = auto()
    LT         = auto()
    GT         = auto()
    LTE        = auto()
    GTE        = auto()
    LPAREN     = auto()
    RPAREN     = auto()
    NEWLINE    = auto()
    INDENT     = auto()
    DEDENT     = auto()
    EOF        = auto()

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type.name}:{self.value}"

class Lexer:
    def __init__(self, text):
        self.text = text.replace("\t", "    ")
        self.pos = 0
        self.current = self.text[0] if self.text else None

        self.indent_stack = [0]
        self.at_line_start = True
        self.pending_dedents = 0

        self.KEYWORDS = {
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "while": TokenType.WHILE,
            "do": TokenType.DO,
        }

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current = None
        else:
            self.current = self.text[self.pos]

    def peek(self):
        nxt = self.pos + 1
        if nxt >= len(self.text):
            return None
        return self.text[nxt]

    def skip_comment(self):
        while self.current and self.current != "\n":
            self.advance()

    def number(self):
        result = ""
        while self.current and self.current.isdigit():
            result += self.current
            self.advance()
        return Token(TokenType.NUMBER, int(result))

    def string(self):
        self.advance()
        result = ""
        while self.current and self.current != '"':
            result += self.current
            self.advance()
        self.advance()
        return Token(TokenType.STRING, result)

    def identifier(self):
        result = ""
        while self.current and (self.current.isalnum() or self.current == "_"):
            result += self.current
            self.advance()

        token_type = self.KEYWORDS.get(result, TokenType.IDENTIFIER)

        if token_type == TokenType.TRUE:
            return Token(token_type, True)
        if token_type == TokenType.FALSE:
            return Token(token_type, False)

        return Token(token_type, result)

    def handle_indentation(self):
        count = 0

        while self.current == " ":
            count += 1
            self.advance()

        if self.current == "\n" or self.current is None:
            return None

        if count % 4 != 0:
            raise Exception("Indentation must be multiple of 4 spaces")

        current_indent = self.indent_stack[-1]

        if count > current_indent:
            self.indent_stack.append(count)
            return Token(TokenType.INDENT, count)

        if count < current_indent:
            while self.indent_stack and count < self.indent_stack[-1]:
                self.indent_stack.pop()
                self.pending_dedents += 1

            if count != self.indent_stack[-1]:
                raise Exception("Invalid indentation level")

            return None

        return None

    def get_next_token(self):
        while True:

            if self.pending_dedents > 0:
                self.pending_dedents -= 1
                return Token(TokenType.DEDENT, None)

            if self.current is None:
                if len(self.indent_stack) > 1:
                    self.indent_stack.pop()
                    return Token(TokenType.DEDENT, None)
                return Token(TokenType.EOF, None)

            if self.current == "\n":
                self.advance()
                self.at_line_start = True
                return Token(TokenType.NEWLINE, "\n")

            if self.at_line_start:
                self.at_line_start = False
                indent_token = self.handle_indentation()
                if indent_token:
                    return indent_token
                continue

            if self.current == " ":
                self.advance()
                continue

            if self.current == "#":
                self.skip_comment()
                continue

            if self.current.isdigit():
                return self.number()

            if self.current.isalpha() or self.current == "_":
                return self.identifier()

            if self.current == '"':
                return self.string()

            if self.current == "=":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TokenType.EQEQ, "==")
                self.advance()
                return Token(TokenType.EQUAL, "=")

            if self.current == "!":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TokenType.NEQ, "!=")

            if self.current == "<":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TokenType.LTE, "<=")
                self.advance()
                return Token(TokenType.LT, "<")

            if self.current == ">":
                if self.peek() == "=":
                    self.advance()
                    self.advance()
                    return Token(TokenType.GTE, ">=")
                self.advance()
                return Token(TokenType.GT, ">")

            if self.current == "+":
                self.advance()
                return Token(TokenType.PLUS, "+")

            if self.current == "-":
                self.advance()
                return Token(TokenType.MINUS, "-")

            if self.current == "*":
                self.advance()
                return Token(TokenType.STAR, "*")

            if self.current == "/":
                self.advance()
                return Token(TokenType.SLASH, "/")

            if self.current == "(":
                self.advance()
                return Token(TokenType.LPAREN, "(")

            if self.current == ")":
                self.advance()
                return Token(TokenType.RPAREN, ")")

            raise Exception(f"Unexpected character: {self.current}")
