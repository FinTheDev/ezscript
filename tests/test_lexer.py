from src.lexer.lexer import Lexer, TokenType

code = """
x = 5 + 3
print("hi")
# comment

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

token = lexer.get_next_token()
while token.type != TokenType.EOF:
    print(token)
    token = lexer.get_next_token()

print(token)
