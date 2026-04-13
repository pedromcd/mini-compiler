from lexer import lexer
from parser import parser
from interpreter import interpret

# Pergunta ao usuário se quer ativar modo debug
print("=== Configuração Inicial ===")
while True:
    escolha = input("Modo debug? (s/n): ").strip().lower()

    if escolha == "s":
        DEBUG = True
        break
    elif escolha == "n":
        DEBUG = False
        break
    else:
        print("Entrada inválida. Digite apenas 's' ou 'n'.")

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