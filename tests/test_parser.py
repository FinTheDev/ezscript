from src.lexer.lexer import Lexer
from src.parser.parser import Parser

code = "x = 5 + 3 * 2"

lexer = Lexer(code)
parser = Parser(lexer)
ast = parser.parse()

print(ast)
