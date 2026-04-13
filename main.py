from lexer import lexer
from parser import parser
from interpreter import interpret

# Pergunta ao usuário se quer ativar modo debug
DEBUG = input("Modo debug? (s/n): ").lower() == "s"

while True:
    try:
        # Entrada do usuário
        code = input(">> ")

        # 🔹 ANÁLISE LÉXICA (AFD)
        tokens = lexer(code)

        if DEBUG:
            print("Tokens:", tokens)

        # 🔹 ANÁLISE SINTÁTICA (GLC)
        parser(tokens)

        if DEBUG:
            print("Código válido!")

        # 🔹 INTERPRETAÇÃO (SEMÂNTICA)
        interpret(tokens)

    except Exception as e:
        print(e)