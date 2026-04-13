# Dicionário que armazena as variáveis (memória do programa)
variables = {}

def interpret(tokens):
    # 🔹 Caso: declaração de variável
    # Ex: var x = 5 + 3
    if tokens[0][0] == "VAR":
        name = tokens[1][1]  # nome da variável

        # Pega toda a expressão após o '='
        expression_tokens = tokens[3:]

        # Constrói a expressão como string (ex: "5+3*2")
        expression = ""
        for token in expression_tokens:
            expression += token[1]

        try:
            # Avalia a expressão
            value = eval(expression)
        except:
            raise Exception("Erro ao avaliar expressão")

        # Armazena o valor na memória
        variables[name] = value

    # 🔹 Caso: impressão
    # Ex: print(x)
    elif tokens[0][0] == "PRINT":
        name = tokens[2][1]

        if name in variables:
            print(variables[name])  # imprime valor
        else:
            print("Erro: variável não definida")