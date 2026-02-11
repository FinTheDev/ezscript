from src.lexer.lexer import Lexer, TokenType

code = """
        x = 5 + 3
        print("hi")
        # comment
       """

lexer = Lexer(code)

token = lexer.get_next_token()
while token.type != TokenType.EOF:
    print(token)
    token = lexer.get_next_token()

print(token)
