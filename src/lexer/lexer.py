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
    EQEQ       = auto()
    NEQ        = auto()
    LT         = auto()
    GT         = auto()
    LTE        = auto()
    GTE        = auto()
    LPAREN     = auto()
    RPAREN     = auto()
    EOF        = auto()

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type.name}:{self.value}"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current = text[0] if text else None

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

    def skip_whitespace(self):
        while self.current and self.current.isspace():
            self.advance()

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
        if result == "true":
            return Token(TokenType.TRUE, True)
        if result == "false":
            return Token(TokenType.FALSE, False)
        return Token(TokenType.IDENTIFIER, result)

    def get_next_token(self):
        while self.current:

            if self.current.isspace():
                self.skip_whitespace()
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

        return Token(TokenType.EOF, None)

if __name__ == "__main__":
    code = """
            x = 5 + 3
            print("hi")
            # comment
           """

    lexer = Lexer(code)

    token = lexer.get_next_token()
    while token.type != TokenType.EOF:
        print(token)
        token = lexer.get_next_token()

    print(token)
