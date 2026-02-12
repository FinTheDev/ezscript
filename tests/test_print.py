from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.runtime.interpreter import Interpreter

code = 'print("hello")'

lexer = Lexer(code)
parser = Parser(lexer)
ast = parser.parse()

interpreter = Interpreter()
interpreter.visit(ast)
