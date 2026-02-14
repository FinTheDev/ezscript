from src.ast.nodes import *

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def get(self, name):
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise Exception(f"Undefined variable {name}")

    def set(self, name, value):
        self.values[name] = value

    def __repr__(self):
        return f"Environment({self.values})"

class RuntimeFunction:
    def __init__(self, name, params, body, closure):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def __repr__(self):
        return f"<function {self.name}({', '.join(self.params)})>"

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.env = Environment()

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, None)
        if not method:
            raise Exception(f"No visit method for {type(node).__name__}")
        return method(node)

    def visit_Number(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Bool(self, node):
        return node.value

    def visit_Identifier(self, node):
        return self.env.get(node.name)

    def visit_BinaryOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type.name == "PLUS":
            return left + right
        if node.op.type.name == "MINUS":
            return left - right
        if node.op.type.name == "STAR":
            return left * right
        if node.op.type.name == "SLASH":
            return left / right
        if node.op.type.name == "GT":
            return left > right
        if node.op.type.name == "LT":
            return left < right
        if node.op.type.name == "GTE":
            return left >= right
        if node.op.type.name == "LTE":
            return left <= right
        if node.op.type.name == "EQEQ":
            return left == right
        if node.op.type.name == "NEQ":
            return left != right
        if node.op.type.name == "AND":
            return left and right
        if node.op.type.name == "OR":
            return left or right

    def visit_Assignment(self, node):
        value = self.visit(node.value)
        self.env.set(node.name, value)
        return value

    def visit_Call(self, node):
        if isinstance(node.callee, Identifier) and node.callee.name == "print":
            values = [self.visit(arg) for arg in node.arguments]
            print(*values)
            return None

        function = self.visit(node.callee)

        if not isinstance(function, RuntimeFunction):
            raise Exception("Can only call functions")

        arguments = [self.visit(arg) for arg in node.arguments]

        if len(arguments) != len(function.params):
            raise Exception("Wrong number of arguments")

        new_env = Environment(parent=function.closure)

        for name, value in zip(function.params, arguments):
            new_env.set(name, value)

        previous_env = self.env
        self.env = new_env

        try:
            self.visit(function.body)
        except ReturnSignal as r:
            self.env = previous_env
            return r.value

        self.env = previous_env
        return None

    def visit_Block(self, node):
        result = None
        for stmt in node.statements:
            result = self.visit(stmt)
        return result

    def visit_If(self, node):
        for condition, block in node.branches:
            if self.visit(condition):
                return self.visit(block)

        if node.else_block:
            return self.visit(node.else_block)

        return None

    def visit_UnaryOp(self, node):
        value = self.visit(node.expr)

        if node.op.type.name == "NOT":
            return not value

        raise Exception("Unsupported unary operator")

    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.block)
        return None

    def visit_Function(self, node):
        function = RuntimeFunction(node.name, node.params, node.body, self.env)
        self.env.set(node.name, function)
        return None

    def visit_Return(self, node):
        value = self.visit(node.value)
        raise ReturnSignal(value)
