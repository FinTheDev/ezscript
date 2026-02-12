from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.runtime.interpreter import Interpreter

lexer = Lexer("""
x = 5 + 3 * 2
if x > 10 do
    print("greater than 10")
else x == 11 do
    print("x is 11")
else x < 10 do
    print("less than 10")
else do
    print("x is not a number")
""")
parser = Parser(lexer)
ast = parser.parse()

interpreter = Interpreter()
result = interpreter.visit(ast)

print("result:", result)
print("env:", interpreter.env)
