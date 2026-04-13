variables = {}

def interpret(tokens):
    # Caso: var x = ...
    if tokens[0][0] == "VAR":
        name = tokens[1][1]

        # Caso simples: var x = 10
        if len(tokens) == 4:
            value = int(tokens[3][1])

        # Caso com expressão: var x = 5 + 3
        else:
            num1 = int(tokens[3][1])
            op = tokens[4][0]
            num2 = int(tokens[5][1])

            if op == "PLUS":
                value = num1 + num2
            elif op == "MINUS":
                value = num1 - num2
            elif op == "MULT":
                value = num1 * num2
            elif op == "DIV":
                value = num1 / num2
            else:
                raise Exception("Operador inválido")

        variables[name] = value

    # Caso: print(x)
    elif tokens[0][0] == "PRINT":
        name = tokens[2][1]

        if name in variables:
            print(variables[name])
        else:
            print("Erro: variável não definida")