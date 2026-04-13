from lexer import lexer
from parser import parser
from interpreter import interpret

while True:
    try:
        code = input(">> ")

        tokens = lexer(code)
        print("Tokens:", tokens)

        parser(tokens)
        print("Código válido!")

        interpret(tokens)

    except Exception as e:
        print(e)