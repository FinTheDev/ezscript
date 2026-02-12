from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.runtime.interpreter import Interpreter

lexer = Lexer("x = 5 + 3 * 2")
parser = Parser(lexer)
ast = parser.parse()

interpreter = Interpreter()
result = interpreter.visit(ast)

print("result:", result)
print("env:", interpreter.env)
