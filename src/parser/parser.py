from src.lexer.lexer import TokenType
from src.ast.nodes import *

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current = lexer.get_next_token()

    def eat(self, token_type):
        if self.current.type == token_type:
            self.current = self.lexer.get_next_token()
        else:
            raise Exception(f"Expected {token_type}, got {self.current.type}")

    def factor(self):
        token = self.current

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)

        if token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token.value)

        if token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Bool(True)

        if token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Bool(False)

        if token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Identifier(token.value)

        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        raise Exception("Invalid factor")

    def term(self):
        node = self.factor()

        while self.current.type in (TokenType.STAR, TokenType.SLASH):
            op = self.current
            if op.type == TokenType.STAR:
                self.eat(TokenType.STAR)
            else:
                self.eat(TokenType.SLASH)
            node = BinaryOp(node, op, self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current
            if op.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            node = BinaryOp(node, op, self.term())

        return node

    def assignment(self):
        name = self.current.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.EQUAL)
        value = self.expr()
        return Assignment(name, value)

    def parse(self):
        if self.current.type == TokenType.IDENTIFIER and self.lexer.peek() == "=":
            return self.assignment()
        return self.expr()
