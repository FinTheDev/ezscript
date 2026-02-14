class Number:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"

class String:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"String({self.value})"

class Bool:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Bool({self.value})"

class Identifier:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier({self.name})"

class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinaryOp({self.left}, {self.op.type.name}, {self.right})"

class UnaryOp:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def __repr__(self):
        return f"UnaryOp({self.op.type.name}, {self.expr})"

class Assignment:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"Assignment({self.name}, {self.value})"

class Call:
    def __init__(self, callee, arguments):
        self.callee = callee
        self.arguments = arguments

    def __repr__(self):
        return f"Call({self.callee}, {self.arguments})"

class Block:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"Block({self.statements})"

class If:
    def __init__(self, branches, else_block=None):
        self.branches = branches
        self.else_block = else_block

    def __repr__(self):
        return f"If({self.branches}, else={self.else_block})"

class While:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __repr__(self):
        return f"While({self.condition}, {self.block})"

class Function:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"Function({self.name}, {self.params}, {self.body})"

class Return:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Return({self.value})"
