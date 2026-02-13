class Interpreter:
    def __init__(self):
        self.env = {}

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
        if node.name not in self.env:
            raise Exception(f"Undefined variable {node.name}")
        return self.env[node.name]

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

    def visit_Assignment(self, node):
        value = self.visit(node.value)
        self.env[node.name] = value
        return value

    def visit_Call(self, node):
        value = self.visit(node.argument)

        if node.name == "print":
            print(value)
            return None

        raise Exception(f"Unknown function {node.name}")

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

    def visit_While(self, node):
        while self.visit(node.condition):
            self.visit(node.block)
        return None
