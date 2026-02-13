from src.lexer.lexer import Lexer
from src.parser.parser import Parser

code = """
x = 5 + 3 * 2
if x > 10 do
    print("greater than 10")
else x == 11 do
    print("x is 11")
else x < 10 do
    print("less than 10")
else do
    print("x is not a number")

y = 0
while y < 3 do
    print(y)
    y = y + 1
"""

lexer = Lexer(code)
parser = Parser(lexer)
ast = parser.parse()

print(ast)
