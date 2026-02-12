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

    def visit_Assignment(self, node):
        value = self.visit(node.value)
        self.env[node.name] = value
        return value
