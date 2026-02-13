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
            name = token.value
            self.eat(TokenType.IDENTIFIER)

            if self.current.type == TokenType.LPAREN:
                self.eat(TokenType.LPAREN)
                argument = self.expr()
                self.eat(TokenType.RPAREN)
                return Call(name, argument)

            return Identifier(name)

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

    def arithmetic(self):
        node = self.term()

        while self.current.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current
            if op.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            node = BinaryOp(node, op, self.term())

        return node

    def comparison(self):
        node = self.arithmetic()

        while self.current.type in (
            TokenType.EQEQ,
            TokenType.NEQ,
            TokenType.LT,
            TokenType.GT,
            TokenType.LTE,
            TokenType.GTE,
        ):
            op = self.current
            self.eat(op.type)
            node = BinaryOp(node, op, self.arithmetic())

        return node

    def expr(self):
        return self.comparison()

    def block(self):
        self.eat(TokenType.NEWLINE)
        self.eat(TokenType.INDENT)

        statements = []

        while self.current.type != TokenType.DEDENT:
            if self.current.type == TokenType.NEWLINE:
                self.eat(TokenType.NEWLINE)
                continue

            statements.append(self.statement())

        self.eat(TokenType.DEDENT)

        return Block(statements)

    def if_statement(self):
        branches = []

        self.eat(TokenType.IF)
        condition = self.expr()
        self.eat(TokenType.DO)

        block_node = self.block()
        branches.append((condition, block_node))

        while self.current.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)

            if self.current.type == TokenType.DO:
                self.eat(TokenType.DO)
                else_block = self.block()
                return If(branches, else_block)

            condition = self.expr()
            self.eat(TokenType.DO)
            block_node = self.block()
            branches.append((condition, block_node))

        return If(branches)

    def while_statement(self):
        self.eat(TokenType.WHILE)
        condition = self.expr()
        self.eat(TokenType.DO)
        block_node = self.block()
        return While(condition, block_node)

    def statement(self):
        if self.current.type == TokenType.IF:
            return self.if_statement()

        if self.current.type == TokenType.WHILE:
            return self.while_statement()

        if self.current.type == TokenType.IDENTIFIER:
            next_token = self.peek_token()
            if next_token.type == TokenType.EQUAL:
                return self.assignment()
            return self.expr()

        return self.expr()

    def assignment(self):
        name = self.current.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.EQUAL)
        value = self.expr()
        return Assignment(name, value)

    def peek_token(self):
        old_pos = self.lexer.pos
        old_current = self.lexer.current

        token = self.lexer.get_next_token()

        self.lexer.pos = old_pos
        self.lexer.current = old_current

        return token

    def parse(self):
        statements = []

        while self.current.type != TokenType.EOF:
            if self.current.type == TokenType.NEWLINE:
                self.eat(TokenType.NEWLINE)
                continue

            statements.append(self.statement())

        return Block(statements)
