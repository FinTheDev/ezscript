import sys
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.runtime.interpreter import Interpreter

def run_file(path):
    with open(path, "r") as f:
        code = f.read()

    lexer = Lexer(code)
    parser = Parser(lexer)
    ast = parser.parse()

    interpreter = Interpreter()
    interpreter.visit(ast)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ez <file.ez>")
        sys.exit(1)

    run_file(sys.argv[1])
