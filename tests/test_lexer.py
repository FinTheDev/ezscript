from src.lexer.lexer import Lexer, TokenType

code = """
x = 5 + 3
print("hi")
# comment

if x == 8 do
    print("eight")
else x > 7 do
    print("greater than seven")
"""

lexer = Lexer(code)

token = lexer.get_next_token()
while token.type != TokenType.EOF:
    print(token)
    token = lexer.get_next_token()

print(token)
